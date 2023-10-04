import holoviews as hv
import panel as pn
import matplotlib as mpl

from holoviews import opts
from holoviews.streams import Counter

import pandas as pd
import io

from simulator import Simulation

mpl.use("agg")

pn.extension(throttled=True)
hv.extension("matplotlib")

TIME_STEP = 0.05
PARTICLE_COUNT = 10
GAS_VOLUME = 4
GAS_SIDE_LEN = GAS_VOLUME ** (1 / 3)
GAS_TEMP = 237

sim = Simulation(PARTICLE_COUNT, 1.2e-20, 0.01, GAS_TEMP, GAS_VOLUME, TIME_STEP)


def update_gas_display(counter):
    points = (sim.r[:, 0], sim.r[:, 1], sim.r[:, 2])
    return hv.Scatter3D(points)


def remove_ticks(plot, element):
    plot.handles["axis"].set_xticklabels([])
    plot.handles["axis"].set_yticklabels([])
    plot.handles["axis"].set_zticklabels([])


counter = Counter(transient=True)

axis_lims = (-GAS_SIDE_LEN / 2, GAS_SIDE_LEN / 2)
plot = hv.DynamicMap(update_gas_display, streams=[counter]).opts(
    opts.Scatter3D(
        apply_ranges=False,
        labelled=[],
        xlim=axis_lims,
        ylim=axis_lims,
        zlim=axis_lims,
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
periodic_callback = pn.state.add_periodic_callback(advance, period=int(0.2 * 10**3))


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
