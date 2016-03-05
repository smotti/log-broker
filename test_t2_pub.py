#!/usr/bin/env python2.7

from time import sleep
import zmq


ADDR = "ipc:///tmp/t2.ipc"


if __name__ == "__main__":
    context = zmq.Context.instance()
    pub = context.socket(zmq.PUB)
    pub.bind(ADDR)

    while True:
        msg = ["t2", "hello"]
        pub.send_multipart(msg)
        sleep(1)
