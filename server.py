import socket
import click
import logging
import os
import sys

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
        if data:
            log.info("Data: %s" % data)
            client.send(data)
            log.info("sent %s bytes back to %s" % (data, address))
        # end connection
        client.close()


if __name__ == '__main__':
    port = 2000
    echo_server(port)
