from benchmark.exp_runner import setup_experiment, run_with_timing
from benchmark.timed_process_downsampling import patch_process_downsampling, ElapsedTime
from plotly_resampler import FigureResampler
from benchmark.input_handler import InputHandler
import plotly.graph_objects as go

exp_name = "downsampling_comparison"
exp = setup_experiment(exp_name)

@exp.automain
def run(cases, iterations, n_range, file_input_list, decimal_places, width):
    input_handler_instance = InputHandler()

    def experiment_fn(x, y, option):
        ElapsedTime.elapsed_time = None
        with patch_process_downsampling():
            figure = FigureResampler(go.Figure())
            figure.add_trace(go.Scattergl(name=option, showlegend=True), hf_x=x, hf_y=y)
            del figure
        return ElapsedTime.elapsed_time

    results = run_with_timing(input_handler_instance, experiment_fn, cases, n_range, file_input_list, decimal_places, iterations, width)
    # exp.log_scalar("num_cases", len(results))
    return results
