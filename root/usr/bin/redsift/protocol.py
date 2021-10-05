import sys
import json
import base64


def b64decode(d):
    if d["data"] is None:
        return d

    for dd in d["data"]:
        if "value" in dd:
            if dd["value"] is None:
                return d

            dd["value"] = base64.b64decode(dd["value"])
    return d


def b64encode(d):
    if "value" in d:
        v = d["value"]
        typ = type(v)
        if typ == dict or typ == list:
            d["value"] = base64.b64encode(json.dumps(v).encode("utf-8")).decode("utf-8")
        elif typ == str:
            if sys.version_info[0] < 3:
                d["value"] = base64.b64encode(v).decode("utf-8")
            else:
                d["value"] = base64.b64encode(v.encode("utf-8")).decode("utf-8")
        elif typ == bytearray or typ == bytes:
            d["value"] = base64.b64encode(v).decode("utf-8")
        else:
            print(typ)
            raise Exception("unsupported data type")
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
        raise Exception("node implementation has to return dict, list or None")

    return json.dumps({"out": out, "stats": {"result": diff}})


def from_encoded_message(data):
    """Umarshal the raw data read of the socket."""
    d = json.loads(data.decode("utf-8"))

    for k in ["in", "with"]:
        if k in d:
            b64decode(d[k])

    for g in d.get("get", []):
        b64decode(g)

    return d
