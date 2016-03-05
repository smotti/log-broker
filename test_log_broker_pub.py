#!/usr/bin/env python2.7

import zmq


PUB_ADDR = "ipc:///tmp/log-broker-backend.ipc"

if __name__ == "__main__":
    context = zmq.Context.instance()
    sub = context.socket(zmq.SUB)
    sub.setsockopt(zmq.SUBSCRIBE, b"")
    sub.connect(PUB_ADDR)

    while True:
        msg = sub.recv_multipart()
        print(msg)
