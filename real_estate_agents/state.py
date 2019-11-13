import sys
import time 
import random
import argparse
# same dir
from server_key import ServerKey
import utils as F
# blockchain dir
import blockchain.utils as utils
from blockchain.wallet import Wallet
from blockchain.wallets import Wallets
from blockchain.blockchain import Blockchain
from blockchain.transaction import UTXOTx, CoinbaseTx

States = ['Wait', 'Pre_prepare', 'Prepare', 'Commit', 'Gensig']

""" States Transition
    1. primary : 
        Ask for transaction :
            Wait -> pre_prapare -> prepare -> commit -|
            ^-----------------------------------------|
        Ask for key pair :
            Wait -> gensig -|
            ^---------------|
        Ask for balance ; create wallet :
            Wait -|
            ^-----|

    2. backups :
        Wait -> prepare -> commit -|
        ^--------------------------|
    3. view = {primary, backups}
"""


class State(object):
    """ Represents a new Block object.
    Args:
        _current_state (str): The current state
    Attributes:
        _timestamp (bytes): Creation timestamp of Block.
    """
    def __init__(self, primary=False, number=4, clisocket=None):
        self._current_state = 'Wait'
        self.number = number
        self.primary = primary
        self.client_socket = clisocket
        self.clisocket = None
        self.false_tolerance = (number-1)//3
        self.limit = self.number - 1 - self.false_tolerance
        self.key = ServerKey()
        self.command = None

        self.history = []
        self.result = []
        self.blockchain = None
        self.block = None

    def GO(self, sockets):
        if self._current_state == 'Wait':
            self.wait(sockets)
        elif self._current_state == 'Gensig':
            self.gensig(sockets)   
        elif self._current_state == 'Pre_prepare':
            self.pre_prepare(sockets)
        elif self._current_state == 'Prepare':
            self.prepare(sockets)
        elif self._current_state == 'Commit':
            self.commit(sockets)
    
    def wait(self, sockets):
        print('State 1 : Wait ...')
        if self.primary:
            # receive message from clients
            ## format = 'Get key pair'
            ## format = 'Create wallet name'
            ## format = 'get balance name'
            ## format = 'New request'
            self.client_socket.listen(0)
            client, _ = self.client_socket.accept()
            self.clisocket = client
            cli_message = self.clisocket.recv(2048)
            print('\tReceive message from the client.')

            if b'key pair' in cli_message:
                self._current_state = 'Gensig'
            elif b'Create wallet' in cli_message:
                data = cli_message.decode('utf-8')
                data = data.split()
                check, privatekey, address  = F.create_wallet(data[-1])
                # send 2 times, encode by 'utf-8'
                if check:
                    self.clisocket.send(privatekey)
                    self.clisocket.send(address.encode('utf-8'))
                else:
                    self.clisocket.send(b'False')
                self._current_state = 'Wait'
            elif b'get balance' in cli_message:
                balance = F.get_balance_from_name(cli_message.decode('utf-8').split()[-1])
                self.clisocket.send(balance.encode('utf-8'))
                self._current_state = 'Wait'
            else:
                sockets[-1][0].send(b'New request !')
                self._current_state = 'Pre_prepare'
        else:
            # receive message from primary
            data = sockets[0][0].recv(2048)
            self.command = data
            print('\tReceive message from the primary.')
            self._current_state = 'Prepare'

    def gensig(self, sockets):
        print('State 1.5 : Generate signature')
        # Generate a key pair and send back to the client
        ## format = 'CoinType'
        CoinType = self.clisocket.recv(2048).decode('utf-8')
        sign = self.key.generateTypeSign(CoinType)
        self.clisocket.send(sign)
        self._current_state = 'Wait'

    def pre_prepare(self, sockets):
        print('State 2 : Preprepare')
        # build block
        data = self.clisocket.recv(2048)
        ## parse data
        ## format = 'subsidy cointype name typesig (addcoin)'
        ## format = 'from_name to_name cointype amount sig (send)'
        for s in sockets[:-1]:
            s[0].send(data)
        self.command = data
        sockets[-1][0].send(b'New request !')
        self._current_state = 'Prepare'

    def prepare(self, sockets):
        print('State 3 : Prepare')
        ## send
        '''
        for s in sockets:
            s[0].send(b'Received')
        ## receive
        for s in sockets[:-1]: 
            _ = s[0].recv(2048)
        '''
        print('Received from all the other nodes.')

        self._current_state = 'Commit'
        
    def commit(self, sockets):
        print('State 4 : Commit')
        # calculate and send to other people
        ## calculate
        result = F.evaluate(self.command, self.key)
        ## send
        for s in sockets:
            s[0].send(result.encode('utf-8'))
        ## receive from the others except the control panel
        agree = 0
        for s in sockets[:-1]: 
            data = s[0].recv(2048)
            agree += 1 if data == b'Agree' else 0
        print('\tAgree : {}, Disagree : {}  => {}'.format(agree, 3-agree, agree>=self.limit))

        # Primary build block
        if self.primary :
            # Commit success
            if agree>=self.limit:
                # Create a block and add into blockchain(dump)
                ## format = 'subsidy(int) cointype name typesig (addcoin)'
                ## format = 'from_name to_name cointype amount(int) sig (send)'
                comList = self.command.split(b'   ')
                if comList[-1] == b'(send)':
                    bc = Blockchain()
                    newBlock = F.send(comList[0].decode('utf-8'), comList[1].decode('utf-8'), comList[2].decode('utf-8'), int(comList[3].decode('utf-8')))
                    bc._block_put(newBlock)
                    from_balance = F.get_balance_from_name(comList[0].decode('utf-8'))
                    self.clisocket.send(from_balance.encode('utf-8'))
                elif self.blockchain == None:
                    F.create_blockchain(int(comList[0].decode('utf-8')), comList[1].decode('utf-8'), comList[2].decode('utf-8'))
                    self.blockchain = 1
                    self.clisocket.send("Add coin SUCCESS".encode('utf-8'))
                else:
                    F.add_coin(int(comList[0].decode('utf-8')), comList[1].decode('utf-8'), comList[2].decode('utf-8'))
                    self.clisocket.send("Add coin SUCCESS".encode('utf-8'))
            # Commit failed
            else:
                self.clisocket.send("FAILED".encode('utf-8'))



            
        self._current_state = 'Wait'


