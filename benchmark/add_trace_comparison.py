import time
from benchmark.exp_runner import setup_experiment, run_with_timing
from data_structures import input_tools
from plotly_resampler.figure_resampler.figurewidget_resampler import FigureWidgetResampler
import plotly.graph_objects as go

exp_name = "downsampling_comparison"
exp = setup_experiment(exp_name)

@exp.automain
def run(cases, iterations, n_range, file_input_list, decimal_places):
    input_tools_instance = input_tools.InputTools()

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

    results = run_with_timing(input_tools_instance, experiment_fn, cases, n_range, file_input_list, decimal_places, iterations)
    exp.log_scalar("num_cases", len(results))
    return results
