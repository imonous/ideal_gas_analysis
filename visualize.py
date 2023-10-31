import holoviews as hv
import numpy as np

hv.extension("bokeh")


def table(data):
    heads = ["T"] + [f"Trial {i+1}" for i in range(len(data[0]) - 1)]
    return hv.Table(data, heads)


def scatter(data):
    return hv.Scatter(data)


def save_png(obj, file_path):
    hv.save(obj, file_path, fmt="png")
