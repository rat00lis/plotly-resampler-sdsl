import pytest
import numpy as np
from data_structures.input_tools import InputTools

@pytest.fixture
def input_tools():
    return InputTools()

def test_default_normal(input_tools):
    size = 1000
    x, y = input_tools.get(input_type="default", option="normal", size=size)
    
    assert len(x) == size
    assert len(y) == size
    assert isinstance(y, np.ndarray)
    assert np.all(x == np.linspace(0, 4 * np.pi, size))
    assert isinstance(y[0], np.float64)

def test_default_sdsl4py(input_tools):
    size = 1000
    x, vector = input_tools.get(input_type="default", option="sdsl4py", size=size)
    
    assert len(x) == size 
    assert len(vector) == size
    assert hasattr(vector, 'build_from_vector')
    assert np.all(x == np.linspace(0, 4 * np.pi, size))

def test_invalid_input_type(input_tools):
    with pytest.raises(Exception):
        input_tools.get(input_type="invalid")

def test_custom_size(input_tools):
    size = 500
    x, y = input_tools.get(size=size)
    assert len(x) == size
    assert len(y) == size

def test_output_shapes_match(input_tools):
    size = 1000
    x, y = input_tools.get(size=size)
    assert x.shape == y.shape

def test_x_values_monotonic(input_tools):
    x, _ = input_tools.get()
    assert np.all(np.diff(x) > 0)

def test_get_from_file(input_tools):
    # Create a temporary CSV file for testing
    test_file_path = 'test_data.csv'
    with open(test_file_path, 'w') as f:
        f.write("0,1\n")
        f.write("1,2\n")
        f.write("2,3\n")

    # Test the function
    x, y = input_tools.get_from_file(test_file_path, option="default", column=1, delimiter=",")

    assert len(x) == 3
    assert len(y) == 3
    assert np.all(x == np.array([0, 1, 2]))
    assert np.all(y == np.array([1, 2, 3]))

    # Clean up the temporary file
    import os
    os.remove(test_file_path)