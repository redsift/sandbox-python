from __future__ import print_function

import imp
import json
import os
import os.path
import sys
import threading
import time
import math

import monotonic

from nanomsg import Socket, REP

import protocol as p

def listen_and_reply(sock, compute_func):
    while True:
        req = p.from_encoded_message(sock.recv())
        start = monotonic()
        # TODO: try/catch
        ret = compute_func(req)
        end = monotonic()
        t = end - start
        diff = []
        diff.append(math.floor(t))
        diff.append((t - math.floor(t)) * math.pow(10, 9))
        sock.send(p.to_encoded_message(ret, diff))

def env_var_or_exit(n):
    v = os.environ.get(n)
    if not v:
        print(n + ' not set')
        sys.exit(1)
    return v

def new_module(node_idx, src):
    # Append dir of the source file to sys.path to allow relative imports.
    sys.path.append(os.path.dirname(src))
    m = imp.load_source('node%d' % node_idx, src)
    if not hasattr(m, 'compute'):
        print('"%s" does not implement compute function' % src)
        sys.exit(1)
    return m

def load_dag(sift_root):
     return json.load(open(os.path.join(sift_root, 'sift.json')))

def main():
    sift_root = env_var_or_exit('SIFT_ROOT')
    ipc_root = env_var_or_exit('IPC_ROOT')
    dag = load_dag(sift_root)
    threads = {}
    sockets = []
    node_indexes = sys.argv[1:]
    if len(node_indexes) == 0:
        print('no nodes to execute')
        return 1
    for i in map(int, node_indexes):
        src = os.path.join(sift_root, dag['dag']['nodes'][i]['implementation']['python'])
        print('loading ' + src)
        m = new_module(i, src)

        # Create nanomsg socket.
        addr = 'ipc://%s/%d.sock'% (ipc_root, i)
        s = Socket(REP)
        s.send_timeout = 2000 # ms
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
