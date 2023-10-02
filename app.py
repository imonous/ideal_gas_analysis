import panel as pn
import holoviews as hv
from holoviews.streams import Pipe
from streamz import Stream

from simulator import Simulation

pn.extension("plotly")
hv.extension("plotly")

TIME_STEP = 0.2
PARTICLE_COUNT = 1000
GAS_VOLUME = 2
GAS_SIDE_LEN = 2 ** (1 / 3) / 2

sim = Simulation(PARTICLE_COUNT, 1.2e-20, 0.01, 500, GAS_VOLUME, TIME_STEP)
source = Stream()


def display_gas(data):
    axis_lim = (-GAS_SIDE_LEN, GAS_SIDE_LEN)
    return hv.Scatter3D(data).opts(size=3, xlim=axis_lim, ylim=axis_lim, zlim=axis_lim)


def emit():
    sim.next_step()
    source.emit((sim.r[:, 0], sim.r[:, 1], sim.r[:, 2]))


gas_display_stream = source.map(display_gas)
gas_display_pane = pn.pane.Streamz(gas_display_stream, height=350)

layout = pn.Row(gas_display_pane)
pn.state.add_periodic_callback(emit, period=int(TIME_STEP * 10**3))
layout.servable()
