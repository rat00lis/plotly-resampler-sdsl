import pytest
from data_structures.compressed_vector import CompressedVector
import sdsl4py


@pytest.fixture
def original_vector_and_decimal_places():
    # Input data
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


def test_default_compressed_vector(original_vector_and_decimal_places):
    original_vector, decimal_places = original_vector_and_decimal_places
    # Create the compressed vector
    cv = CompressedVector()
    cv.build_from_vector(original_vector, decimal_places=decimal_places)
    verify_compressed_vector(original_vector, decimal_places, cv)


def test_enc_compressed_vector(original_vector_and_decimal_places):
    original_vector, decimal_places = original_vector_and_decimal_places
    cv = CompressedVector()
    cv.set_int_part_structure(sdsl4py.enc_vector_elias_delta)
    cv.set_dec_part_structure(sdsl4py.enc_vector_elias_delta)
    cv.build_from_vector(original_vector, decimal_places=decimal_places)
    verify_compressed_vector(original_vector, decimal_places, cv)

def test_vlc_compressed_vector(original_vector_and_decimal_places):
    original_vector, decimal_places = original_vector_and_decimal_places
    cv = CompressedVector()
    cv.set_int_part_structure(sdsl4py.vlc_vector_elias_delta)
    cv.set_dec_part_structure(sdsl4py.vlc_vector_elias_delta)
    cv.build_from_vector(original_vector, decimal_places=decimal_places)
    verify_compressed_vector(original_vector, decimal_places, cv)

def test_dac_compressed_vector(original_vector_and_decimal_places):
    original_vector, decimal_places = original_vector_and_decimal_places
    cv = CompressedVector()
    cv.set_int_part_structure(sdsl4py.dac_vector)
    cv.set_dec_part_structure(sdsl4py.dac_vector)
    cv.build_from_vector(original_vector, decimal_places=decimal_places)
    verify_compressed_vector(original_vector, decimal_places, cv)