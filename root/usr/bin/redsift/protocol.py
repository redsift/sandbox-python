import base64
import json


def b64decode(d):
    for dd in d['data']:
        if 'value' in dd:
            dd['value'] = base64.b64decode(dd['value'])
    return d

def b64encode(d):
    if 'value' in d:
        v = d['value']
        if type(v) == dict or type(v) == list:
            d['value'] = base64.b64encode(json.dumps(v).encode('utf-8')).decode('utf-8')
        elif type(v) == str:
            d['value'] = base64.b64encode(v.encode('utf-8')).decode('utf-8')
        elif type(v) == bytearray or type(v) == bytes:
            d['value'] = base64.b64encode(v).decode('utf-8')
        else:
            raise Exception('unsupported data type')
    return d

def to_encoded_message(d, diff):
    """Marshal the data d to write it to the socket."""
    if type(d) == dict:
        out = [b64encode(d)]
    elif type(d) == list:
        out = [b64encode(i) for i in d]
    elif d == None:
        out = [d]
    else:
        raise Exception('node implementation has to return dict, list or None')

    return json.dumps(dict(out=out, stats=dict(result=diff)))

def from_encoded_message(data):
    """Umarshal the raw data read of the socket."""
    d = json.loads(data.decode('utf-8'))

    for k in ['in', 'with']:
        if k in d:
            b64decode(d[k])

    for l in d.get('lookup', []):
        b64decode(l)

    return d
