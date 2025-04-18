import sdsl4py

def test_sdsl4py_import_and_usage():
    # Test if the library can be imported and used
    v = sdsl4py.int_vector(size=10, default_value=0, int_width=8)
    for i in range(10):
        v[i] = i

    ev = sdsl4py.enc_vector_elias_delta(v)
    vv = sdsl4py.vlc_vector_elias_delta(v)
    dv = sdsl4py.dac_vector(v)

    # Check if the size_in_bytes function works without errors
    assert sdsl4py.size_in_bytes(v) > 0
    assert sdsl4py.size_in_bytes(ev) > 0
    assert sdsl4py.size_in_bytes(vv) > 0
    assert sdsl4py.size_in_bytes(dv) > 0