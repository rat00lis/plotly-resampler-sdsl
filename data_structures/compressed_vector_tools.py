from data_structures import compressed_vector

def convert_vectors_to_sdsl4py(*args, decimal_places=4, int_width=64):
    """
    Convert multiple vectors to sdsl4py format.
    
    Parameters:
    ----------
    *args : list, numpy.ndarray, etc.
        Any number of vectors to convert.
        
    Returns:
    -------
    list
        List of converted vectors.
    """
    converted_vectors = []
    for vec in args:
        c_vec = compressed_vector.CompressedVector(
            int_width=int_width,
            decimal_places=decimal_places
        )
        c_vec.create_vector(len(vec))
        c_vec.fill_from_vector(vec)
        converted_vectors.append(c_vec)
    return converted_vectors