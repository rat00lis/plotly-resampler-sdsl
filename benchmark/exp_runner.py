import statistics
from data_structures import input_tools
from sacred import Experiment
from sacred.observers import FileStorageObserver
from benchmark.config import add_base_config, ROOT_OUTPUT_FOLDER

def setup_experiment(exp_name, config_overrides=None):
    exp = Experiment(exp_name)
    exp.observers.append(FileStorageObserver.create(ROOT_OUTPUT_FOLDER + "/" + exp_name))
    add_base_config(exp)

    @exp.config
    def default_config():
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
    return exp

def run_with_timing(input_tools_instance, experiment_fn, cases, n_range, file_input_list, decimal_places, iterations):
    results = {}

    for file_input in file_input_list:
        for n_size in n_range:
            for case in cases:
                option = case["option"]
                input_type = case["input_type"]
                x, y = input_tools_instance.get_from_file(
                    file_input, input_type, decimal_places, truncate=n_size
                )
                if len(x) != len(y):
                    raise ValueError(
                        f"Length mismatch! {option=}, {file_input=}, {n_size=}, len(x)={len(x)}, len(y)={len(y)}"
                    )

                timings = []
                for _ in range(iterations):
                    timings.append(experiment_fn(x, y, option))

                clean_file_input = file_input.split("/")[-1].split(".")[0]
                key = f"{clean_file_input}_{n_size}_{option}"

                results[key] = {
                    "option": option,
                    "file:": clean_file_input,
                    "n_size": n_size,
                    "mean": statistics.mean(timings),
                    "stdev": statistics.stdev(timings) if len(timings) > 1 else 0,
                    "min": min(timings),
                    "max": max(timings),
                    "all_times": timings,
                    "iterations": iterations
                }
    return results
