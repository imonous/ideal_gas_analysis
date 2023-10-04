import holoviews as hv
import panel as pn
import pandas as pd
from holoviews import opts
from holoviews.streams import Counter
import io

from simulator import Simulation

pn.extension("plotly", "tabulator")
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


gas_display = pn.pane.HoloViews(plot, center=True, backend="plotly")


def advance():
    sim.next_step()
    counter.event(counter=counter.counter + 1)


temperature_slider = pn.widgets.IntSlider(
    name="Temperature (K)",
    value=273,
    start=0,
    end=1000,
    step=5,
)
update_temperature_button = pn.widgets.Button(
    name="Update Temperature", button_type="primary"
)
update_temperature_button.on_click(
    lambda event: sim.set_temperature(temperature_slider.value)
)


def get_raw_data():
    csv_buffer = io.BytesIO()
    df = pd.DataFrame(
        {
            "x velocity (m/s)": sim.r[:, 0],
            "y velocity (m/s)": sim.r[:, 1],
            "z velocity (m/s)": sim.r[:, 2],
        }
    )
    df.to_csv(csv_buffer, index=False)
    return csv_buffer


raw_data_download = pn.widgets.FileDownload(
    file=get_raw_data(), filename="raw_data.csv"
)


pn.state.add_periodic_callback(advance, period=50)

app = pn.template.BootstrapTemplate(
    title="Ideal Gas Simulator",
    sidebar=[
        temperature_slider,
        update_temperature_button,
        raw_data_download,
    ],
)
app.main.append(gas_display)
app.servable()
