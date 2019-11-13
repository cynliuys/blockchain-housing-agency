import sys
import time 

States = ['Wait', 'Pre_prepare', 'Prepare', 'Commit']

""" States Transition
    Wait -> pre_prapare -> prepare -> commit -|
    ^-----------------------------------------|
"""


class State(object):
    """ Represents a new Block object.
    Args:
        _current_state (str): The current state
    Attributes:
        _timestamp (bytes): Creation timestamp of Block.
    """
    def __init__(self, number=4):
        self._current_state = 'Wait'
        self.number = number
        self.false_tolerance = (number-1)//3
        self.limit = self.number - self.false_tolerance

    def GO(self, clients):
        if self._current_state == 'Wait':
            self.wait(clients)
        elif self._current_state == 'Pre_prepare':
            self.pre_prepare(clients)
        elif self._current_state == 'Prepare':
            self.prepare(clients)
        elif self._current_state == 'Commit':
            self.commit(clients)

    def wait(self, clients):
        # receive message from primary
        print('State 1 : Wait ...')
        data = clients[0].recv(2048)
        print('\tReceive message from the primary')
        print('\t  primary: {}'.format(data.decode('utf-8')))

        self._current_state = 'Pre_prepare'

    def pre_prepare(self, clients):
        # receive message from primary
        print('State 2 : Preprepare')
        data = clients[0].recv(2048)
        print('\tReceive message from the primary')
        print('\t  primary: {}'.format(data.decode('utf-8')))
        
        self._current_state = 'Prepare'

    def prepare(self, clients):
        print('State 3 : Prepare')
        '''
        # receive message from all the nodes
        for id, client in enumerate(clients):
            data = client.recv(2048)
        '''
        print('Received from all the other nodes.')

        self._current_state = 'Commit'
        
    def commit(self, clients):
        print('State 4 : Commit')
        # receive message from all the nodes
        agree = 0
        for id, client in enumerate(clients):
            data = client.recv(2048)
            agree += 1 if b'Agree' in data else 0
            print('\tReceive message from the socket{}.'.format(id))
        print('\t  Agree : {}, Disagree : {}  => {}'.format(agree, 4-agree, agree>=self.limit))
        
        self._current_state = 'Wait'
