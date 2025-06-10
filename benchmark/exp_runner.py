import statistics
from benchmark.input_handler import InputHandler
from sacred import Experiment
from sacred.observers import FileStorageObserver
from benchmark.config import add_base_config, ROOT_OUTPUT_FOLDER
from data_structures.compressed_vector import CompressedVector
def setup_experiment(exp_name, config_overrides=None):
    exp = Experiment(exp_name)
    exp.observers.append(FileStorageObserver.create(ROOT_OUTPUT_FOLDER + "/" + exp_name))
    add_base_config(exp)
    return exp

def run_with_timing(input_handler_instance, experiment_fn, cases, n_range, file_input_list, decimal_places, iterations, width, decompressed):
    results = {}

    for file_input in file_input_list:
        for n_size in n_range:
            for case in cases:
                option = case["option"]
                input_type = case["input_type"]
                input_handler_instance.set_width(width, "y")
                x, y = input_handler_instance.get_from_file(
                    file_path = file_input,
                    option = input_type,
                    decimal_places= decimal_places,
                    delimiter=";", 
                    column=1, 
                    truncate= n_size
                )
                if len(x) != len(y):
                    raise ValueError(
                        f"Length mismatch! {option=}, {file_input=}, {n_size=}, len(x)={len(x)}, len(y)={len(y)}"
                    )

                timings = []
                for _ in range(iterations):
                    timings.append(experiment_fn(x, y, option))
                if isinstance(x, CompressedVector):
                    x.destroy()
                else:
                    x = None
                if isinstance(y, CompressedVector):
                    y.destroy()
                else:
                    y = None
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

def run_with_memory(input_handler_instance, experiment_fn, cases, n_range, file_input_list, decimal_places, iterations, width, decompressed):
    results = {}

    for file_input in file_input_list:
        for n_size in n_range:
            for case in cases:
                option = case["option"]
                input_type = case["input_type"]
                x, y = input_handler_instance.get_from_file(
                    file_path = file_input,
                    option = input_type,
                    decimal_places= decimal_places,
                    delimiter=";", 
                    column=1, 
                    truncate= n_size,
                    decompressed=decompressed
                )
                if len(x) != len(y):
                    raise ValueError(
                        f"Length mismatch! {option=}, {file_input=}, {n_size=}, len(x)={len(x)}, len(y)={len(y)}"
                    )

                mem_usages = []
                for _ in range(iterations):
                    mem_usages.append(experiment_fn(x, y, option))

                clean_file_input = file_input.split("/")[-1].split(".")[0]
                key = f"{clean_file_input}_{n_size}_{option}"

                results[key] = {
                    "option": option,
                    "file:": clean_file_input,
                    "n_size": n_size,
                    "mean": statistics.mean(mem_usages),
                    "stdev": statistics.stdev(mem_usages) if len(mem_usages) > 1 else 0,
                    "min": min(mem_usages),
                    "max": max(mem_usages),
                    "all_times": mem_usages,
                    "iterations": iterations
                }
    return results