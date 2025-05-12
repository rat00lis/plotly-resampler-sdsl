import pytest
import numpy as np
from benchmark.input_handler import InputHandler

#create file
file_name = "integration_test/test_input/test_input_tools.txt"

@pytest.fixture
def input_handler():
    #write csv file as [0] = 1...1000, and [1] = 999...0
    with open(file_name, "w") as file:
        for i in range(1000):
            file.write(f"{i};{999-i}\n")

    return InputHandler()

def verify_values_are_the_same(original_x, original_y, ih_x, ih_y):
    #assert the values are the same
    assert np.array_equal(original_x, ih_x), f"Expected {original_x} but got {ih_x}"
    assert np.array_equal(original_y, ih_y), f"Expected {original_y} but got {ih_y}"


def test_normal_option(input_handler):
    #get the values from a file to a vector without the tool
    or_vec_x, or_vec_y = np.loadtxt(file_name, delimiter=";", unpack=True)
    
    #get the values from a file to a vector with the tool
    ih_vector_x, ih_vector_y = input_handler.get_from_file( 
        file_path=file_name,
        option = "default",
        decimal_places= 0, 
        delimiter=";", 
        column=1, 
        truncate=None
    )
    
    #assert the values are the same
    verify_values_are_the_same(or_vec_x, or_vec_y, ih_vector_x, ih_vector_y)

def test_sdsl4py_option_with_64_width(input_handler):
    or_vec_x, or_vec_y = np.loadtxt(file_name, delimiter=";", unpack=True)
    # sdsl4py case
    ih_vector_x, ih_vector_y = input_handler.get_from_file( 
        file_path=file_name,
        option = "sdsl4py",
        decimal_places= 0, 
        delimiter=";", 
        column=1, 
        truncate=None
    )

    input_handler.set_width(64)
    #assert the values are the same
    verify_values_are_the_same(or_vec_x, or_vec_y, ih_vector_x, ih_vector_y)

def test_sdsl4py_option_with_32_width(input_handler):
    or_vec_x, or_vec_y = np.loadtxt(file_name, delimiter=";", unpack=True)
    # sdsl4py case
    ih_vector_x, ih_vector_y = input_handler.get_from_file( 
        file_path=file_name,
        option = "sdsl4py",
        decimal_places= 0, 
        delimiter=";", 
        column=1, 
        truncate=None
    )

    input_handler.set_width(32)
    #assert the values are the same
    verify_values_are_the_same(or_vec_x, or_vec_y, ih_vector_x, ih_vector_y)

def test_sdsl4py_option_with_16_width(input_handler):
    or_vec_x, or_vec_y = np.loadtxt(file_name, delimiter=";", unpack=True)
    # sdsl4py case
    ih_vector_x, ih_vector_y = input_handler.get_from_file( 
        file_path=file_name,
        option = "sdsl4py",
        decimal_places= 0, 
        delimiter=";", 
        column=1, 
        truncate=None
    )

    input_handler.set_width(16)
    #assert the values are the same
    verify_values_are_the_same(or_vec_x, or_vec_y, ih_vector_x, ih_vector_y)

def test_sdsl4py_option_with_8_width(input_handler):
    or_vec_x, or_vec_y = np.loadtxt(file_name, delimiter=";", unpack=True)
    # sdsl4py case
    ih_vector_x, ih_vector_y = input_handler.get_from_file( 
        file_path=file_name,
        option = "sdsl4py",
        decimal_places= 0, 
        delimiter=";", 
        column=1, 
        truncate=None
    )

    input_handler.set_width(8)
    #assert the values are the same
    verify_values_are_the_same(or_vec_x, or_vec_y, ih_vector_x, ih_vector_y)