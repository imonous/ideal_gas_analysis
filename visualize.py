import holoviews as hv

hv.extension("matplotlib", "bokeh")


def table(data, processed=False):
    if not processed:
        hv.output(backend="matplotlib", size=250, dpi=300)
    else:
        hv.output(backend="matplotlib", size=450)

    offset = 4 if processed else 1  # account for non-trials
    heads = ["Temperature"] + [f"Trial {i+1}" for i in range(len(data[0]) - offset)]
    if processed:
        heads += ["Average", "Absolute uncert.", "Relative uncert. %"]
    return hv.Table(data, heads).opts(fontscale=4)


def scatter(data):
    hv.output(backend="bokeh")
    return hv.Scatter(data, kdims=["T"], vdims="Part", label="Actual").opts(
        marker="x", size=10, color="blue", fill_alpha=0.8
    )


def curve(data, fit=False):
    hv.output(backend="bokeh")
    return (
        hv.Curve(data, kdims=["T"], vdims="Part")
        if not fit
        else hv.Curve(data, kdims=["T"], vdims="Part", label="Fitted").opts(
            color="orange"
        )
    )


def error_bars(data):
    hv.output(backend="bokeh")
    return hv.ErrorBars(data, vdims=["y", "neg_err", "pos_err"])


def save_png(obj, file_path):
    hv.save(obj, file_path, fmt="png")
