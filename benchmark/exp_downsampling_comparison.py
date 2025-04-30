from sacred import Experiment
from sacred.observers import FileStorageObserver
from benchmark.config import add_base_config, ROOT_OUTPUT_FOLDER
import statistics
from benchmark.timed_process_downsampling import patch_process_downsampling, ElapsedTime
from data_structures import input_tools
from plotly_resampler import FigureResampler
import plotly.graph_objects as go

exp_name = "downsampling_comparison"
exp = Experiment(exp_name)
exp.observers.append(FileStorageObserver.create(ROOT_OUTPUT_FOLDER + "/" + exp_name))
add_base_config(exp)

@exp.config
def config():
    """
    Configuration for the experiment.
    """
    cases = [
        {
            "option": "plotly_resampler",
            "input_type": "default",
        },
        {
            "option": "sdsl4py",
            "input_type": "sdsl4py",
        }
    ]
    n_range = [1001, 10001, 100001]

@exp.automain
def compare_downsampling(cases, iterations, n_range, file_input_list, decimal_places):
    """
    Run the downsampling comparison experiment.
    """
    results = {}
    input_tools_instance = input_tools.InputTools()
    
    for file_input in file_input_list:
        for n_size in n_range:
            for case in cases:
                option = case["option"]
                input_type = case["input_type"]
                x, y = input_tools_instance.get_from_file(file_input, input_type, decimal_places, truncate=n_size) # TODO: case here might be confusing if we change sdsl4py
                if len(x) != len(y):
                    raise ValueError(
                        f"Length mismatch! Option={option}, Input={file_input}, n={n_size}, len(x)={len(x)}, len(y)={len(y)}"
                    )
                # Run multiple iterations
                timings = []
                for _ in range(iterations):
                    ElapsedTime.elapsed_time = None
                    with patch_process_downsampling():
                        figure = FigureResampler(go.Figure())
                        figure.add_trace(go.Scattergl(name=option, showlegend=True), hf_x=x, hf_y=y)
                        del figure
                    if ElapsedTime.elapsed_time is None:
                        raise ValueError(
                            f"The n_size is too small for the benchmark. Downsampling is not being triggered \n n={n_size} <= 1000"
                        )
                    timings.append(ElapsedTime.elapsed_time)
                
                # Store results
                clean_file_input = file_input.split("/")[-1].split(".")[0]
                key = f"{clean_file_input}_{n_size}_{option}"
                results[key] = {
                    "mean": statistics.mean(timings),
                    "stdev": statistics.stdev(timings) if len(timings) > 1 else 0,
                    "min": min(timings),
                    "max": max(timings),
                    "all_times": timings
                }
    exp.log_scalar("num_cases", len(results))  # optional extra logs            
    return results

