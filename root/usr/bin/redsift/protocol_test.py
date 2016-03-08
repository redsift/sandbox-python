import protocol as p


def test_encode():
    d = dict(value='abc')
    assert p.to_encoded_message(d, [0,0]) == '{"stats": {"result": [0, 0]}, "out": [{"value": "YWJj"}]}'

def test_decode():
    d = p.from_encoded_message('{"in":{"data":[{"value": "YWJj"}]}}')
    assert d == {'in': {'data': [{'value': 'abc'}]}}

def test_decode_lookup():
    d = p.from_encoded_message('{"in":{"data":[{"value": "YWJj"}]}, "lookup": [{"data":[{"value": "YWJj"}]}]}')
    assert d == {'in': {'data': [{'value': 'abc'}]}, 'lookup': [{'data': [{'value': 'abc'}]}]}
