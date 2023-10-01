import panel as pn
import holoviews as hv
from streamz import Stream
from simulator import Simulation

hv.extension("plotly")

sim = Simulation(500, 1.2e-20, 0.01, 500, 2, 0.05)


# def display_gas(data):
#     hv.Scatter3D((data[:, 0], data[:, 1], data[:, 2])).opts(
#         size=5, height=600, width=600
#     )


# source = Stream()
# stream = source.map(display_gas)


# def emit():
#     sim.next_step()
#     source.emit(sim.r)


# gas_display = pn.pane.Streamz(stream, height=350)
# pn.state.add_periodic_callback(emit, period=1000, count=5)

# gas_display.servable()
