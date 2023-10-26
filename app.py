import holoviews as hv
import panel as pn
import matplotlib as mpl
import pandas as pd
import io

from holoviews import opts
from holoviews.streams import Counter

from simulation import Simulation


APP_TIME_STEP = 0.1e3
mpl.use("agg")
pn.extension(
    throttled=True,
    disconnect_notification="Connection lost, try reloading the page!",
    ready_notification="Application fully loaded.",
    # defer_load=True,
    # loading_indicator=False,
)
hv.extension("matplotlib")
sim = Simulation(n_particles=10, mass=1.2e-20, rad=0.01, T=237, dt=0.05, V=2)


def update_gas_display(counter):
    points = (sim.r[:, 0], sim.r[:, 1], sim.r[:, 2])
    return hv.Scatter3D(points)


def remove_ticks(plot, element):
    plot.handles["axis"].set_xticklabels([])
    plot.handles["axis"].set_yticklabels([])
    plot.handles["axis"].set_zticklabels([])


counter = Counter(transient=True)

plot = hv.DynamicMap(update_gas_display, streams=[counter]).opts(
    opts.Scatter3D(
        apply_ranges=False,
        labelled=[],
        xlim=(-sim.halfL, sim.halfL),
        ylim=(-sim.halfL, sim.halfL),
        zlim=(-sim.halfL, sim.halfL),
        azimuth=45,
        elevation=10,
        color="x",
        cmap="kr",
        s=20,
        hooks=[remove_ticks],
    )
)


def advance():
    sim.next_step()
    counter.event(counter=counter.counter + 1)


gas_display = pn.pane.HoloViews(plot)
periodic_callback = pn.state.add_periodic_callback(advance, period=int(APP_TIME_STEP))


temperature_slider = pn.widgets.IntSlider(
    name="Temperature (K)",
    value=273,
    start=0,
    end=1000,
    step=3,
)


def temperature_slider_callback(event):
    if event.type == "changed":
        sim.set_temperature(event.new)


temperature_slider.param.watch(temperature_slider_callback, ["value"])


def get_raw_data():
    df = pd.DataFrame(
        {
            "x velocity (m/s)": sim.r[:, 0],
            "y velocity (m/s)": sim.r[:, 1],
            "z velocity (m/s)": sim.r[:, 2],
        }
    )
    file = io.BytesIO()
    df.to_csv(file, index=False)
    file.seek(0)
    return file


raw_data_download = pn.widgets.FileDownload(
    callback=get_raw_data, filename="raw_data.csv"
)


toggle_simulation = pn.widgets.Button(name="Pause Simulation")


def toggle_simulation_callback(event):
    if toggle_simulation.clicks % 2 != 0:
        toggle_simulation.name = "Resume Simulation"
        periodic_callback.stop()
    else:
        toggle_simulation.name = "Pause Simulation"
        periodic_callback.start()


toggle_simulation.on_click(toggle_simulation_callback)


app = pn.template.VanillaTemplate(
    title="Ideal Gas Simulator",
    sidebar=[
        temperature_slider,
        raw_data_download,
        toggle_simulation,
    ],
)
app.main.append(pn.WidgetBox(gas_display))
app.servable()
