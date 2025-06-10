NUM_ITERATIONS = 1
ROOT_OUTPUT_FOLDER = "./benchmark/output/"
N_RANGE = range(1001, 5001, 1000)
DECIMAL_PLACES = 4
DELIMITER = ";"
COLUMN = 1
DECOMPRESSED = False  # Whether to use compressed vectors
WIDTH = 16  # 16 bits can represent numbers from 0 to 65535, enough for 4-digit numbers
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
        "width": WIDTH,
        "decompressed": DECOMPRESSED
    })

