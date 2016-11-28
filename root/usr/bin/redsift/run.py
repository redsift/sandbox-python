from __future__ import print_function

import imp
import json
import os
import os.path
import sys
import threading
import time
import math

from monotonic import monotonic

from nanomsg import Socket, REP

import protocol
import init

def listen_and_reply(sock, compute_func):
    while True:
        req = protocol.from_encoded_message(sock.recv())
        start = monotonic()
        try:
            ret = compute_func(req)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            #sock.send(protocol.to_encoded_message(ret, diff))
            return
        end = monotonic()
        t = end - start
        diff = []
        diff.append(math.floor(t))
        diff.append((t - diff[0]) * math.pow(10, 9))
        sock.send(protocol.to_encoded_message(ret, diff))

def new_module(node_idx, src):
    # Prepend source file and local site-packages dirs to sys.path to allow
    # relative imports.
    for d in  [os.path.dirname(src), os.path.join(os.path.dirname(src), 'site-packages')]:
        if d not in sys.path:
            sys.path.insert(0, d)

    m = imp.load_source('node%d' % node_idx, src)
    if not hasattr(m, 'compute'):
        print('"%s" does not implement compute function' % src)
        sys.exit(1)
    return m

def load_dag(sift_root):
    sift_json = init.env_var_or_exit('SIFT_JSON')
    return json.load(open(os.path.join(sift_root, sift_json)))

def main():
    sift_root = init.env_var_or_exit('SIFT_ROOT')
    ipc_root = init.env_var_or_exit('IPC_ROOT')
    dag = load_dag(sift_root)
    threads = {}
    sockets = []
    node_indexes = sys.argv[1:]
    if len(node_indexes) == 0:
        print('no nodes to execute')
        return 1

    dry = os.environ.get('DRY', 'false')
    if dry == 'true':
        return 0

    for i in map(int, node_indexes):
        src = os.path.join(sift_root, dag['dag']['nodes'][i]['implementation']['python'])
        print('loading ' + src)
        m = new_module(i, src)

        # Create nanomsg socket.
        addr = 'ipc://%s/%d.sock'% (ipc_root, i)
        s = Socket(REP)
        s.recv_max_size = -1
        s.connect(addr)
        print('connected to '+ addr)
        sockets.append(s)

        # Launch request handler.
        t = threading.Thread(target=listen_and_reply, args=(s, m.compute))
        t.daemon = True
        t.start()
        threads[i] = t

    try:
        while True:
            time.sleep(1)
            for i, thr in threads.items():
                if not thr.isAlive():
                    raise Exception('thread of node with index %d is dead' % i)
    finally:
        print('closing sockets')
        for s in sockets: s.close()

if __name__ == '__main__':
    main()
