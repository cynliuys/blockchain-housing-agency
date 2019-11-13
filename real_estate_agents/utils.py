import time 
import codecs
import binascii
import ecdsa
from server_key import ServerKey
import blockchain.utils as utils
from blockchain.wallet import Wallet
from blockchain.wallets import Wallets
from blockchain.blockchain import Blockchain
from blockchain.transaction import UTXOTx, CoinbaseTx

def get_client(str):
    ls = str.split()
    return ls[-2]


def get_balance_from_name(name):
    bc = Blockchain()

    wallets = Wallets()
    if not name in wallets.namelist.keys():
        return ''
    address = wallets.get_address_from_name(name)

    pubkey_hash = utils.address_to_pubkey_hash(address)
    balance = dict()
    UTXOs = bc.find_utxo(pubkey_hash)

    for out in UTXOs:
        if out.cointype not in balance.keys():
            balance[out.cointype] = 0 
        balance[out.cointype] += out.value

    data = ''
    for k,v in balance.items():
        data = data + k + ':$' + str(v)  + '\n'
    return data


def get_balance(address):
    bc = Blockchain()

    pubkey_hash = utils.address_to_pubkey_hash(address)
    balance = dict()
    UTXOs = bc.find_utxo(pubkey_hash)

    for out in UTXOs:
        if out.cointype not in balance.keys():
            balance[out.cointype] = 0 
        balance[out.cointype] += out.value

    print('Balance of {0}:'.format(address))
    print('----------------------')
    for c,b in balance.items():
        print('{0}: {1}'.format(c, b))

def create_wallet(name):
    wallets = Wallets()
    if name in wallets.namelist.keys():
        return False, 1,1

    wallet = Wallet(name)
    address = wallet.address
    wallets.add_wallet(address, wallet)
    wallets.save_to_file()
    return True, wallet._private_key, wallet._address


def create_blockchain(subsidy, cointype, name):
    wallets = Wallets()
    address = wallets.get_address_from_name(name)
    bc = Blockchain(subsidy, cointype, address)
    bc._block_put(bc.genesis)


def add_coin(subsidy, cointype, name):
    wallets = Wallets()
    address = wallets.get_address_from_name(name)

    bc = Blockchain()
    cb_tx = CoinbaseTx(address, subsidy, cointype).set_id()
    newBlock = bc.MineBlock([cb_tx])
    bc._block_put(newBlock)
    
    
def print_chain(height=-1):
    bc = Blockchain()

    for block in bc.blocks:
        if (height == -1) or (height == block.height):
            print("Prev. hash: {0}".format(block.prev_block_hash))
            print("Hash: {0}".format(block.hash))
            pow = Pow(block)
            print("PoW: {0}".format(pow.validate()))
            print("Height: {0}\n".format(block.height))


def send(from_name, to_name, cointype, amount):
    bc = Blockchain()

    wallets = Wallets()
    from_addr = wallets.get_address_from_name(from_name)
    to_addr = wallets.get_address_from_name(to_name)

    tx = UTXOTx(from_addr, to_addr, int(amount), cointype, bc).set_id()
    block = bc.MineBlock([tx])
    return block


def evaluate(command, key):
    ## format = 'subsidy cointype name typesig (addcoin)'
    ## format = 'from_name to_name cointype amount sig (send)'
    command = command.split(b'   ')
    print(command)
    if command[-1] == b'(addcoin)':
        wallets = Wallets()
        if not command[2].decode('utf-8') in wallets.namelist.keys():
            return 'Disagree'
        if key.verifyTypeSign(command[1].decode('utf-8'), command[3]):
            return 'Agree'
        return 'Disagree'

    elif command[-1] == b'(send)':
        bc = Blockchain()
        wallets = Wallets()
        if not command[0].decode('utf-8') in wallets.namelist.keys():
            return 'Disagree'
        if not command[1].decode('utf-8') in wallets.namelist.keys():
            return 'Disagree'
        if not check_tx(bc, command[0].decode('utf-8'), command[2].decode('utf-8'), command[3].decode('utf-8')):
            return 'Disagree'
        wallet = wallets.get_wallet_from_name(command[0].decode('utf-8'))
        '''Wallet public key not good
        vk = ecdsa.VerifyingKey.from_string(wallet._public_key, curve=ecdsa.SECP256k1)
        if not vk.verify(command[-2], 'yes'):
            return 'Disagree'
        '''
        return 'Agree'


def check_tx(bc, from_name, cointype, amount):

    wallets = Wallets()
    wallet = wallets.get_wallet_from_name(from_name)
    pubkey_hash = utils.hash_public_key(wallet.public_key)

    acc, valid_outputs = bc.find_spendable_outputs(pubkey_hash, int(amount), cointype)
    if acc < int(amount):
        return False
    return True


