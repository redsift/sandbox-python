import sys
import time

import nanomsg

import bootstrap


def main():
    node_indexes = sys.argv[1:]
    if len(node_indexes) == 0:
        print 'no nodes to execute'
        return 1

    sockets = {}
    for i in map(int, node_indexes):
        s = nanomsg.Socket(nanomsg.REQ)
        addr = "ipc:///tmp/%d.sock" % i
        s.bind(addr)
        print 'bound to', addr
        sockets[i] = s

    while True:
        for i, s in sockets.items():
            s.send("hello")
            print time.time(), s.recv(), 'from', i
            time.sleep(1)

if __name__ == '__main__':
    main()
