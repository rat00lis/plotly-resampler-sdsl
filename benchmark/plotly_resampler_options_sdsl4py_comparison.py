"""
Constructing traces with **very large data amounts** really takes some time.
            To speed this up; use this [`add_trace`][figure_resampler.figure_resampler_interface.AbstractFigureAggregator.add_trace] method and

            1. Create a trace with no data (empty lists)
            2. pass the high frequency data to this method using the ``hf_x`` and ``hf_y``
               parameters.
"""

from benchmark.exp_runner import setup_experiment, run_with_timing
from benchmark.input_handler import InputHandler
from plotly_resampler import FigureResampler, FigureWidgetResampler
import plotly.graph_objects as go
import time
exp_name = "plotly_resampler_options_sdsl4py_comparison"
exp = setup_experiment(exp_name)
# Override default config
@exp.config
def default_config():
    cases = [
        {
            "option": "widget",
            "input_type": "sdsl4py",
        },
        {
            "option": "resampler",
            "input_type": "sdsl4py",
        }
    ]
@exp.automain
def run(cases, iterations, n_range, file_input_list, decimal_places, width):
    input_handler_instance = InputHandler()

    def experiment_fn(x, y, option):
        if option == "widget":
            fig_widget = FigureWidgetResampler(go.Figure())
            start = time.perf_counter()
            fig_widget.add_trace(go.Scattergl(name=option, showlegend=True), hf_x=x, hf_y=y)
            end = time.perf_counter()
            diff = end - start
            del fig_widget
            return diff
        elif option == "resampler":
            fig_resampler = FigureResampler(go.Figure())
            start = time.perf_counter()
            fig_resampler.add_trace(go.Scattergl(name=option, showlegend=True), hf_x=x, hf_y=y)
            end = time.perf_counter()
            diff = end - start
            del fig_resampler
            return diff
        raise ValueError(f"Unknown option: {option}")

    results = run_with_timing(input_handler_instance, experiment_fn, cases, n_range, file_input_list, decimal_places, iterations, width)
    # exp.log_scalar("num_cases", len(results))
    return results

