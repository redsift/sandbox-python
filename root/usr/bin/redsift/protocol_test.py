import protocol as p
import json

def test_encode():
    d = dict(value='abc')
    assert json.loads(p.to_encoded_message(d, [0,0])) == json.loads('{"stats": {"result": [0, 0]}, "out": [{"value": "YWJj"}]}')

def test_decode():
    d = p.from_encoded_message(b'{"in":{"data":[{"value": "YWJj"}]}}')
    assert d == {'in': {'data': [{'value': b'abc'}]}}

def test_decode_lookup():
    d = p.from_encoded_message(b'{"in":{"data":[{"value": "YWJj"}]}, "lookup": [{"data":[{"value": "YWJj"}]}]}')
    assert d == {'in': {'data': [{'value': b'abc'}]}, 'lookup': [{'data': [{'value': b'abc'}]}]}

def test_decode_lookup1():
    d = p.from_encoded_message(b'{"in":{"data":[{"value": "YWJj"}]}, "lookup": [{"data":[]}]}')
    assert d == {'in': {'data': [{'value': b'abc'}]}, 'lookup': [{'data': []}]}

def test_decode_lookup2():
    d = p.from_encoded_message(b'{"in":{"data":[{"value": "YWJj"}]}, "lookup": [{"data":[{"value": null}]}]}')
    assert d == {'in': {'data': [{'value': b'abc'}]}, 'lookup': [{'data': [{'value': None }]}]}

def test_decode_lookup3():
    d = p.from_encoded_message(b'{"in":{"data":[{"value": "YWJj"}]}, "lookup": [{"data":null}]}')
    assert d == {'in': {'data': [{'value': b'abc'}]}, 'lookup': [{'data': None}]}

test_encode()
test_decode()
test_decode_lookup()
test_decode_lookup1()
test_decode_lookup2()
test_decode_lookup3()
