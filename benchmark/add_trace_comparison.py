import time
from benchmark.exp_runner import setup_experiment, run_with_timing
from benchmark.input_handler import InputHandler
from plotly_resampler.figure_resampler.figurewidget_resampler import FigureWidgetResampler
import plotly.graph_objects as go

exp_name = "add_trace_comparison"
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
def run(cases, iterations, n_range, file_input_list, decimal_places):
    input_handler_instance = InputHandler()

    def experiment_fn(x, y, option):
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

    results = run_with_timing(input_handler_instance, experiment_fn, cases, n_range, file_input_list, decimal_places, iterations)
    # exp.log_scalar("num_cases", len(results))
    return results

