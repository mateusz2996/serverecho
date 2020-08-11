import json
import logging
import os
import socket
import sys

import main

log = logging.getLogger("application")
hdlr = logging.FileHandler(os.getcwd() + "\\server_logs.txt")
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
hdlr.setFormatter(formatter)
log.addHandler(hdlr)
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.INFO)


host = 'localhost'
data_payload = 2048
backlog = 5


def echo_server(port):
    """ A simple echo server """
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Enable reuse address/port
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    server_address = (host, port)
    log.info("Starting up echo server  on %s port %s" % server_address)
    sock.bind(server_address)
    # Listen to clients, backlog argument specifies the max no. of queued connections
    sock.listen(backlog)
    while True:
        log.info("Waiting to receive message from client")
        client, address = sock.accept()
        data = client.recv(data_payload)
        nums = [int(s) for s in list(data.decode("utf-8")) if s.isdigit()]
        message1 = dict({"sum": main.sum_by_reduce(nums)})
        message2 = dict({"min": min(nums)})
        message3 = dict({"max": max(nums)})
        message4 = dict({"number of unique elements": len(set(nums))})
        message = {"result": [message1, message2, message3, message4]}
        data = json.dumps(message)
        if data:
            log.info("Data: %s" % data)
            client.send(bytes(data, encoding="utf-8"))
            log.info("sent %s bytes back to %s" % (data, address))
        # end connection
        client.close()


if __name__ == '__main__':
    port = 2000
    echo_server(port)
