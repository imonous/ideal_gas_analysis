import holoviews as hv

hv.extension("bokeh")


def hide_table_index(plot, element):
    plot.handles["table"].index_position = None


def table(data):
    heads = ["T"] + [f"Trial {i+1}" for i in range(len(data[0]) - 1)]
    return hv.Table(data, heads).opts(hooks=[hide_table_index])


def scatter(data):
    return hv.Scatter(data)


def curve(data):
    return hv.Curve(data)


def error_bars(data):
    return hv.ErrorBars(data, vdims=["y", "neg_err", "pos_err"])


def save_png(obj, file_path):
    hv.save(obj, file_path, fmt="png")
