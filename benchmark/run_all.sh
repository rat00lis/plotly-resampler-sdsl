#!/bin/bash

# Experiment names
EXP_NAMES=(
    "downsampling_comparison"
    "add_trace_no_widget"
    "add_trace_memory_no_widget_consumption"
    # "plotly_resampler_options_comparison"
    # "plotly_resampler_options_sdsl4py_comparison"
    # "add_trace_comparison"
    # "add_trace_memory_consumption"
)

# Go to root directory
cd "$(dirname "$0")/.."

# Activate Python environment
source fork-env/bin/activate

# Max number of parallel jobs
MAX_PARALLEL_JOBS=4

# Cleanup on Ctrl+C
cleanup() {
    echo -e "\nAborting all running experiments..."
    pkill -P $$  # Kill all subprocesses of this script
    exit 1
}

trap cleanup SIGINT

# Run experiments in parallel
running_jobs=0

for exp_name in "${EXP_NAMES[@]}"; do
    echo "Running experiment: $exp_name"
    python -m benchmark."$exp_name" &

    ((running_jobs+=1))

    if (( running_jobs >= MAX_PARALLEL_JOBS )); then
        wait
        running_jobs=0
    fi
done

# Wait for any remaining jobs
wait

# Run output interpreter
echo "All experiments completed."
echo "Running output interpreter..."
python -m benchmark.output_interpreter
