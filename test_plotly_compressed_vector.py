import numpy as np
from benchmark.input_handler import InputHandler
import plotly.graph_objects as go
from plotly_resampler import FigureWidgetResampler

file_name = "input/dataset_bridge/d_08_1_1_1.txt"

input_tools = InputHandler()

sdsl4py_sample_x, sdsl4py_sample_y = input_tools.get_from_file(
    file_path=file_name,
    option="sdsl4py",
    column=1,
    delimiter=";",
)

plotly_figure = go.Figure()
plotly_figure.add_trace(
    go.Scatter(
        x = sdsl4py_sample_x,
        y = sdsl4py_sample_y,
        mode = "lines"
    )
)
