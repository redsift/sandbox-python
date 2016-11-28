import protocol as p


def test_encode():
    d = dict(value='abc')
    d1 = dict(value='abc')
    print(p.to_encoded_message(d1, [0,0]))
    assert p.to_encoded_message(d, [0,0]) == '{"stats": {"result": [0, 0]}, "out": [{"value": "YWJj"}]}'

def test_decode():
    d = p.from_encoded_message('{"in":{"data":[{"value": "YWJj"}]}}')
    assert d == {'in': {'data': [{'value': 'abc'}]}}

def test_decode_lookup():
    d = p.from_encoded_message('{"in":{"data":[{"value": "YWJj"}]}, "lookup": [{"data":[{"value": "YWJj"}]}]}')
    assert d == {'in': {'data': [{'value': 'abc'}]}, 'lookup': [{'data': [{'value': 'abc'}]}]}

def test_decode_lookup1():
    d = p.from_encoded_message('{"in":{"data":[{"value": "YWJj"}]}, "lookup": [{"data":[]}]}')
    assert d == {'in': {'data': [{'value': 'abc'}]}, 'lookup': [{'data': []}]}

def test_decode_lookup2():
    d = p.from_encoded_message('{"in":{"data":[{"value": "YWJj"}]}, "lookup": [{"data":[{"value": null}]}]}')
    assert d == {'in': {'data': [{'value': 'abc'}]}, 'lookup': [{'data': [{'value': None }]}]}

def test_decode_lookup3():
    d = p.from_encoded_message('{"in":{"data":[{"value": "YWJj"}]}, "lookup": [{"data":null}]}')
    assert d == {'in': {'data': [{'value': 'abc'}]}, 'lookup': [{'data': None}]}

test_encode()
test_decode()
test_decode_lookup()
test_decode_lookup1()
test_decode_lookup2()
test_decode_lookup3()
