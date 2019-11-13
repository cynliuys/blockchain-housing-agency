# finished
import time 
import hashlib
import pickle

import blockchain.utils as utils
from blockchain.pow import Pow

class Block(object):
    """
    Represents a new block object
    Args:
        transaction_lst (list): List of transaction.
        prev_block_hash (string): Hash of the previous Block. 
    Attributes:
        _timestamp (bytes): Creation timestamp of Block.
        _tx_lst (list): List of transaction.
        _prev_block_hash (bytes): Hash of the previous Block.
        _hash (bytes): Hash of the current Block.
        _nonce (int): A 32 bit arbitrary random number that is typically used once.
    """
    
    def __init__(self, transaction_lst, prev_height, prev_block_hash=''):
        self._timestamp = utils.encode(str(int(time.time())))
        self._tx_lst = transaction_lst
        self._prev_block_hash = utils.encode(prev_block_hash) 
        self._hash = None
        self._nonce = None
        self._height = prev_height + 1

    def __repr__(self):
        return 'Block(timestamp={0!r}, tx_lst={1!r}, prev_block_hash={2!r}, hash={3!r}, nonce={4!r}), height={5!r}'.format(
                self._timestamp, self._tx_lst, self._prev_block_hash, self._hash, self._nonce, self._height)

    @property
    def hash(self):
        return utils.decode(self._hash)

    @property
    def prev_block_hash(self):
        return utils.decode(self._prev_block_hash)

    @property
    def nonce(self):
        return str(self._nonce)
    
    @property
    def timestamp(self):
        return str(self._timestamp)

    @property
    def transactions(self):
        return self._tx_lst

    @property 
    def height(self):
        return self._height

    def pow_of_block(self):
        pow = Pow(self)
        nonce, hash = pow.run() # run Pow, returns nonce and hash_hex
        self._nonce, self._hash = nonce, utils.encode(hash)
        return self
        
    def hash_transactions(self): #hashing the transaction ids
        tx_hashs = []

        for tx in self._tx_lst:
            tx_hashs.append(tx.ID)
        
        return utils.sum256(utils.encode(''.join(tx_hashs)))

    def serialize(self): # why do we need this
        return pickle.dumps(self)

    def deserialize(self, data): # why do we need this
        """
        Deserializes the block.
        :param `bytes` data: The serialized data.
        :return: A Block object.
        :rtype: Block object.
        """
        return pickle.load(data)



