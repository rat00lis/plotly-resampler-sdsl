import pytest
from data_structures.compressed_vector import CompressedVector
import sdsl4py

def get_original_vector_and_decimal_places(width):
    if width <= 16:
        original_vector = [-12.56, 0.01, 98.43, -42.0, 0.99]
        decimal_places = 2
    else:
        original_vector = [1234.5678, 0.00012345, 98765.4321, 42.0, 0.99999999]
        decimal_places = 8
    return original_vector, decimal_places


def verify_compressed_vector(original_vector, decimal_places, compressed_vector):
    # Verify that the reconstructed values match the original values
    reconstructed_values = list(compressed_vector)
    for original, reconstructed in zip(original_vector, reconstructed_values):
        assert round(original, decimal_places) == round(reconstructed, decimal_places), \
            f"Original: {original}, Reconstructed: {reconstructed}"

    # Verify the size in bytes is greater than zero
    size_in_bytes = compressed_vector.size_in_bytes()
    assert size_in_bytes > 0, "Size in bytes should be greater than zero"
    print(f"Size in bytes: {size_in_bytes}")

    # Verify that the compressed vector can be iterated over
    for value in compressed_vector:
        assert isinstance(value, float), "Value should be a float"
        print(f"Value: {value}")


def test_int_vector_64():
    original_vector, decimal_places = get_original_vector_and_decimal_places(64)
    # Create the compressed vector
    cv = CompressedVector(decimal_places, 64)
    cv.create_vector(len(original_vector))
    cv.fill_from_vector(original_vector)
    verify_compressed_vector(original_vector, decimal_places, cv)

    assert type(cv.integer_part) == sdsl4py.int_vector_64, "Compressed vector should be of type int_vector_64"


def test_int_vector_32():
    original_vector, decimal_places = get_original_vector_and_decimal_places(32)
    # Create the compressed vector
    cv = CompressedVector(decimal_places, 32)
    cv.create_vector(len(original_vector))
    cv.fill_from_vector(original_vector)
    verify_compressed_vector(original_vector, decimal_places, cv)

    assert type(cv.integer_part) == sdsl4py.int_vector_32, "Compressed vector should be of type int_vector_32"


def test_int_vector_16():
    original_vector, decimal_places = get_original_vector_and_decimal_places(16)
    # Create the compressed vector
    cv = CompressedVector(decimal_places, 16)
    cv.create_vector(len(original_vector))
    cv.fill_from_vector(original_vector)
    verify_compressed_vector(original_vector, decimal_places, cv)

    assert type(cv.integer_part) == sdsl4py.int_vector_16, "Compressed vector should be of type int_vector_16"


def test_int_vector_8():
    original_vector, decimal_places = get_original_vector_and_decimal_places(8)
    # Create the compressed vector
    cv = CompressedVector(decimal_places, 8)
    cv.create_vector(len(original_vector))
    cv.fill_from_vector(original_vector)
    verify_compressed_vector(original_vector, decimal_places, cv)

    assert type(cv.integer_part) == sdsl4py.int_vector_8, "Compressed vector should be of type int_vector_8"