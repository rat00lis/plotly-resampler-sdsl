from data_structures import input_tools
import time
from .  import time_experiments as exp
import csv

class TimeExperimentsRunner:
    def __init__(self, iterations=10):
        self.input_tools = input_tools.InputTools()
        self.iterations = iterations
        self.input_cases = ["sdsl4py", "plotly_resampler", "plotly"]
        self.output_folder = "./benchmark/output/"
        self.output_csv_name = self.output_folder + "benchmark_results.csv"
        self.n_range = [100, 1000, 10000]

    def generate_csv_output_filename(self, prefix="", suffix=""):
        """
        Generate a CSV filename based on the timestamp, optional prefix, and optional suffix
        """
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        prefix_part = f"{prefix}_" if prefix else ""
        suffix_part = f"_{suffix}" if suffix else ""
        self.output_csv_name = f"{self.output_folder}{prefix_part}{timestamp}{suffix_part}_benchmark_results.csv"

    def get_input(self, input_type, option, size):
        """
        Get the input for the benchmark based on the input type
        """
        return self.input_tools.get(input_type, option, size)

    def run_experiment_iteration(self, experiment_function, n_size):
        """
        Run the experiment function and measure its execution time.
        """
        results = [n_size]

        for case in self.input_cases:
            start_time = time.perf_counter()
            given_time_by_function = None
            for i in range(self.iterations):
                x, vector = self.get_input("default", case, n_size)
                given_time_by_function = experiment_function(x, vector, case)
    
            end_time = time.perf_counter()
            execution_time = given_time_by_function if given_time_by_function is not None else (end_time - start_time)
            results.append(execution_time / self.iterations)
    
        # Write the results to the CSV file
        self.write_in_csv(results)

    def write_in_csv(self, line):
        """
        Write the results in a csv file.
        """
        formatted_line = [f"{x:.10f}" if isinstance(x, float) else x for x in line]
        with open(self.output_csv_name, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(formatted_line)


    def run_experiment(self, experiment_function):
        # Write the header to the CSV file
        header = ["n_size"] + self.input_cases
        self.write_in_csv(header)
        
        for n_size in self.n_range:
            self.run_experiment_iteration(experiment_function, n_size)
