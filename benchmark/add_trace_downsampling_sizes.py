import statistics
import time
import os
import gc  # For memory cleanup

import plotly.graph_objects as go
from plotly_resampler.figure_resampler.figurewidget_resampler import FigureWidgetResampler

from benchmark.exp_runner import setup_experiment
from benchmark.input_handler import InputHandler

def run_with_timing(input_handler_instance, experiment_fn, cases, file_input_list, decimal_places, iterations, width, downsampling_percentage_range, n_size=300000):
    results = {}

    for file_input in file_input_list:
        for i, downsampling_percentage in enumerate(downsampling_percentage_range):
            for case in cases:
                option = case["option"]
                input_type = case["input_type"]
                input_handler_instance.set_width(width, "y")
                x, y = input_handler_instance.get_from_file(
                    file_path=file_input,
                    option=input_type,
                    decimal_places=decimal_places,
                    delimiter=";",
                    column=1,
                    truncate=n_size
                )

                if len(x) != len(y):
                    raise ValueError(
                        f"Length mismatch! {option=}, {file_input=}, {n_size=}, len(x)={len(x)}, len(y)={len(y)}"
                    )

                timings = []
                for _ in range(iterations):
                    timings.append(experiment_fn(x, y, option, downsampling_percentage))


                clean_file_input = file_input.split("/")[-1].split(".")[0]
                key = f"{clean_file_input}_{n_size}_{option}_{downsampling_percentage}"

                results[key] = {
                    "option": option,
                    "file:": clean_file_input,
                    "downsampling_size": int(downsampling_percentage * len(x) / 100),
                    "mean": statistics.mean(timings),
                    "stdev": statistics.stdev(timings) if len(timings) > 1 else 0,
                    "min": min(timings),
                    "max": max(timings),
                    "all_times": timings,
                    "iterations": iterations
                }
                   # Free memory
                del x
                del y
                gc.collect()
    return results

exp_name = "add_trace_downsampling_sizes"
exp = setup_experiment(exp_name)

@exp.config
def default_config():
    cases = [
        {
            "option": "plotly_resampler",
            "input_type": "default",
        }
    ]
    n_size = 300000
    downsampling_percentage_range = [0.05, 0.1, 3, 8, 15, 20]
    generate_figures = True

@exp.automain
def run(cases, iterations, n_size, file_input_list, decimal_places, width, downsampling_percentage_range, generate_figures):
    input_handler_instance = InputHandler()

    def experiment_fn(x, y, option, downsampling_percentage):
        downsampling_size = int(downsampling_percentage * len(x) / 100)

        figure = FigureWidgetResampler(go.Figure())
        start = time.perf_counter()
        figure.add_trace(go.Scattergl(name=option, showlegend=True), hf_x=x, hf_y=y, max_n_samples=downsampling_size)
        end = time.perf_counter()
        result_time = end - start

        if generate_figures:
            output_dir = "benchmark/output/figures"
            os.makedirs(output_dir, exist_ok=True)
            output_file = f"{output_dir}/{exp_name}_{downsampling_size}_{downsampling_percentage}.html"
            if not os.path.exists(output_file):
                figure.write_html(output_file)

        del figure
        gc.collect()

        return result_time

    results = run_with_timing(
        input_handler_instance=input_handler_instance,
        experiment_fn=experiment_fn,
        cases=cases,
        file_input_list=file_input_list,
        decimal_places=decimal_places,
        iterations=iterations,
        width=width,
        downsampling_percentage_range=downsampling_percentage_range,
        n_size=n_size
    )

    return results
