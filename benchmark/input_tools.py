import sdsl4py
import numpy as np

class InputTools:
    def __init__(self):
        pass
    
    def get(self, input_type="default", option="normal", size=10000000):
        """
            Get the inputs for the benchmark based on the input type and save them in input_cases.
        """
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
        vector_size = size
        x = np.arange(vector_size)
        base_signal = (np.sin(2 * np.pi * x / 10000) + 1) * 500
        base_signal = np.rint(base_signal).astype(int)
        noise = np.random.randint(-20, 21, size=len(x))
        integer_values = np.clip(base_signal + noise, 0, 999).astype(int)
        match option:
            case "sdsl4py":
                default_vector = sdsl4py.int_vector(size=vector_size, default_value=0, int_width=16)
                for i in range(len(integer_values)):
                    default_vector[i] = integer_values[i]
                return x,default_vector
            
            case "normal":
                return x,integer_values
