import time
from typing import Tuple
from plotly_resampler.aggregation.plotly_aggregator_parser import PlotlyAggregatorParser
import numpy as np

class timed_PlotlyAggregatorParser(PlotlyAggregatorParser):
    """
    A subclass of PlotlyAggregatorParser that times the execution of the aggregation methods.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timing = {}

    def process_downsampling(
        self,
        hf_trace_data: dict,
        hf_x: np.ndarray,
        hf_y: np.ndarray,
        hf_x_parsed: np.ndarray,
        hf_y_parsed: np.ndarray,
        start_idx: int,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Process downsampling for the given trace data.
        """
        start_time = time.time()
        result = super().process_downsampling(
            hf_trace_data, hf_x, hf_y, hf_x_parsed, hf_y_parsed, start_idx
        )
        end_time = time.time()
        self.timing["process_downsampling"] = end_time - start_time
        return result