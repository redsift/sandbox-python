from __future__ import print_function

import json
import os
import os.path
import sys
import threading
import time
import math
import traceback
import re
import site
import protocol
import init

from monotonic import monotonic
from nanomsg import Socket, REP

try:
    from importlib.machinery import SourceFileLoader as load_source
except:
    from imp import load_source


def listen_and_reply(sock, m, err):
    while True:
        req = protocol.from_encoded_message(sock.recv())
        start = monotonic()

        if m is None:
            sock.send(json.dumps(dict(error=err)).encode())
        else:
            try:
                ret = m.compute(req)
                end = monotonic()
                t = end - start
                diff = []
                diff.append(math.floor(t))
                diff.append((t - diff[0]) * math.pow(10, 9))
                sock.send(protocol.to_encoded_message(ret, diff).encode())
            except:
                exc = traceback.format_exc()
                print(exc)
                err = dict(message=sys.exc_info()[0].__name__, stack=exc)
                sock.send(json.dumps(dict(error=err)).encode())


def add_site_dir(srcp):
    spp = os.path.join(srcp, "site-packages")
    for path in [srcp, spp]:
        if path not in sys.path:
            site.addsitedir(path)


def new_module(node_idx, src):
    # Prepend source file and local site-packages dirs to sys.path to allow
    # relative imports.
    srcp = os.path.dirname(src)
    root_path_search = re.search(r"(.+/server)/.*", srcp)
    if root_path_search:
        root_path = root_path_search[1]
        add_site_dir(root_path)

    add_site_dir(srcp)

    m = load_source("node%d" % node_idx, src)
    if sys.version_info[0] == 3:
        m = m.load_module()
    if not hasattr(m, "compute"):
        print('"%s" does not implement compute function' % src)
        sys.exit(1)
    return m


def load_dag(sift_root):
    sift_json = init.env_var_or_exit("SIFT_JSON")
    return json.load(open(os.path.join(sift_root, sift_json)))


def main():
    sift_root = init.env_var_or_exit("SIFT_ROOT")
    ipc_root = init.env_var_or_exit("IPC_ROOT")
    dag = load_dag(sift_root)
    threads = {}
    sockets = []
    node_indexes = sys.argv[1:]
    if not node_indexes:
        print("no nodes to execute")
        return 1

    dry = os.environ.get("DRY", "false")
    if dry == "true":
        return 0

    for i in map(int, node_indexes):
        src = os.path.join(
            sift_root, dag["dag"]["nodes"][i]["implementation"]["python"]
        )
        # print("loading " + src)

        # Create nanomsg socket.
        addr = "ipc://%s/%d.sock" % (ipc_root, i)
        s = Socket(REP)
        s.recv_max_size = -1
        s.connect(addr)
        # print("connected to " + addr)
        sockets.append(s)

        m = None
        err = None
        try:
            m = new_module(i, src)
        except:
            m = None
            exc = traceback.format_exc()
            print(exc)
            err = dict(message=sys.exc_info()[0].__name__, stack=exc)

        # Launch request handler.
        t = threading.Thread(target=listen_and_reply, args=(s, m, err))
        t.daemon = True
        t.start()
        threads[i] = t

    try:
        while True:
            time.sleep(1)
            for i, thr in threads.items():
                if not thr.is_alive():
                    raise Exception("thread of node with index %d is dead" % i)
    finally:
        print("closing sockets")
        for s in sockets:
            s.close()


if __name__ == "__main__":
    main()
