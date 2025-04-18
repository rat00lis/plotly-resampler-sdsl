import time
from unittest.mock import patch
from plotly_resampler.aggregation.plotly_aggregator_parser import PlotlyAggregatorParser
from plotly_resampler import FigureWidgetResampler
import numpy as np
from contextlib import contextmanager

class ElapsedTime:
    elapsed_time = None

# Backup del original para poder llamarlo desde el wrapper
original_process_downsampling = PlotlyAggregatorParser.process_downsampling

# Versión con cronómetro
def timed_process_downsampling(
        hf_trace_data: dict,
        hf_x: np.ndarray,
        hf_y: np.ndarray,
        hf_x_parsed: np.ndarray,
        hf_y_parsed: np.ndarray,
        start_idx: int,
    ): 
    start_time = time.perf_counter()
    result = original_process_downsampling(
        hf_trace_data,
        hf_x,
        hf_y,
        hf_x_parsed,
        hf_y_parsed,
        start_idx
    )
    end_time = time.perf_counter()
    ElapsedTime.elapsed_time = end_time - start_time
    return result

# Parcheo temporal
@contextmanager
def patch_process_downsampling():
    with patch.object(PlotlyAggregatorParser, "process_downsampling", new=timed_process_downsampling):
        yield