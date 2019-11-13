import pickle


class Wallets(object):
    """ Wallet stores private and public keys.
    Args:
    Attributes:
        wallets (dict): a wallets dict.
    """

    wallet_file = '../database/wallet.dat'
    namelist_file = '../database/namelist.dat'

    def __init__(self):

        try:
            with open(self.wallet_file, 'rb') as f:
                self.wallets = pickle.load(f)
            with open(self.namelist_file, 'rb') as f:
                self.namelist = pickle.load(f)
        except FileNotFoundError:
            self.wallets = {}
            self.namelist = {}

    def add_wallet(self, addr, wallet):
        self.wallets[addr] = wallet
        self.namelist[wallet._name] = addr

    def get_addresses(self):
        return [addr for addr in self.wallets.keys()]

    def get_address_from_name(self, name):
        return self.namelist[name]


    def get_wallet_from_name(self, name):
        return self.wallets[self.namelist[name]]

    def get_wallet_from_addr(self, addr):
        return self.wallets[addr]

    def save_to_file(self):
        with open(self.wallet_file, 'wb') as f:
            pickle.dump(self.wallets, f)
        with open(self.namelist_file, 'wb') as f:    
            pickle.dump(self.namelist, f)
