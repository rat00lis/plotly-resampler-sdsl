"""
    Test compressed vector buffer.
    This test verifies that the function np.asarray() correctly converts a compressed vector to a numpy array.
    It also checks that the memory usage of the compressed vector is less than 1 MB, and the time
    taken to convert the compressed vector to a numpy array is about the same as the time taken to
    convert a normal vector to a numpy array.
"""

import numpy as np
import sdsl4py
import time
import tracemalloc
import pytest
from plotly_resampler import FigureWidgetResampler
from data_structures.compressed_vector import CompressedVector as cv
from plotly import graph_objects as go
from benchmark.input_handler import InputHandler

file_name = "integration_test/test_input/test_np_asarray.txt"
@pytest.fixture
def input_handler():
    # Create a file with two columns of data, of size 100000
    with open(file_name, "w") as file:
        for i in range(100000):
            file.write(f"{i};{99999-i}\n")
    return InputHandler()

def test_np_asarray_avg_time(input_handler):
    """
    Test that the average time taken to convert a compressed vector to a numpy array is about the same
    as the time taken to convert a normal vector to a numpy array.
    """
    # Get the values from a file to a vector without the tool
    or_vec_x, or_vec_y = np.loadtxt(file_name, delimiter=";", unpack=True)

    # Get the values from a file to a vector with the tool
    ih_vector_x, ih_vector_y = input_handler.get_from_file(
        file_path=file_name,
        option="default",
        decimal_places=0,
        delimiter=";",
        column=1,
        truncate=None
    )

    # Measure time for normal vector
    start_time = time.time()
    np.asarray(or_vec_x)
    normal_vector_time = time.time() - start_time

    # Measure time for compressed vector
    start_time = time.time()
    np.asarray(ih_vector_x)
    compressed_vector_time = time.time() - start_time

    # Check if the times are about the same
    assert abs(normal_vector_time - compressed_vector_time) < 0.1, f"Expected {normal_vector_time} but got {compressed_vector_time}"

def test_memory_usage(input_handler):
    """
    Test that the memory usage of the compressed vector is less than 1 MB.
    """
    # Get the values from a file to a vector with the tool
    ih_vector_x, ih_vector_y = input_handler.get_from_file(
        file_path=file_name,
        option="sdsl4py",
        decimal_places=0,
        delimiter=";",
        column=1,
        truncate=None
    )

    # Measure memory usage
    tracemalloc.start()
    snapshot1 = tracemalloc.take_snapshot()
    
    # Create a resampler figure and add trace
    resampler_figure = FigureWidgetResampler()
    resampler_figure.add_trace(
        go.Scattergl(name='resampler', showlegend=True),
        hf_x=ih_vector_x,
        hf_y=ih_vector_y,
    )
    
    # Take another snapshot and get the difference
    snapshot2 = tracemalloc.take_snapshot()
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')
    
    tracemalloc.stop()

    # Check if the memory usage is less than 1 MB
    # Using the first stat which should be the largest allocation
    if top_stats:
        memory_used = top_stats[0].size_diff if top_stats[0].size_diff > 0 else top_stats[0].size
        assert memory_used < 1024 * 1024, f"Expected add_trace memory usage < 1 MB but got {memory_used / (1024 * 1024)} MB"
    else:
        pytest.fail("No memory allocation stats found") 
        
def test_add_trace_avg_time(input_handler):
    """
    Test that the average time taken to add a trace to a FigureWidgetResampler is about the same
    as the time taken to add a trace to a normal plotly figure.
    """
    # Get the values from a file to a vector with the tool
    ih_vector_x, ih_vector_y = input_handler.get_from_file(
        file_path=file_name,
        option="sdsl4py",
        decimal_places=0,
        delimiter=";",
        column=1,
        truncate=None
    )

    # Create a normal plotly figure
    plotly_figure = FigureWidgetResampler()
    start_time = time.time()
    plotly_figure.add_trace(
        go.Scatter(
            x=ih_vector_x,
            y=ih_vector_y,
            mode="lines",
            name="plotly",
            line=dict(color="blue"),  # Set color for the plotly trace
        )
    )
    normal_plotly_time = time.time() - start_time

    # Create a resampler figure
    resampler_figure = FigureWidgetResampler(plotly_figure)
    start_time = time.time()
    resampler_figure.add_trace(
        go.Scattergl(name='resampler', showlegend=True, line=dict(color="green")),  # Set color for the resampler trace
        hf_x=ih_vector_x,
        hf_y=ih_vector_y,
    )
    resampler_plotly_time = time.time() - start_time

    # Check if the times are about the same or if resampler is faster
    assert resampler_plotly_time <= normal_plotly_time + 0.1, f"Expected resampler time ({resampler_plotly_time}) to be similar or faster than normal time ({normal_plotly_time})"