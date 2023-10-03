import holoviews as hv
import panel as pn


from holoviews import opts
from holoviews.streams import Counter
from simulator import Simulation

hv.extension("plotly")

TIME_STEP = 0.05
PARTICLE_COUNT = 100
GAS_VOLUME = 4
GAS_SIDE_LEN = GAS_VOLUME ** (1 / 3)
GAS_TEMP = 237

sim = Simulation(PARTICLE_COUNT, 1.2e-20, 0.01, GAS_TEMP, GAS_VOLUME, TIME_STEP)


def update_gas_display(counter):
    points = sim.get_points()
    return hv.Scatter3D(points)


counter = Counter(transient=True)
dmap = hv.DynamicMap(update_gas_display, streams=[counter])

axis_lims = (-GAS_SIDE_LEN / 2, GAS_SIDE_LEN / 2)
plot = dmap.opts(
    opts.Scatter3D(
        title="Ideal Gas Simulator",
        height=500,
        size=5,
        xlim=axis_lims,
        ylim=axis_lims,
        zlim=axis_lims,
        # responsive=False,
        # xaxis=None,
        # yaxis=None,
    )
)


panel = pn.pane.HoloViews(plot, center=True)


def advance():
    sim.next_step()
    counter.event(counter=counter.counter + 1)


pn.state.add_periodic_callback(advance, period=int(TIME_STEP * 1000))
panel.servable()
