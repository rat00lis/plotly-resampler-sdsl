import sdsl4py
import math

class CompressedVector:
    def __init__(self):
        self.n_elements = 0
        self.integer_part = None
        self.decimal_part = None
        self.current = 0
        self.decimal_places = None
        self.sign_part = None
        self.int_part_structure = None
        self.dec_part_structure = None

    def __iter__(self):
        self.current = 0  # Reset the current index for iteration
        return self
    
    def __next__(self):
        if self.current < self.n_elements:
            value = self._reconstruct_float_value(self.current)
            self.current += 1
            return value
        raise StopIteration
    
    def _build_compressed_vector(self, original_vector):
        """
        Build the compressed vector from the original vector.
        """
        self._create_vectors(original_vector)
        self._fill_vectors(original_vector)


    def _fill_vectors(self, original_vector):
        """
        Fill the integer and decimal vectors with the values from the original vector.
        """
        for i in range(self.n_elements):
            value = abs(original_vector[i])  # Ensure we are working with the absolute value
            
            # Convert to decimal string format without scientific notation
            str_value = f"{value:.{self.decimal_width}f}"
            
            # Split into integer and decimal parts
            int_part, dec_part = str_value.split(".") if "." in str_value else (str_value, "0")
            
            # Store the integer part
            self.integer_part[i] = int(int_part)
    
            # Handle the decimal part: pad or truncate to match decimal_width
            dec_part = dec_part.ljust(self.decimal_width, "0")[:self.decimal_width]
            self.decimal_part[i] = int(dec_part)
    
            # Store the sign part
            self.sign_part[i] = 1 if original_vector[i] >= 0 else 0
        
        if self.int_part_structure is not None:
            self.integer_part = self.int_part_structure(self.integer_part)
        else:
            self.integer_part = self.integer_part
        if self.dec_part_structure is not None:
            self.decimal_part = self.dec_part_structure(self.decimal_part)
        else:
            self.decimal_part = self.decimal_part


    def _create_vectors(self, original_vector):
        # Determine decimal width
        if self.decimal_places is None:
            # Convert to string without scientific notation
            str_values = [f"{abs(x):.50f}" for x in original_vector]
            max_decimal_places = max(len(s.split(".")[1]) if "." in s else 0 for s in str_values)
            max_decimal_places = min(max_decimal_places, 50)  # Reasonable upper limit
        else:
            max_decimal_places = self.decimal_places
        
        # decimal width
        self.decimal_width = max_decimal_places
         # Calculate int_width for the integer part using absolute values
        max_abs_value = max(abs(x) for x in original_vector)
        int_width = max(1, math.ceil(math.log2(int(max_abs_value) + 1)))

        # Create integer part vector
        self.integer_part = sdsl4py.int_vector(size=self.n_elements, default_value=0, int_width=int_width)

        # Calculate int_width for the decimal part
        decimal_int_width = math.ceil(math.log2(10 ** max_decimal_places))
        self.decimal_part = sdsl4py.int_vector(size=self.n_elements, default_value=0, int_width=decimal_int_width)

        # Sign part
        self.sign_part = sdsl4py.bit_vector(size=self.n_elements, default_value=0)

    # Helper function to get the reconstructed value as a float
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
            + self.decimal_part[index] / (10 ** self.decimal_width)  # decimal part
        )
        return value if self.sign_part[index] == 1 else -value  # sign part
    
    
    def __len__(self):
        """
        Return the number of elements in the compressed vector.
        """
        return self.n_elements
    
    def __getitem__(self, index):
        """
        Return the value at the given index.
        """
        # Handle get the value at the specified index
        if isinstance(index, int):
            if index < 0 or index >= self.n_elements:  # Check for out of range
                raise IndexError("Index out of range")
            return self._reconstruct_float_value(index)

        # Handle slicing
        elif isinstance(index, slice):
            start, stop, step = index.indices(self.n_elements)
            return [self._reconstruct_float_value(i) for i in range(start, stop, step)]

        else:
            raise TypeError("Invalid index type")
        
    def set_int_part_structure(self, int_part_structure):
        """
        Set the structure for the integer part vector.
        Args:
            int_part_structure (function): The function to use for the integer part vector.
        """
        self.int_part_structure = int_part_structure

    def set_dec_part_structure(self, dec_part_structure):
        """
        Set the structure for the decimal part vector.
        Args:
            dec_part_structure (function): The function to use for the decimal part vector.
        """
        self.dec_part_structure = dec_part_structure
    
    def build_from_vector(self, original_vector, decimal_places=4):
        """
        Build the compressed vector from a vector.
        Args:
            original_vector (list): The original vector to compress.
            data_structure (str): The data structure to use for compression.
            decimal_places (int): The number of decimal places to keep.
        """
        self.n_elements = len(original_vector)
        self.decimal_places = decimal_places
        self._build_compressed_vector(original_vector)

    def build_from_file(self, file_path, column=1, decimal_places=4, delimiter=";", truncate=None):
        """
        Build the compressed vector from a specific column in a csv file.
        Args:
            file_path (str): The path to the file containing the original vector.
            column (int): The column index (0-based) to extract the vector from.
            data_structure (str): The data structure to use for compression.
            decimal_places (int): The number of decimal places to keep.
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
                    try:
                        original_vector.append(float(values[column]))
                    except ValueError:
                        pass
            self.n_elements = len(original_vector)
            self.decimal_places = decimal_places
            self._build_compressed_vector(original_vector)
    
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
                + self.decimal_width.__sizeof__()
                + self.current.__sizeof__()
                )
        return total
    