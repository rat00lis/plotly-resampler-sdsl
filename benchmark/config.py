NUM_ITERATIONS = 30
ROOT_OUTPUT_FOLDER = "./benchmark/output/"
N_RANGE = range(10000, 35000, 10000)
DECIMAL_PLACES = 4
DELIMITER = ";"
COLUMN = 1
FILE_INPUT_LIST = [
    # "input/dataset_bridge/d_08_1_1_1.txt",
    # "input/dataset_bridge/d_08_1_1_2.txt",
    # "input/dataset_bridge/d_08_1_1_3.txt",
    # "input/dataset_bridge/d_08_1_1_4.txt",
    # "input/dataset_bridge/d_08_1_1_5.txt",
    # "input/dataset_bridge/d_08_1_1_6.txt",
    # "input/dataset_bridge/d_08_1_1_7.txt",
    # "input/dataset_bridge/d_08_1_1_8.txt",
    # "input/dataset_bridge/d_08_1_1_9.txt",
    "input/dataset_bridge/d_08_1_1_10.txt"
]

def add_base_config(exp):
    """
    Add the base configuration for the experiment.
    """
    exp.add_config({
        "iterations": NUM_ITERATIONS,
        "n_range": N_RANGE,
        "output_folder": ROOT_OUTPUT_FOLDER,
        "decimal_places": DECIMAL_PLACES,
        "delimiter": DELIMITER,
        "column": COLUMN,
        "file_input_list": FILE_INPUT_LIST,
    })