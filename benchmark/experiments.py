from plotly_resampler import FigureResampler, FigureWidgetResampler
import plotly.graph_objects as go
from benchmark.timed_process_downsampling import patch_process_downsampling, ElapsedTime
from . import input_tools
import time
import csv

class Experiments:
    def __init__(self, iterations=10):
        self.input_tools = input_tools.InputTools()
        self.iterations = iterations
        self.input_cases = ["sdsl4py", "plotly_resampler", "plotly"]
        self.output_folder = "./benchmark/output/"
        self.output_csv_name = self.output_folder + "benchmark_results.csv"
        self.n_range = [100, 1000, 10000]

    def generate_csv_output_filename(self):
        """
        Generate a CSV filename based on the timestamp
        """
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.output_csv_name = f"{self.output_folder}{timestamp}_benchmark_results.csv"

    def get_input(self, input_type, option, size):
        """
        Get the input for the benchmark based on the input type
        """
        return self.input_tools.get(input_type, option, size)

    def compare_add_trace(self, x, y, option):
        if option == "plotly":
            figure = go.Figure()
            figure.add_trace(go.Scattergl(x=x, y=y, name=option, showlegend=True))
            # destroy the figure to free memory
            del figure
        else:
            figure = FigureWidgetResampler(go.Figure())
            figure.add_trace(go.Scattergl(name=option, showlegend=True), hf_x=x, hf_y=y)
            # destroy the figure to free memory
            del figure

    def compare_downsampling(self, x, y, option):
        ElapsedTime.elapsed_time = None
        with patch_process_downsampling():
            figure = FigureResampler(go.Figure())
            figure.add_trace(go.Scattergl(name=option, showlegend=True), hf_x=x, hf_y=y)
            del figure
        return ElapsedTime.elapsed_time
        
    def write_in_csv(self, line):
        """
        Write the results in a csv file.
        """
        with open(self.output_csv_name, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(line)

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

    def run_experiment(self, experiment_function):
        # Write the header to the CSV file
        header = ["n_size"] + self.input_cases
        self.write_in_csv(header)
        
        for n_size in self.n_range:
            self.run_experiment_iteration(experiment_function, n_size)

#test run
tests_to_run = [
    "compare_add_trace",
    "compare_downsampling"
]

benchmark_tool = Benchmark()
benchmark_tool.generate_csv_output_filename()

for test in tests_to_run:
    print(f"Running {test}...")
    cases_len = len(benchmark_tool.input_cases)
    section = test
    for i in range(cases_len):
        section += "," + "___"
    benchmark_tool.write_in_csv([section])
    benchmark_tool.run_experiment(getattr(benchmark_tool, test))
    print(f"{test} completed.")

print("All tests completed.")

# Save the results in the CSV file
print(f"Results saved in {benchmark_tool.output_csv_name}")