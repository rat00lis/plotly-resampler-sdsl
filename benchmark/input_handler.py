import sdsl4py
import numpy as np
import data_structures.compressed_vector as compressed_vector
import csv

class InputHandler:
    def __init__(self):
        self.valid_input_types = ["default", "sdsl4py"]
        self.width_y = 64
        self.width_x = 64

    def set_width(self, width, axis="x"):
        """
            Set the width of the integer part in bits.
            Args:
                width (int): The width of the integer part in bits. Only 8, 16, 32, or 64 are valid.
                axis (str): The axis to set the width for. Can be "x" or "y".
        """
        if axis == "x":
            if width in [8, 16, 32, 64]:
                self.width_x = width
            else:
                raise ValueError(f"Invalid width for x: {width}. Valid widths are: 8, 16, 32, 64")
        elif axis == "y":
            if width in [8, 16, 32, 64]:
                self.width_y = width
            else:
                raise ValueError(f"Invalid width for y: {width}. Valid widths are: 8, 16, 32, 64")
        else:
            raise ValueError(f"Invalid axis: {axis}. Valid axes are: x, y")
        
    def get_from_file(
            self, 
            file_path, 
            option, 
            decimal_places=4, 
            delimiter=";", 
            column=1, 
            truncate=None
        ):
        """
            Get the inputs for the benchmark based on the input type and save them in input_cases.
            Args:
                file_path (str): The path to the file containing the original vector.
                option (str): The input type. Can be "default" or "sdsl4py".
                decimal_places (int): The number of decimal places to use for the compressed vector.
                delimiter (str): The delimiter used in the csv file.
                column (int): The column index (0-based) to extract the vector from.
                truncate (int): The maximum number of rows to process. If None, process all rows.
        """
        # get x, from row 0 and y from column 'column'
        x = []
        y = []
        with open(file_path, 'r') as file:
            reader = csv.reader(file, delimiter=delimiter)
            for i, row in enumerate(reader):
                if truncate is not None and i >= truncate:
                    break
                if len(row) > column:
                    x.append(float(row[0]))
                    y.append(float(row[column]))
        
        if option == "default":
            # return the x and y vectors
            return x, y
        
        elif option == "sdsl4py":
            # create the compressed vector
            compressed_vector_instance_x = compressed_vector.CompressedVector(decimal_places, self.width_x)
            compressed_vector_instance_x.create_vector(len(x))
            compressed_vector_instance_x.fill_from_vector(x)
            compressed_vector_instance_y = compressed_vector.CompressedVector(decimal_places, self.width_y)
            compressed_vector_instance_y.create_vector(len(y))
            compressed_vector_instance_y.fill_from_vector(y)
            # return the compressed vector
            return compressed_vector_instance_x, compressed_vector_instance_y
        else:
            raise ValueError(f"Invalid option: {option}. Valid options are: {self.valid_input_types}")