import time
from benchmark.exp_runner import setup_experiment, run_with_timing
from benchmark.input_handler import InputHandler
from plotly_resampler.figure_resampler.figurewidget_resampler import FigureWidgetResampler
import os
import plotly.graph_objects as go

exp_name = "add_trace_resampler"
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
    downsampling_size = 1000
    generate_figures = False

@exp.automain
def run(cases, iterations, n_range, file_input_list, decimal_places, width, downsampling_size, generate_figures):
    input_handler_instance = InputHandler()

    def experiment_fn(x, y, option):
        figure = FigureWidgetResampler(go.Figure())
        start = time.perf_counter()
        figure.add_trace(go.Scattergl(name=option, showlegend=True), hf_x=x, hf_y=y, max_n_samples=downsampling_size)
        end = time.perf_counter()
        result_time = end - start
        
        # Create output directory if it doesn't exist
        output_dir = "benchmark/output/figures"
        os.makedirs(output_dir, exist_ok=True)
        
        if generate_figures:
            output_file = f"{output_dir}/{exp_name}_{downsampling_size}_{len(x)}.html"
            if not os.path.exists(output_file):
                figure.write_html(output_file)
        
        del figure
        return result_time


    results = run_with_timing(input_handler_instance, experiment_fn, cases, n_range, file_input_list, decimal_places, iterations, width, decompressed)
    # exp.log_scalar("num_cases", len(results))
    return results


