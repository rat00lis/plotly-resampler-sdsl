import sdsl4py
import math

class CompressedVector:
    def __init__(self, n_elements, original_vector, data_structure='default', decimal_places=8):
        self.n_elements = n_elements
        self.integer_part = None
        self.decimal_part = None
        self.current = 0
        self.decimal_places = decimal_places
        self.sign_part = None
        self.build_compressed_vector(original_vector, data_structure)

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current < self.n_elements:
            value = self.integer_part[self.current] + self.decimal_part[self.current] / (10 ** self.decimal_width)
            value = value if self.sign_part[self.current] == 1 else -value
            self.current += 1
            return value
        raise StopIteration
    
    def build_compressed_vector(self, original_vector, data_structure='default'):
        """
        Build the compressed vector from the original vector.
        """
        self.create_vectors(original_vector, data_structure)
        self.fill_vectors(original_vector, data_structure)

    def fill_vectors(self, original_vector, data_structure='default'):
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

    def create_vectors(self, original_vector, data_structure='default'):
        # Calculate int_width for the integer part using absolute values
        max_abs_value = max(abs(x) for x in original_vector)
        int_width = max(1, math.ceil(math.log2(int(max_abs_value) + 1)))
        self.integer_part = sdsl4py.int_vector(size=self.n_elements, default_value=0, int_width=int_width)
    
        # Determine decimal width
        if self.decimal_places is None:
            # Convert to string without scientific notation
            str_values = [f"{abs(x):.50f}" for x in original_vector]
            max_decimal_places = max(len(s.split(".")[1]) if "." in s else 0 for s in str_values)
            max_decimal_places = min(max_decimal_places, 50)  # Reasonable upper limit
        else:
            max_decimal_places = self.decimal_places
        self.decimal_width = max_decimal_places
    
        # Calculate int_width for the decimal part
        decimal_int_width = math.ceil(math.log2(10 ** max_decimal_places))
        self.decimal_part = sdsl4py.int_vector(size=self.n_elements, default_value=0, int_width=decimal_int_width)
    
        # Sign part
        self.sign_part = sdsl4py.bit_vector(size=self.n_elements, default_value=0)

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
    
    def __len__(self):
        """
        Return the number of elements in the compressed vector.
        """
        return self.n_elements
    
    def __getitem__(self, index):
        """
        Return the value at the given index, including the sign part.
        """
        if isinstance(index, int):
            if index < 0 or index >= self.n_elements:
                raise IndexError("Index out of range")
            value = self.integer_part[index] + self.decimal_part[index] / (10 ** self.decimal_width)
            return value if self.sign_part[index] == 1 else -value
        elif isinstance(index, slice):
            # Handle slicing
            start, stop, step = index.indices(self.n_elements)
            return [
                (self.integer_part[i] + self.decimal_part[i] / (10 ** self.decimal_width)) 
                if self.sign_part[i] == 1 else 
                -(self.integer_part[i] + self.decimal_part[i] / (10 ** self.decimal_width))
                for i in range(start, stop, step)
            ]
        else:
            raise TypeError("Invalid index type")
