from . import time_experiments_runner
from . import time_experiments
from . import size_experiments_runner
from . import size_experiments
from data_structures import input_tools

TIME_EXP = {}
TIME = time_experiments_runner.TimeExperimentsRunner()
# SIZE_EXP = {}
# SIZE = size_experiments_runner.SizeExperimentsRunner()
INPUT = input_tools.InputTools()

def get_all_experiments():
    """
    Get all the experiments to run by inspecting the imported modules.
    """
    #get all the functions in the time_experiments module
    time_experiments_functions = [func for func in dir(time_experiments) if callable(getattr(time_experiments, func)) and not func.startswith("_")]
    TIME_EXP = {func: getattr(time_experiments, func) for func in time_experiments_functions}


def run_all_time_experiments():
    """
    Run all the time experiments and save the results in a csv file.
    """
    for experiment in TIME_EXP:
        print(f"Running experiment: {experiment}")
        TIME.generate_csv_output_filename(prefix="time", suffix=experiment)
        TIME.run_experiment(TIME_EXP[experiment])