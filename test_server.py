from __future__ import print_function

import sys
import time
import json

from pynng import Req0

def main():
    sift_root = '/tmp'
    node_indexes = sys.argv[1:]
    if len(node_indexes) == 0:
        print('no nodes to execute')
        return 1

    sockets = {}
    for i in map(int, node_indexes):
        s = Req0(listen=f"ipc://{ipc_root}/{i}.sock")
        print(f"bound to ipc://{ipc_root}/{i}.sock")
        sockets[i] = s

    while True:
        for i, s in sockets.items():
            s.send(json.dumps(dict(hello=23)))
            print(time.time(), s.recv(), 'from', i)
            time.sleep(1)

if __name__ == '__main__':
    main()
