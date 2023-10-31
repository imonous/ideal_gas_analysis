import holoviews as hv
import numpy as np

hv.extension("bokeh")


def format_data_table(T, data, precision=3):
    res = [[f"{n:.{precision}f}" for n in row] for row in data]
    res = np.insert(res, 0, [f"{int(n)}K" for n in T], axis=1)
    return res


def table(data):
    heads = ["T"] + [f"Trial {i+1}" for i in range(len(data[0]) - 1)]
    return hv.Table(data, heads)


def format_data_scatter(T, data):
    return np.array([(T[i], data[i]) for i in range(len(data))])


def scatter(data):
    return hv.Scatter(data)


def save_png(obj, file_path):
    hv.save(obj, file_path, fmt="png")
