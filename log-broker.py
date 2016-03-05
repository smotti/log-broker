#!/usr/bin/env python2.7
from os import _exit
from sys import argv, exit
from threading import Thread
from time import sleep
import zmq


FRONTEND_ADDR = "inproc://log-broker-frontend"
BACKEND_ADDR = "ipc:///tmp/log-broker-backend.ipc"


def sub_pub_proxy():
    context = zmq.Context.instance()
    frontend = context.socket(zmq.SUB)
    frontend.bind(FRONTEND_ADDR)
    frontend.setsockopt(zmq.SUBSCRIBE, b"")

    backend = context.socket(zmq.PUB)
    backend.bind(BACKEND_ADDR)

    try:
        zmq.proxy(frontend, backend)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        return
    finally:
        frontend.close()
        backend.close()


def subscriber(addr):
    context = zmq.Context.instance()
    sub = context.socket(zmq.SUB)
    sub.setsockopt(zmq.SUBSCRIBE, b"")
    sub.connect(addr)
    pub = context.socket(zmq.PUB)
    pub.connect(FRONTEND_ADDR)

    while True:
        try:
            msg = sub.recv_multipart()
            pub.send_multipart(msg)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            return
        finally:
            sub.close()
            pub.close()


def main(subscribe_to):
    sub_pub_proxy_t = Thread(target=sub_pub_proxy, name="proxy")
    sub_pub_proxy_t.start()

    subscribers = []
    for addr in subscribe_to:
        sub = Thread(target=subscriber, name=addr, args=(addr,))
        sub.start()
        subscribers.append(sub)

    while True:
        sleep(1)


if __name__ == "__main__":
    if len(argv) == 1:
        print("No subscription addresses specified!")
        exit(1)

    try:
        main(argv[1:])
    except KeyboardInterrupt:
        try:
            exit(0)
        except SystemExit:
            _exit(0)
    finally:
        context = zmq.Context.instance()
        context.destroy()
