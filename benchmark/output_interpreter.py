import csv
import os
import json
import pandas as pd
import plotly.express as px
import argparse  # Add argparse for command-line arguments
import traceback  # For detailed error reporting

file_path_root = "benchmark/output/"
# Dynamically get all experiment names from subdirectories
try:
    exp_names = [d for d in os.listdir(file_path_root) if os.path.isdir(os.path.join(file_path_root, d))]
    print(f"Found experiments: {exp_names}")
except FileNotFoundError:
    print(f"Error: Directory {file_path_root} not found")
    exp_names = []
except Exception as e:
    print(f"Error retrieving experiment names: {e}")
    exp_names = []

def process_all_experiments_output(file_path_root=file_path_root, exp_names=exp_names):
    for exp_name in exp_names:
        try:
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
                try:
                    data = get_json_from_file(file_path)
                    if data is None:
                        print(f"Failed to parse JSON data from {file_path}")
                        continue
                        
                    metadata, result = get_values_from_json(data)
                    if result is None:
                        print(f"Failed to extract result data from {file_path}")
                        continue
                        
                    exp_results = get_exp_results(result)
                    if not exp_results:
                        print(f"No experiment results extracted from {file_path}")
                        continue
                        
                    csv_path = os.path.join(exp_dir, latest_folder, "csv_results.csv")
                    export_results_to_csv(exp_results, csv_path)
                    
                    plot_path = os.path.join(exp_dir, latest_folder, "plot.png")
                    plot_experiment_results(exp_results, exp_name, plot_path)
                    
                    print(f"Successfully processed {exp_name}")
                except Exception as e:
                    print(f"Error processing experiment {exp_name}: {e}")
                    traceback.print_exc()
            else:
                print(f"File {file_path} does not exist.")
        except Exception as e:
            print(f"Unexpected error processing experiment {exp_name}: {e}")
            traceback.print_exc()

def get_json_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from {file_path}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error reading {file_path}: {e}")
        traceback.print_exc()
        return None

def get_values_from_json(json_data):
    try:
        if json_data is None:
            return {}, None
            
        metadata = json_data.get("meta", {})
        result = json_data.get("result", None)
        if result is None:
            print("Warning: 'result' key not found in JSON data")
        return metadata, result
    except Exception as e:
        print(f"Error extracting values from JSON: {e}")
        traceback.print_exc()
        return {}, None

def get_exp_n_range(json_result):
    try:
        if json_result is None:
            return []
            
        n_range = []
        for experiment, experiment_values in json_result.items():
            n_size = experiment_values.get('n_size')
            if n_size not in n_range:
                n_range.append(n_size)
        return n_range
    except Exception as e:
        print(f"Error getting experiment range: {e}")
        traceback.print_exc()
        return []

def get_exp_results(json_result):
    try:
        if json_result is None:
            print("Warning: Received None instead of JSON result data")
            return {}
            
        results_dict = {}

        for experiment, experiment_values in json_result.items():
            try:
                option = experiment_values.get('option')
                mean = experiment_values.get('mean')
                n_size = experiment_values.get('n_size')
                stdev = experiment_values.get('stdev')

                # Skip entries with missing required values
                if None in [option, n_size]:
                    print(f"Warning: Skipping experiment with missing option or n_size: {experiment}")
                    continue

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
            except Exception as e:
                print(f"Error processing experiment {experiment}: {e}")
                continue
        
        # Sort the dictionary by n_size
        results_dict = dict(sorted(results_dict.items(), key=lambda item: item[0]))
        return results_dict
    except Exception as e:
        print(f"Error getting experiment results: {e}")
        traceback.print_exc()
        return {}
        
def export_results_to_csv(results_dict, output_file):
    try:
        if not results_dict:
            print(f"Warning: No results to export to {output_file}")
            return
            
        # Collect all experiment options across all n_size entries
        experiment_options = set()
        for values in results_dict.values():
            for option in values.keys():
                experiment_options.add(option)
        # Sort options for consistent column ordering
        experiment_options = sorted(experiment_options)

        # Create header: starting with n_size, then each option's mean and stdev columns
        fieldnames = ['n_size'] + [f"{option}_mean" for option in experiment_options] + [f"{option}_stdev" for option in experiment_options]

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
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
        print(f"Results exported to {output_file}")
    except Exception as e:
        print(f"Error exporting results to CSV {output_file}: {e}")
        traceback.print_exc()

def plot_experiment_results(results_dict, exp_name, file_path, include_stdev=False):
    try:
        if not results_dict:
            print(f"Warning: No results to plot for {exp_name}")
            return
            
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
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Plotting regular plot
        if include_stdev:
            fig = px.line(df, x='n_size', y='mean', color='option', error_y='stdev',
                      title=f'Experiment Results for {exp_name}',
                      labels={'n_size': 'N Size', 'mean': 'Mean Time (s)', 'option': 'Option'})
        else:
            fig = px.line(df, x='n_size', y='mean', color='option',
                      title=f'Experiment Results for {exp_name}',
                      labels={'n_size': 'N Size', 'mean': 'Mean Time (s)', 'option': 'Option'})
        
        fig.write_image(file_path)  # Save the figure as a PNG file
        
        # Plotting log plot
        log_file_path = file_path.replace('.png', '_log.png')
        if include_stdev:
            fig_log = px.line(df, x='n_size', y='mean', color='option', error_y='stdev',
                      title=f'Experiment Results for {exp_name} (Log Scale)',
                      labels={'n_size': 'N Size', 'mean': 'Mean Time (s)', 'option': 'Option'},
                      log_y=True)
        else:
            fig_log = px.line(df, x='n_size', y='mean', color='option',
                      title=f'Experiment Results for {exp_name} (Log Scale)',
                      labels={'n_size': 'N Size', 'mean': 'Mean Time (s)', 'option': 'Option'},
                      log_y=True)
        
        fig_log.write_image(log_file_path)  # Save the log plot as a PNG file
        print(f"Plots saved to {file_path} and {log_file_path}")
    except Exception as e:
        print(f"Error plotting experiment results for {exp_name}: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser(description='Process experiment results')
        parser.add_argument('-Exp', '--experiments', nargs='+', help='List of experiments to process')
        args = parser.parse_args()
        
        # If experiments are specified, use them, otherwise use all experiments
        selected_experiments = args.experiments if args.experiments else exp_names
        print(f"Processing experiments: {selected_experiments}")
        
        process_all_experiments_output(file_path_root=file_path_root, exp_names=selected_experiments)
        print("Processing complete.")
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()