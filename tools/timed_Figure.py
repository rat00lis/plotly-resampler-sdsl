import time
import numpy as np
from plotly import Figure

class timed_Figure(Figure):
    """
    A subclass of Figure that times the execution of the to_image method.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timing = {}

    def to_image(self, *args, **kwargs) -> Tuple[np.ndarray, float]:
        """
        Generate an image from the figure and time the operation.
        """
        start_time = time.time()
        image = super().to_image(*args, **kwargs)
        end_time = time.time()
        self.timing["to_image"] = end_time - start_time
        return image
    
    def add_trace(self, *args, **kwargs):
        """
        Add a trace to the figure and time the operation.
        """
        start_time = time.time()
        result = super().add_trace(*args, **kwargs)
        end_time = time.time()
        self.timing["add_trace"] = end_time - start_time
        return result
