"""
    This file contains all the experiments that can be run.
"""

from plotly_resampler import FigureResampler, FigureWidgetResampler
import plotly.graph_objects as go
from benchmark.timed_process_downsampling import patch_process_downsampling, ElapsedTime
import time

def compare_downsampling(x, y, option):
    if option == "plotly":
        return -1
    ElapsedTime.elapsed_time = None
    with patch_process_downsampling():
        figure = FigureResampler(go.Figure())
        figure.add_trace(go.Scattergl(name=option, showlegend=True), hf_x=x, hf_y=y)
        del figure
    return ElapsedTime.elapsed_time

def compare_add_trace(x, y, option):
    if option == "plotly":
        figure = go.Figure()
        start = time.perf_counter()
        figure.add_trace(go.Scattergl(x=x, y=y, name=option, showlegend=True))
        end = time.perf_counter()
        return end - start
    
    figure = FigureWidgetResampler(go.Figure())
    start = time.perf_counter()
    figure.add_trace(go.Scattergl(name=option, showlegend=True), hf_x=x, hf_y=y)
    end = time.perf_counter()
    return end - start
