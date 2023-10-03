# import panel as pn
# import holoviews as hv
# from streamz import Stream

# from simulator import Simulation

# pn.extension("plotly")
# hv.extension("plotly")

# TIME_STEP = 0.01
# PARTICLE_COUNT = 5
# GAS_VOLUME = 2
# GAS_SIDE_LEN = GAS_VOLUME ** (1 / 3)
# GAS_TEMP = 237

# sim = Simulation(PARTICLE_COUNT, 1.2e-20, 0.01, GAS_TEMP, GAS_VOLUME, TIME_STEP)
# source = Stream()


# def display_gas(data):
#     axis_lim = (-GAS_SIDE_LEN , GAS_SIDE_LEN ) # FAKE
#     return hv.Scatter3D(data).opts(size=5, xlim=axis_lim, ylim=axis_lim, zlim=axis_lim)


# def emit():
#     sim.next_step()
#     source.emit((sim.r[:, 0], sim.r[:, 1], sim.r[:, 2]))


# gas_display_stream = source.map(display_gas)
# gas_display_pane = pn.pane.Streamz(gas_display_stream, height=350)

# layout = pn.Row(gas_display_pane)
# pn.state.add_periodic_callback(emit, period=int(TIME_STEP * 10**3))
# layout.servable()


#################################################################


# import panel as pn

# import holoviews as hv
# from holoviews.streams import Stream, param

# from simulator import Simulation

# pn.extension("plotly")
# hv.extension("plotly")

# TIME_STEP = 0.05
# PARTICLE_COUNT = 5
# GAS_VOLUME = 2
# GAS_SIDE_LEN = GAS_VOLUME ** (1 / 3)
# GAS_TEMP = 237


# def sim_display():
#     sim = Simulation(PARTICLE_COUNT, 1.2e-20, 0.01, GAS_TEMP, GAS_VOLUME, TIME_STEP)
#     axis_lims = (-GAS_SIDE_LEN, GAS_SIDE_LEN)  # FAKE
#     while True:
#         sim.next_step()
#         points = (sim.r[:, 0], sim.r[:, 1], sim.r[:, 2])
#         yield hv.Scatter3D(points).opts(
#             size=5, xlim=axis_lims, ylim=axis_lims, zlim=axis_lims
#         )


# sim_generator = sim_display()
# dmap = hv.DynamicMap(sim_generator, streams=[Stream.define("Next")()])

# app = pn.Row(dmap)
# dmap.periodic(0.1, timeout=3, block=False)
# pn.state.add_periodic_callback(dmap.event, period=int(TIME_STEP * 1000))
# app.servable()


#################################################################


# import panel as pn

# import holoviews as hv
# from holoviews.streams import Stream, Pipe

# from simulator import Simulation

# pn.extension("plotly")
# hv.extension("plotly")

# TIME_STEP = 0.2
# PARTICLE_COUNT = 2
# GAS_VOLUME = 2
# GAS_SIDE_LEN = GAS_VOLUME ** (1 / 3)
# GAS_TEMP = 237

# sim = Simulation(PARTICLE_COUNT, 1.2e-20, 0.01, GAS_TEMP, GAS_VOLUME, TIME_STEP)
# pipe = Pipe(data=sim.r)


# axis_lims = (-GAS_SIDE_LEN, GAS_SIDE_LEN)  # FAKE


# def sim_display(data):
#     points = (data[:, 0], data[:, 1], data[:, 2])
#     return hv.Scatter3D(points).opts(
#         size=5,
#         xlim=axis_lims,
#         ylim=axis_lims,
#         zlim=axis_lims,
#     )


# dmap = hv.DynamicMap(sim_display, streams=[pipe])


# def update():
#     sim.next_step()
#     pipe.send(sim.r)


# app = pn.Row(dmap)
# pn.state.add_periodic_callback(update, period=int(TIME_STEP * 1000))
# app.servable()


#################################################################


# import panel as pn
# import holoviews as hv
# from holoviews.streams import Buffer
# import pandas as pd

# from simulator import Simulation

# pn.extension("plotly")
# hv.extension("plotly")

# TIME_STEP = 0.05
# PARTICLE_COUNT = 2
# GAS_VOLUME = 2
# GAS_SIDE_LEN = GAS_VOLUME ** (1 / 3)
# GAS_TEMP = 237

# sim = Simulation(PARTICLE_COUNT, 1.2e-20, 0.01, GAS_TEMP, GAS_VOLUME, TIME_STEP)


# def gas_df_points():
#     return pd.DataFrame({"x": sim.r[:, 0], "y": sim.r[:, 1], "z": sim.r[:, 2]})


# stream = Buffer(gas_df_points(), length=PARTICLE_COUNT, index=False)
# dmap = hv.DynamicMap(hv.Scatter3D, streams=[stream])

# axis_lims = (-GAS_SIDE_LEN, GAS_SIDE_LEN)  # FAKE
# dmap.opts(xlim=axis_lims, ylim=axis_lims, zlim=axis_lims)


# def generate_gas():
#     while True:
#         sim.next_step()
#         yield gas_df_points()


# gas = generate_gas()


# def update():
#     stream.send(next(gas))


# app = pn.Row(dmap)
# pn.state.add_periodic_callback(update, period=int(TIME_STEP * 1000))
# app.servable()
