from benchmark.exp_runner import setup_experiment, run_with_timing
from benchmark.input_handler import InputHandler
import time
import plotly.graph_objects as go
exp_name = "add_trace_plotly"
exp = setup_experiment(exp_name)

# Override default config
@exp.config
def default_config():
    cases = [
        {
            "option": "plotly_resampler",
            "input_type": "default",
        }
    ]

@exp.automain
def run(cases, iterations, n_range, file_input_list, decimal_places, width, decompressed):
    input_handler_instance = InputHandler()

    def experiment_fn(x, y, option):
        figure = go.Figure()
        start = time.perf_counter()
        figure.add_trace(go.Scattergl(x=x, y=y, name=option, showlegend=True))
        end = time.perf_counter()
        del figure
        return end - start

    results = run_with_timing(input_handler_instance, experiment_fn, cases, n_range, file_input_list, decimal_places, iterations, width, decompressed)
    exp.log_scalar("num_cases", len(results))
    return results
