import base64
import json


def unmarshal(data):
    """Umarshal the raw data read of the socket."""
    print '\n--'
    print data
    try:
        d = json.loads(data)
        print d.keys()
    except ValueError:
        pass
    return data

def marshal(s):
    return str(s)
