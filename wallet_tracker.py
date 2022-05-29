from termcolor import colored

from bitcoin_api import BitcoinAPI


class WalletTracker:
    def __init__(self):
        self.wallets = []
        self.curr_wallet = None
        self.curr_tran = None

    def insert_address(self, address):
        self.wallets.append(address)

    def get_curr_wallet(self):
        return self.curr_wallet

    def pop_address(self):
        self.wallets.pop()

    def check_last_wallet(self):
        self.curr_wallet = BitcoinAPI.get_bitcoin_wallet_transactions(
            self.wallets[-1]
        )
        print(self.curr_wallet)

    def check_last_wallet_transactions(self):
        self.curr_wallet = BitcoinAPI.get_bitcoin_wallet_transactions(
            self.wallets[-1]
        )
        print(self.curr_wallet.list_transactions())

    def chech_transaction(self, transaction_hash):
        self.curr_tran = BitcoinAPI.get_transaction(transaction_hash)
        print(self.curr_tran)

    def get_bitcoin_price(self, bitcoins):
        price = BitcoinAPI.get_bitcoin_price()

        print(
            "{} Bitcoins now are equal to {} Dollars.".format(
                colored(format(bitcoins, ".5f"), "cyan"),
                colored(format(bitcoins * price, ".2f"), "blue"),
            )
        )

    def get_balance(self):
        bitcoin_price = BitcoinAPI.get_bitcoin_price()
        wallet_balance = self.curr_wallet.get_dollar_balanace(bitcoin_price)

        print(
            "Bitcoin address: {} has total balance of: {}.\
\n\t1 Bitcoin price right now is {} dollars".format(
                colored(
                    self.curr_wallet.address_hash,
                    "yellow",
                    attrs=["underline", "bold"],
                ),
                colored(wallet_balance, "cyan"),
                colored(bitcoin_price, "blue"),
            )
        )
