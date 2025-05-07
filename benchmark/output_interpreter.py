import csv
import os
import json
import pandas as pd
import plotly.express as px  # Use Plotly Express for plotting

file_path_root = "benchmark/output/"
exp_names =[
    "downsampling_comparison",
    "add_trace_comparison"
]

def run_all_experiments():
    for exp_name in exp_names:
        # Get the experiment directory
        exp_dir = os.path.join(file_path_root, exp_name)
        
        # Check if the directory exists
        if not os.path.exists(exp_dir):
            print(f"Directory {exp_dir} does not exist.")
            continue
        
        # Get all numbered folders and find the highest number
        subfolders = [f for f in os.listdir(exp_dir) if f.isdigit() and os.path.isdir(os.path.join(exp_dir, f))]
        if not subfolders:
            print(f"No numbered subfolders found in {exp_dir}.")
            continue
        
        # Convert to integers for proper numerical sorting, then back to string
        latest_folder = str(max(map(int, subfolders)))
        
        # Process only the latest folder
        file_path = os.path.join(exp_dir, latest_folder, "run.json")
        if os.path.exists(file_path):
            data = get_json_from_file(file_path)
            metadata, result = get_values_from_json(data)   
            exp_results = get_exp_results(result)
            export_results_to_csv(exp_results, os.path.join(exp_dir, latest_folder, "csv_results.csv"))
            plot_experiment_results(exp_results, exp_name, os.path.join(exp_dir, latest_folder, "plot.png"))
        else:
            print(f"File {file_path} does not exist.")

def get_json_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    return data

def get_values_from_json(json_data):
    metadata = json_data.get("meta", {})
    result = json_data.get("result", {})
    return metadata, result

def get_exp_n_range(json_result):
    n_range = []
    for experiment, experiment_values in json_result.items():
        n_size = experiment_values.get('n_size')
        if n_size not in n_range:
            n_range.append(n_size)
    return n_range

def get_exp_results(json_result):
    results_dict = {}

    for experiment, experiment_values in json_result.items():
        option = experiment_values.get('option')
        mean = experiment_values.get('mean')
        n_size = experiment_values.get('n_size')
        stdev = experiment_values.get('stdev')

        this_experiment = {
            option: {
                "mean": mean,
                "stdev": stdev
            }
        }
        
        if n_size in results_dict:
            results_dict[n_size].update(this_experiment)
        else:
            results_dict[n_size] = this_experiment
    
    # Sort the dictionary by n_size
    results_dict = dict(sorted(results_dict.items(), key=lambda item: item[0]))
    return results_dict
        
def export_results_to_csv(results_dict, output_file):
    # Collect all experiment options across all n_size entries
    experiment_options = set()
    for values in results_dict.values():
        for option in values.keys():
            experiment_options.add(option)
    # Sort options for consistent column ordering
    experiment_options = sorted(experiment_options)

    # Create header: starting with n_size, then each option's mean and stdev columns
    fieldnames = ['n_size'] + [f"{option}_mean" for option in experiment_options] + [f"{option}_stdev" for option in experiment_options]

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for n_size, experiments in results_dict.items():
            row = {'n_size': n_size}
            for option in experiment_options:
                if option in experiments:
                    row[f"{option}_mean"] = experiments[option].get("mean", "")
                    row[f"{option}_stdev"] = experiments[option].get("stdev", "")
                else:
                    row[f"{option}_mean"] = ""
                    row[f"{option}_stdev"] = ""
            writer.writerow(row)


def plot_experiment_results(results_dict, exp_name, file_path, include_stdev=False):
    # Convert the results dictionary to a DataFrame
    data = []
    for n_size, experiments in results_dict.items():
        for option, values in experiments.items():
            data.append({
                'n_size': n_size,
                'option': option,
                'mean': values['mean'],
                'stdev': values['stdev']
            })
    
    df = pd.DataFrame(data)
    
    # Plotting
    if include_stdev:
        fig = px.line(df, x='n_size', y='mean', color='option', error_y='stdev',
                  title=f'Experiment Results for {exp_name}',
                  labels={'n_size': 'N Size', 'mean': 'Mean Time (s)', 'option': 'Option'})
    else:
        fig = px.line(df, x='n_size', y='mean', color='option',
                  title=f'Experiment Results for {exp_name}',
                  labels={'n_size': 'N Size', 'mean': 'Mean Time (s)', 'option': 'Option'})
    
    fig.write_image(file_path)  # Save the figure as a PNG file

run_all_experiments()