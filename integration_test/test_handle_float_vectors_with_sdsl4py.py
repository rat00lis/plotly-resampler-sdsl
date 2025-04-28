from data_structures.compressed_vector import CompressedVector

def test_handle_float_vectors_with_sdsl4py():
    # Input data
    original_vector = [1234.5678, 0.00012345, 98765.4321, 42.0, 0.99999999]
    decimal_places = 8

    # Create the compressed vector
    compressed_vector = CompressedVector()
    compressed_vector.build_from_vector(original_vector, decimal_places=decimal_places)

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