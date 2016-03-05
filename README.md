# Description

A simple broker that subscribes to a given set of publishers to publish all
incoming events on another publisher socket.

# Why?

We need a log-broker that can publish log events from several services on one
system for easier/convienent consumption by another serivce or ui.

# Usage

Note that the broker expects multipart messages.

```
# ./log-broker pub-addr1 pub-addr2 ... pub-addrN

# ./test_t1_pub.py &
# ./log-broker.py ipc:///tmp/t1.ipc &
# ./test_log_broker_pub.py
```

# Development

Required dependencies:

* zeromq 4.1.4
* Python 2.7
* Python Modules:
    * pyzmq 15.2.0
