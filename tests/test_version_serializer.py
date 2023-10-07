from anunnaki_server.utils import serialize_version

def test_serialize():
    assert serialize_version('0.0.1') == (0, 0, 1)
    assert serialize_version('0003.015.1') == (3, 15, 1)
