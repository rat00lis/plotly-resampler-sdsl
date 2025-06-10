import time
import memory_profiler
from benchmark.exp_runner import setup_experiment, run_with_timing
from benchmark.input_handler import InputHandler
from plotly_resampler import FigureResampler
import plotly.graph_objects as go

exp_name = "add_trace_memory_no_widget_consumption"
exp = setup_experiment(exp_name)

# Override default config
@exp.config
def default_config():
    cases = [
        {
            "option": "plotly",
            "input_type": "default",
        },
        {
            "option": "plotly_resampler_sdsl4py",
            "input_type": "sdsl4py",
        },
        {
            "option": "plotly_resampler",
            "input_type": "default",
        }
    ]

@exp.automain
def run(cases, iterations, n_range, file_input_list, decimal_places, width, decompressed):
    input_handler_instance = InputHandler()

    def experiment_fn(x, y, option):
        # Measure memory before adding the trace
        mem_before = memory_profiler.memory_usage()[0]

        # Two different branches depending on the option:
        if option == "plotly":
            figure = go.Figure()
            figure.add_trace(go.Scattergl(x=x, y=y, name=option, showlegend=True))
        else:
            figure = FigureResampler(go.Figure())
            figure.add_trace(go.Scattergl(name=option, showlegend=True), hf_x=x, hf_y=y)

        # Measure memory after adding the trace
        mem_after = memory_profiler.memory_usage()[0]

        # Calculate the difference in memory usage
        mem_delta = mem_after - mem_before
        del figure
        # For debugging, you could also print addresses or sizes here.
        return mem_delta

    # Run the experiment using your existing experiment runner.
    results = run_with_timing(
        input_handler_instance, experiment_fn, cases, n_range, file_input_list, decimal_places, iterations, width
    )
    return results
