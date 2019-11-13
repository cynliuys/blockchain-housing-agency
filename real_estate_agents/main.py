import os 
import sys
import time
import socket
import numpy as np
from argparse import ArgumentParser

from state import State


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--primary", help="This node is a primary(True) or a backup(False).", \
                            required=False, type=str, default='False')
    parser.add_argument("-n", "--number", help="The number of nodes.", required=True, type=int, default=0)
    parser.add_argument("-crp", "--create-ports", nargs='+', help="The ports need to be created.", required=False, type=list, default=[])
    parser.add_argument("-conp", "--connect-ports", nargs='+', help="The ports need to be connected.", required=False, type=list, default=[])
    parser.add_argument("-clip", "--client-port", help="The client port", required=False, type=int, default=-1)
    args = parser.parse_args()

    primary = False if args.primary == 'False' else True
    if primary and args.client_port == -1:
        print('The client port needs to be set if this node is primary')
        print('eg. python3 main.py -p True -n 4 -crp 10000 10001 10002 -conp 10003 -clip 10010')
        sys.exit()

    if args.number != len(args.create_ports) + len(args.connect_ports):
        print('The number of nodes ned to be consistent with the number of ports.')
        print('eg. python3 main.py -p True -n 4 -crp 10000 10001 10002 -conp 10003 -clip 10010')
        sys.exit()
    
    # ports connection
    print('sockets are setting now...')
    HOST = '127.0.0.1'
    crp = [int(''.join(port)) for port in args.create_ports]
    conp = [int(''.join(port)) for port in args.connect_ports]

    sockets = []
    ## connect first
    for i, port in enumerate(conp):
        s = [socket.socket(socket.AF_INET, socket.SOCK_STREAM), HOST, port, True] # True for conp
        s[0].connect((HOST, port))
        sockets.append(s)
        print('\tsocket(port={}) is connected'.format(port))
    ## create second
    for i, port in enumerate(crp):
        s = [socket.socket(socket.AF_INET, socket.SOCK_STREAM), HOST, port, False] # False for crp
        s[0].bind(('', port))
        sockets.append(s)
        print('\tsocket(port={}) is created'.format(port))
    ## sorted third
    sockets = sorted(sockets,key=lambda l:l[2], reverse=False)
    ## accept fourth
    for i, s in enumerate(sockets):
        if not s[3]:
            s[0].listen(0)
            client, _ = s[0].accept()
            sockets[i][0] = client
            print('{} is connected.'.format(s[2]))

    time.sleep(5)
    print('finish socket connecting')

    if primary:
        clisocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clisocket.bind(('',args.client_port))

        print('client socket(port={}) is created'.format(port))
        MyState = State(primary=primary, number=args.number, clisocket=clisocket)
    else :
        MyState = State(primary=primary, number=args.number)

    while True:
        MyState.GO(sockets)




    '''
    HOST = '127.0.0.1'
    PORT = 10003
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    while True:
        data = s.recv(1024)
        print(data)
        s.send(b'hello')
    '''

    
