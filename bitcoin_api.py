import json
import urllib.request

import pandas

from address import Address
from input_transaction import InputTransaction
from output_transaction import OutputTransaction
from transaction import Transaction


class BitcoinAPI:
    def fill_transactions(transaction, data, curr_address):
        inputs = [None] * transaction.input_size
        for i, transaction_input in enumerate(data["inputs"]):
            transaction_input_output = transaction_input["prev_out"]
            inputs[i] = InputTransaction(
                transaction_input_output["addr"],
                transaction_input_output["value"],
                curr_address,
            )
        transaction.set_inputs(inputs)

        outputs = [None] * transaction.output_size
        for i, transaction_output in enumerate(data["out"]):
            outputs[i] = OutputTransaction(
                transaction_output["addr"],
                transaction_output["value"],
                curr_address,
            )
        transaction.set_outputs(outputs)

    def get_bitcoin_wallet_transactions(your_btc_address):
        url = (
            "https://blockchain.info/rawaddr/" + your_btc_address + "?limit=10"
        )
        df = pandas.read_json(url)

        wallet = Address(
            df["address"][0],
            df["n_tx"][0],
            float(df["total_received"][0]),
            float(df["total_sent"][0]),
            float(df["final_balance"][0]),
        )

        transactions = [None] * len(df["txs"])
        for idx, json_transaction in enumerate(df["txs"]):
            transactions[idx] = Transaction(
                json_transaction["hash"],
                json_transaction["vin_sz"],
                json_transaction["vout_sz"],
                float(json_transaction["fee"]),
                float(json_transaction["result"]),
                float(json_transaction["balance"]),
                json_transaction["time"],
            )

            BitcoinAPI.fill_transactions(
                transactions[idx], json_transaction, your_btc_address
            )

        wallet.set_transactions(transactions)

        return wallet

    def get_transaction(transaction_hash):
        transaction = None

        with urllib.request.urlopen(
            "https://blockchain.info/rawtx/" + transaction_hash
        ) as url:
            data = json.loads(url.read().decode())

            transaction = Transaction(
                data["hash"],
                data["vin_sz"],
                data["vout_sz"],
                data["fee"],
                None,
                None,
                data["time"],
            )

            BitcoinAPI.fill_transactions(transaction, data, None)

        return transaction

    def get_bitcoin_price():
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        data = pandas.read_json(url, typ="series")
        return float(data["price"])
