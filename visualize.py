import holoviews as hv

hv.extension("bokeh")


def hide_table_index(plot, element):
    plot.handles["table"].index_position = None


def table(data, processed=False):
    offset = 4 if processed else 1  # account for non-trials
    heads = ["Temperature"] + [f"Trial {i+1}" for i in range(len(data[0]) - offset)]
    if processed:
        heads += ["Average", "Absolute uncert.", "Relative uncert."]
    return hv.Table(data, heads).opts(hooks=[hide_table_index], width=800)


def scatter(data):
    return hv.Scatter(data, kdims=["T"], vdims="Part", label="Actual").opts(
        marker="x", size=10, color="blue", fill_alpha=0.8
    )


def curve(data, fit=False):
    return (
        hv.Curve(data, kdims=["T"], vdims="Part")
        if not fit
        else hv.Curve(data, kdims=["T"], vdims="Part", label="Fitted").opts(
            color="orange"
        )
    )


def error_bars(data):
    return hv.ErrorBars(data, vdims=["y", "neg_err", "pos_err"])


def save_png(obj, file_path):
    hv.save(obj, file_path, fmt="png")
