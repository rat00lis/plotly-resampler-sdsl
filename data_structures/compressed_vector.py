import sdsl4py
import math

class CompressedVector:
    def __init__(self, n_elements, original_vector, data_structure='default', decimal_places=8):
        self.n_elements = n_elements
        self.integer_part = None
        self.decimal_part = None
        self.current = 0
        self.decimal_places = decimal_places
        self.build_compressed_vector(original_vector, data_structure)

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current < self.n_elements:
            value = self.integer_part[self.current] + self.decimal_part[self.current] / (10 ** self.decimal_width)
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
            value = original_vector[i]
            # Split into integer and decimal parts
            int_part, dec_part = str(value).split(".") if "." in str(value) else (str(value), "0")
            
            # Store the integer part
            self.integer_part[i] = int(int_part)

            # Handle the decimal part: pad or truncate to match decimal_width
            dec_part = dec_part.ljust(self.decimal_width, "0")[:self.decimal_width]
            self.decimal_part[i] = int(dec_part)

    def create_vectors(self, original_vector, data_structure='default'):
        # Calculate int_width for the integer part
        int_width = math.ceil(math.log2(max(original_vector) + 1))
        self.integer_part = sdsl4py.int_vector(size=self.n_elements, default_value=0, int_width=int_width)

        # Determine decimal width
        if self.decimal_places is None:
            max_decimal_places = max(len(str(x).split(".")[1]) if "." in str(x) else 0 for x in original_vector)
        else:
            max_decimal_places = self.decimal_places
        self.decimal_width = max_decimal_places

        # Calculate int_width for the decimal part
        decimal_int_width = math.ceil(math.log2(10 ** max_decimal_places))
        self.decimal_part = sdsl4py.int_vector(size=self.n_elements, default_value=0, int_width=decimal_int_width)

    def size_in_bytes(self):
        """
        Return the size in bytes of the compressed vector.
        """
        total = sdsl4py.size_in_bytes(self.integer_part) + sdsl4py.size_in_bytes(self.decimal_part)
        return total