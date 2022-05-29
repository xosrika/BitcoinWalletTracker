import argparse
import traceback

from common_addresses import CommonAddresses
from wallet_tracker import WalletTracker


class WalletInputParser:
    def check_wallet(self, args):
        if args.u:
            args.a = CommonAddresses.COMMON_ADDRESSES[args.u]

        self.wallet_tracker.insert_address(args.a)
        self.wallet_tracker.check_last_wallet()

    def check_wallet_transactions(self, args):
        self.wallet_tracker.check_last_wallet_transactions()

    def pop_last_wallet(self, args):
        self.wallet_tracker.pop_address()

    def choose_wallet_transaction(self, args):
        if args.i is not None:
            args.hash = (
                self.wallet_tracker.get_curr_wallet()
                .get_transatcion(args.i)
                .hash
            )

        self.wallet_tracker.chech_transaction(args.hash)

    def check_transaction_wallet(self, args):
        tran_elem = None
        if args.i:
            tran_elem = self.wallet_tracker.curr_tran.input_list[args.i]
        else:
            tran_elem = self.wallet_tracker.curr_tran.output_list[args.o]

        self.wallet_tracker.insert_address(tran_elem.address)
        self.wallet_tracker.check_last_wallet()

    def get_wallet_balance(self, args):
        self.wallet_tracker.get_balance()

    def bitcoin_to_dollar(self, args):
        bitcoins = args.b
        if args.s:
            bitcoins /= 100000000
        self.wallet_tracker.get_bitcoin_price(bitcoins)

    def check_transaction_wallet_fromtransactions(self, args):
        transatcion = self.wallet_tracker.curr_wallet.transactions[args.t]
        address = None
        if args.i is not None:
            address = transatcion.input_list[args.i].address
        else:
            address = transatcion.output_list[args.o].address

        self.wallet_tracker.insert_address(address)
        self.wallet_tracker.check_last_wallet()

    def __init__(self):
        self.wallet_tracker = WalletTracker()

        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers()

        parser_wallet = subparsers.add_parser("wallet")
        parser_wallet_group = parser_wallet.add_mutually_exclusive_group(
            required=True
        )
        parser_wallet_group.add_argument("-a", type=str)
        parser_wallet_group.add_argument("-u", type=str, default=None)
        parser_wallet_group.add_argument("-i", type=int, default=None)
        parser_wallet.set_defaults(func=self.check_wallet)

        parser_trans = subparsers.add_parser("trans")
        parser_trans.set_defaults(func=self.check_wallet_transactions)

        parser_pop = subparsers.add_parser("pop")
        parser_pop.set_defaults(func=self.pop_last_wallet)

        parser_tran = subparsers.add_parser("tran")
        parser_tran_group = parser_tran.add_mutually_exclusive_group(
            required=True
        )
        parser_tran_group.add_argument("-i", type=int, default=None)
        parser_tran_group.add_argument("--hash", type=str, default=None)
        parser_tran.set_defaults(func=self.choose_wallet_transaction)

        parser_tran_wallet = subparsers.add_parser("check")
        tran_wallet_group = parser_tran_wallet.add_mutually_exclusive_group(
            required=True
        )
        tran_wallet_group.add_argument("-i", type=int, default=None)
        tran_wallet_group.add_argument("-o", type=int, default=None)
        parser_tran_wallet.set_defaults(func=self.check_transaction_wallet)

        parser_balance = subparsers.add_parser("balance")
        parser_balance.set_defaults(func=self.get_wallet_balance)

        parser_dollar = subparsers.add_parser("dollar")
        parser_dollar.add_argument("-b", type=float, default=1.0)
        parser_dollar.add_argument("-s", action="store_true")
        parser_dollar.set_defaults(func=self.bitcoin_to_dollar)

        parser_tran_check = subparsers.add_parser("tran_check")
        parser_tran_check.add_argument("-t", type=int, default=0)
        parser_tran_check.add_argument("-i", type=int)
        parser_tran_check.add_argument("-o", type=int, default=0)
        parser_tran_check.set_defaults(
            func=self.check_transaction_wallet_fromtransactions
        )

    def run(self):
        while True:
            st = input("Please enter your command: ")
            if st == "exit":
                return
            try:
                args = self.parser.parse_args(st.split())
                args.func(args)
            except Exception:
                traceback.print_exc()
            except SystemExit:
                print("Ignoring SystemExit")
