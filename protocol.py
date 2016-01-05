import base64
import json


def b64decode(d):
    for dd in d['data']:
        if 'value' in dd:
            dd['value'] = base64.b64decode(dd['value'])
    return d

def b64encode(d):
    if 'value' in d:
        d['value'] = base64.b64encode(json.dumps(d['value']))
    return d

def marshal(d):
    """Marshal the data d to write it to the socket."""
    if type(d) == dict:
        out = [b64encode(d)]
    else:
        out = [b64encode(i) for i in d]
    return json.dumps(dict(out=out))

def unmarshal(data):
    """Umarshal the raw data read of the socket."""
    d = json.loads(data)

    for k in ['in', 'with']:
        if k in d: b64decode(d[k])

    return d
