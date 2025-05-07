import sdsl4py
import numpy as np
import data_structures.compressed_vector as compressed_vector
import csv

class InputTools:
    def __init__(self):
        self.valid_input_types = ["default", "sdsl4py"]
    
    def get(self, input_type="default", option="normal", size=10000000):
        """
            Get the inputs for the benchmark based on the input type and save them in input_cases.
        """

        if input_type not in self.valid_input_types:
            raise Exception(f"Invalid input type: {input_type}. Valid types are: {self.valid_input_types}")

        sdsl4py_or_normal = "normal" if option != "sdsl4py" else "sdsl4py"

        match input_type:
            case "default":
                x, vector = self.get_default(sdsl4py_or_normal, size)
                return x, vector
            
            
    @staticmethod
    def get_default(option, size):
        """
            Placeholder, returns a predeterminated vector
        """
        x = np.linspace(0, 4 * np.pi, size)
        y = np.sin(x) + np.random.normal(0, 0.1, len(x))

        match option:
            case "sdsl4py":
                default_vector = compressed_vector.CompressedVector()
                default_vector.build_from_vector(y,decimal_places=4)
                return x,default_vector
            
            case "normal":
                return x,y

    def get_from_file(self, file_path, option, decimal_places=4, delimiter=";", column=1, truncate=None):
        """
            Get the inputs for the benchmark based on the input type and save them in input_cases.
        """
        # get x, from row 0 and y from column 'column'
        x = []
        y = []
        line_count = 0
        if truncate is not None:
            with open(file_path, 'r') as file:
                total_lines = sum(1 for line in file if line.strip())
                if truncate > total_lines:
                    print(f"Warning: Truncate value ({truncate}) is larger than the file length ({total_lines})")
        match option:
            case "default":
                with open(file_path, 'r') as file:
                    reader = csv.reader(file, delimiter=delimiter)
                    for row in reader:
                        if not row:  # Skip empty rows
                            continue
                        if truncate is not None and line_count >= truncate:
                            break
                        try:
                            x.append(float(row[0]))
                            y.append(float(row[column]))
                        except IndexError:
                            print(f"IndexError: Check the delimiter '{delimiter}' or the file structure.")
                            raise
                        line_count += 1
                return np.array(x), np.array(y)
            
            case "sdsl4py":
                with open(file_path, 'r') as file:
                    reader = csv.reader(file, delimiter=delimiter)
                    for row in reader:
                        if not row:  # Skip empty rows
                            continue
                        if truncate is not None and line_count >= truncate:
                            break
                        try:
                            x.append(float(row[0]))
                        except IndexError:
                            print(f"IndexError: Check the delimiter '{delimiter}' or the file structure.")
                            raise
                        line_count += 1

                y = compressed_vector.CompressedVector()
                try:
                    y.build_from_file(file_path, column=column, decimal_places=decimal_places, delimiter=delimiter, truncate=truncate)
                except IndexError:
                    print(f"IndexError: Check the delimiter '{delimiter}' or the file structure.")
                    raise
                return np.array(x), y
        raise Exception(f"Invalid option: {option}. Valid options are: default, sdsl4py")