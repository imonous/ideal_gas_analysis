import holoviews as hv
import panel as pn
import pandas as pd
from holoviews import opts
from holoviews.streams import Counter
import io

from simulator import Simulation

pn.extension("plotly", "tabulator")
pn.config.throttled = True
hv.extension("plotly")

TIME_STEP = 0.01
PARTICLE_COUNT = 100
GAS_VOLUME = 4
GAS_SIDE_LEN = GAS_VOLUME ** (1 / 3)
GAS_TEMP = 237

sim = Simulation(PARTICLE_COUNT, 1.2e-20, 0.01, GAS_TEMP, GAS_VOLUME, TIME_STEP)


def update_gas_display(counter):
    points = (sim.r[:, 0], sim.r[:, 1], sim.r[:, 2])
    return hv.Scatter3D(points)


counter = Counter(transient=True)
dmap = hv.DynamicMap(update_gas_display, streams=[counter])


axis_lims = (-GAS_SIDE_LEN / 2, GAS_SIDE_LEN / 2)
plot = dmap.opts(
    opts.Scatter3D(
        size=5,
        xlim=axis_lims,
        ylim=axis_lims,
        zlim=axis_lims,
    )
)


def advance():
    sim.next_step()
    counter.event(counter=counter.counter + 1)


gas_display = pn.pane.HoloViews(plot, center=True, backend="plotly")
periodic_callback = pn.state.add_periodic_callback(advance, period=50)


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
