import sdsl4py
import math
import numpy as np

class CompressedVector:
    def __init__(
        self,
        decimal_places=0,
        int_width=64,
        dtype=float
    ):
        """
        Initialize the CompressedVector with default values.
        Args:
            decimal_places (int): Number of decimal places to keep.
            int_width (int): Width of the integer part in bits. (default: 64)
        """
        if decimal_places < 0:
            raise ValueError("Decimal places must be non-negative")
        if decimal_places > int_width:
            raise ValueError("Decimal places cannot be greater than int_width")
        
        self.decimal_places = decimal_places
        self.int_width = int_width
        self.current = 0
        self.n_elements = 0

    def __iter__(self):
        self.current = 0  # Reset the current index for iteration
        return self
    
    def __next__(self):
        if self.current < self.n_elements:
            value = self._reconstruct_float_value(self.current)
            self.current += 1
            return value
        raise StopIteration
    
    # def __array__(self, dtype=None, copy=True):
    #     array = np.empty(self.n_elements, dtype=dtype or float)
    #     for i in range(self.n_elements):
    #         array[i] = self._reconstruct_float_value(i)
    #     return array.copy() if copy else array
    
    def __len__(self):
        """
        Return the number of elements in the compressed vector.
        """
        return self.n_elements
    
    def __getitem__(self, index):
        if isinstance(index, int):
            if index < 0 or index >= self.n_elements:
                reverse_index = self.n_elements + index
                if reverse_index < 0:
                    raise IndexError("Index out of range")
                index = reverse_index
            return self._reconstruct_float_value(index)

        # elif isinstance(index, slice):
        #     start, stop, step = index.indices(self.n_elements)
        #     sliced_values = [self._reconstruct_float_value(i) for i in range(start, stop, step)]
        #     result = CompressedVector(self.decimal_places, self.int_width, dtype=self.dtype)
        #     result.create_vector(len(sliced_values))
        #     result.fill_from_vector(sliced_values)
        #     return result

        elif isinstance(index, (list, np.ndarray)):
            # return np array
            int_arr = np.asarray(self.integer_part)
            dec_arr = np.asarray(self.decimal_part)
            sign_arr = np.asarray(self.sign_part)

            denom = 10 ** self.decimal_places
            selected = np.array(indices)

            float_arr = int_arr[selected] + dec_arr[selected] / denom
            float_arr[sign_arr[selected] == 0] *= -1
            return float_arr
        
        elif isinstance(index, slice):
            start, stop, step = index.indices(self.n_elements)
            indices = range(start, stop, step)
            int_arr = np.asarray(self.integer_part)
            dec_arr = np.asarray(self.decimal_part)
            sign_arr = np.asarray(self.sign_part)

            denom = 10 ** self.decimal_places
            selected = np.array(indices)

            float_arr = int_arr[selected] + dec_arr[selected] / denom
            float_arr[sign_arr[selected] == 0] *= -1
            return float_arr

        else:
            raise TypeError(f"Invalid index type: {type(index)}. Expected int, slice, list or ndarray.")


    def __setitem__(self, index, value):
        """
        Set the value at the given index.
        """
        # Handle set the value at the specified index
        if isinstance(index, int):
            if index < 0 or index >= self.n_elements:
                raise IndexError("Index out of range")
            
            self._insert_value(index, value)


    def _insert_value(self, index, value):
        """
        Insert a value at the specified index.
        Args:
            index (int): The index to insert the value at.
            value (float): The value to insert.
        """
        int_part = int(abs(value))
        dec_part = abs(value) - int_part
        dec_part = round(dec_part, self.decimal_places)
        dec_part = int(dec_part * (10 ** self.decimal_places))
        sign_part = 1 if value >= 0 else 0
        self.integer_part[index] = int_part
        self.decimal_part[index] = dec_part
        self.sign_part[index] = sign_part


    
    def create_vector(self, size):
        """
        Create the integer and decimal vectors.
        """
        self.n_elements = size
        match self.int_width:
            case 8:
                self._create_vector(sdsl4py.int_vector_8)
            case 16:
                self._create_vector(sdsl4py.int_vector_16)
            case 32:
                self._create_vector(sdsl4py.int_vector_32)
            case 64:
                self._create_vector(sdsl4py.int_vector_64)
            case _:
                print(f"Unsupported int_width: {self.int_width}, defaulting to 64")
                self._create_vector(sdsl4py.int_vector_64)

    
    def fill_from_vector(self, original_vector):
        """
        Build the compressed vector from a vector.
        Args:
            original_vector (list): The original vector to fill the compressed vector with.
        """
        if self.integer_part is None or self.decimal_part is None or self.sign_part is None:
            raise ValueError("Vectors not created. Call create_vector() first.")
        for value in original_vector:
            self.current += 1
            self._insert_value(self.current-1, value)
        self.n_elements = len(original_vector)
        self.current = 0

    def fill_from_file(self, file_path, column=1, delimiter=";", truncate=None):
        """
        Build the compressed vector from a specific column in a csv file.
        Args:
            file_path (str): The path to the file containing the original vector.
            column (int): The column index (0-based) to extract the vector from.
            delimiter (str): The delimiter used in the csv file.
            truncate (int): The maximum number of rows to process. If None, process all rows.
        """
        with open(file_path, 'r') as file:
            lines = file.readlines()
            original_vector = []
            for i, line in enumerate(lines):
                if truncate is not None and i >= truncate:
                    break
                values = line.strip().split(delimiter)
                if len(values) > column:
                    value_to_add = values[column]
                    try:
                        value_to_add = float(value_to_add)
                        self.current += 1
                        self._insert_value(self.current-1, value_to_add)
                    except ValueError:
                        print(f"Invalid value at line {i}: {value_to_add}")
                    
            self.n_elements = len(original_vector)
            self.current = 0
    
    def size_in_bytes(self):
        """
        Return the size in bytes of the compressed vector.
        """ 
        total = (
                # sdsl4py vectors
                sdsl4py.size_in_bytes(self.integer_part) 
                + sdsl4py.size_in_bytes(self.decimal_part)
                + sdsl4py.size_in_bytes(self.sign_part)

                # self attributes
                + self.n_elements.__sizeof__()
                + self.decimal_places.__sizeof__()
                + self.current.__sizeof__()
                )
        return total
    

    def _create_vector(self, vector_type):
        """
        Create the integer and decimal vectors with the specified type.
        """
        self.integer_part = vector_type(size=self.n_elements, default_value=0)
        self.decimal_part = vector_type(size=self.n_elements, default_value=0)
        self.sign_part = vector_type(size=self.n_elements, default_value=0)

    def _reconstruct_float_value(self, index):
        """
        Reconstructs the original float value at the given index by combining
        integer part, decimal part and sign.

        Args:
            index (int): Index of the value to reconstruct

        Returns:
            float: Reconstructed value with correct sign
        """
        value = (
            self.integer_part[index]  # integer part
            + self.decimal_part[index] / (10 ** self.decimal_places)  # decimal part
        )
        return value if self.sign_part[index] == 1 else -value  # sign part
    
    @property
    def dtype(self):
        """
        Return the data type of the compressed vector.
        """
        return np.dtype(float)
    
    @property
    def ndim(self):
        return 1

    @property
    def shape(self):
        return (self.n_elements,)
    
    @property
    def size(self):
        return self.n_elements
