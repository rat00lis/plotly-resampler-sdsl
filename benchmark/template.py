from benchmark.exp_runner import setup_experiment, run_with_timing
from data_structures import input_tools

exp_name = "downsampling_comparison"
exp = setup_experiment(exp_name)

@exp.automain
def run(cases, iterations, n_range, file_input_list, decimal_places):
    input_tools_instance = input_tools.InputTools()

    def experiment_fn(x, y, option):
        return

    results = run_with_timing(input_tools_instance, experiment_fn, cases, n_range, file_input_list, decimal_places, iterations)
    exp.log_scalar("num_cases", len(results))
    return results
