import logging
import os
import socket
import sys
from multiprocessing import Process, Value, Array

import click

log = logging.getLogger("application")
hdlr = logging.FileHandler(os.getcwd() + "\\client_logs.txt")
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
hdlr.setFormatter(formatter)
log.addHandler(hdlr)
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.INFO)


host = 'localhost'


def echo_client(port, numbers):
    """ A simple echo client """
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the server
    server_address = (host, port.value)
    log.info("Connecting to %s port %s" % server_address)
    sock.connect(server_address)

    # Send data
    try:
        # Send data
        nums = numbers[:]
        sock.sendall(bytes(str(nums), encoding='utf8'))

        data = sock.recv(4096)
        log.info("Received: %s" % str(data))
    except socket.error as e:
        log.error("Socket error: %s" % str(e))
    except Exception as e:
        log.error("Other exception: %s" % str(e))
    finally:
        log.info("Closing connection to the server")
        sock.close()


if __name__ == '__main__':

    port = 2000
    numbers = []
    howmanynumbers = click.prompt('Enter number of integers you want to process', type=int)
    for _ in range(howmanynumbers):
        numbers.append(click.prompt('Please enter a valid integer', type=int))
    num = Value('i', port)
    arr = Array('i', numbers)
    p = Process(target=echo_client, args=(num, arr))

    p.start()
    p.join()
