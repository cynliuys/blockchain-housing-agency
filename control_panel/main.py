import os 
import sys
import time
import socket
import numpy as np
from argparse import ArgumentParser

from state import State


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-n", "--number", help="The number of nodes.", required=True, type=int, default=4)
    parser.add_argument("-lsp", "--ports", nargs='+', help="The list of ports of nodes.", required=True, type=list)

    args = parser.parse_args()
    
    if args.number != len(args.ports):
        print('The number of nodes ned to be consistent with the number of ports.')
        print('eg. python3 main.py -cp 10010 -n 4 -lsp 10003 10006 10008 10009')
        sys.exit()

    # setup connection
    print('Connection is setting now...')
    ports = [int(''.join(port)) for port in args.ports]
    sockets = []
    clients = []
    for i, port in enumerate(ports):
        sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        sockets[i].bind(('', port))
    print('- {} sockets are created.'.format(args.number))

    for s in sockets:
        s.listen(0)
    print('- {} sockets are running.'.format(args.number))

    for s in sockets:
        client, _ = s.accept()
        clients.append(client)
    print('- {} nodes are connected.'.format(args.number))
    
    # Start controlling
    MyState = State(args.number)
    while True:
        MyState.GO(clients)