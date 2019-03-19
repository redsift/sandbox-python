import protocol as p
import json

def test_encode():
    d = dict(value='abc')
    assert json.loads(p.to_encoded_message(d, [0,0])) == json.loads('{"stats": {"result": [0, 0]}, "out": [{"value": "YWJj"}]}')

def test_decode():
    d = p.from_encoded_message(b'{"in":{"data":[{"value": "YWJj"}]}}')
    assert d == {'in': {'data': [{'value': b'abc'}]}}

def test_decode_get():
    d = p.from_encoded_message(b'{"in":{"data":[{"value": "YWJj"}]}, "get": [{"data":[{"value": "YWJj"}]}]}')
    assert d == {'in': {'data': [{'value': b'abc'}]}, 'get': [{'data': [{'value': b'abc'}]}]}

def test_decode_get1():
    d = p.from_encoded_message(b'{"in":{"data":[{"value": "YWJj"}]}, "get": [{"data":[]}]}')
    assert d == {'in': {'data': [{'value': b'abc'}]}, 'get': [{'data': []}]}

def test_decode_get2():
    d = p.from_encoded_message(b'{"in":{"data":[{"value": "YWJj"}]}, "get": [{"data":[{"value": null}]}]}')
    assert d == {'in': {'data': [{'value': b'abc'}]}, 'get': [{'data': [{'value': None }]}]}

def test_decode_get3():
    d = p.from_encoded_message(b'{"in":{"data":[{"value": "YWJj"}]}, "get": [{"data":null}]}')
    assert d == {'in': {'data': [{'value': b'abc'}]}, 'get': [{'data': None}]}

test_encode()
test_decode()
test_decode_get()
test_decode_get1()
test_decode_get2()
test_decode_get3()
