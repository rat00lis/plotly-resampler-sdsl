"""
    Test if the plot results of all the models are correct.
"""

import os
import pytest
import numpy as np
from plotly_resampler import FigureWidgetResampler
import plotly.graph_objects as go  
import sdsl4py
from data_structures.compressed_vector import CompressedVector
import math

output_path = "integration_test/test_output"

@pytest.fixture
def setup_plot():
    figure = go.Figure()
    resampler = FigureWidgetResampler(figure)
    # x and y for a sine wave of size 10000
    x = np.linspace(0, 10, 10000)
    y = np.sin(x)
    
    def truncate(value, decimal_places):
        str_value = str(value)
        if '.' in str_value:
            integer_part, decimal_part = str_value.split('.')
            decimal_part = decimal_part[:decimal_places]
            return float(f"{integer_part}.{decimal_part}")
        else:
            return float(str_value)
    # Truncate y values to 4 decimal places
    y = np.array([truncate(val, 4) for val in y])
    x = np.array([truncate(val, 4) for val in x])
    return x, y, resampler

def test_plot_results(setup_plot):
    x = setup_plot[0]
    y = setup_plot[1]
    resampler = setup_plot[2]

    # Create and fill compressed vectors more efficiently
    c_vector_x = CompressedVector(
        decimal_places=4,
        int_width=32,
    )
    c_vector_x.create_vector(len(x))
    c_vector_x.fill_from_vector(x)

    c_vector_y = CompressedVector(
        decimal_places=4,
        int_width=32,
    )
    c_vector_y.create_vector(len(y))
    c_vector_y.fill_from_vector(y)

    # Add the compressed vectors to the figure
    resampler.add_trace(
        go.Scatter(name="Compressed Sine Wave", mode="lines", showlegend=True),
        hf_x=c_vector_x,
        hf_y=c_vector_y
    )

    # Move the plot upwards and make a new trace
    # For adding 1 to the y values, create a new numpy array first
    y_plus_one = y + 1

    resampler.add_trace(
        go.Scatter(name="Compressed Sine Wave + 1", mode="lines", showlegend=True),
        hf_x=x,
        hf_y=y_plus_one
    )

    # Save the figure
    os.makedirs(output_path, exist_ok=True)
    resampler.write_html(os.path.join(output_path, "test_plot_results.html"))

    # assert all values are close enough (within tolerance)
    for i in range(len(x)):
        assert np.isclose(x[i], c_vector_x[i], rtol=1e-3, atol=1e-4), \
            f"X values do not match at index {i}, x: {x[i]}, c_vector_x: {c_vector_x[i]}"