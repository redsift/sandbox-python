import protocol as p


def test_marshal():
    d = dict(value='abc')
    assert p.marshal(d) == '{"out": [{"value": "ImFiYyI="}]}'

def test_unmarshal():
    d = p.unmarshal('{"in":{"data":[{"value": "ImFiYyI="}]}}')
    assert d == {'in': {'data': [{'value': '"abc"'}]}}

