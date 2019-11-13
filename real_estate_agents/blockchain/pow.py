# finished
import hashlib
import sys

import blockchain.utils as utils

class Pow(object):
    """
    Args:
        block (Block object)
    Attributes:
        _block (Block object): a Block object.
        _target (int): a integer target need to less than it.
    """

    max_nonce = sys.maxsize # 2**63 - 1 on a 64-bit platform
    target_bits = 10

    def __init__(self, block):
        self._block = block
        self._target = 1<<(256-Pow.target_bits)

    def _prepare_data(self, nonce):
        data_lst = [self._block.prev_block_hash,
                    self._block.hash_transactions(), 
                    #the hash_transactions function has no decorator @property in front of it
                    #so don't forget to add the ()
                    self._block.timestamp,
                    str(self.target_bits),
                    str(nonce)
                    ]
        return utils.encode(''.join(data_lst))


    def validate(self):
        #validates a block's Pow
        data = self._prepare_data(self._block.nonce) # why can't we just return self._nonce
        hash_hex = utils.sum256(data)
        hash_int = int(hash_hex, 16)
        return True if hash_int<self._target else False


    def run(self):
        nonce = 0
        print('Mining a new block')
        
        while nonce < self.max_nonce:
            data = self._prepare_data(nonce) # encode the data using utf-8
            hash_hex = utils.sum256(data)
            sys.stdout.write("%s \r" % (hash_hex))
            hash_int = int(hash_hex, 16)
            
            if hash_int < self._target:
                break
            else:
                nonce += 1

        print('\n\n')
        return nonce, hash_hex


