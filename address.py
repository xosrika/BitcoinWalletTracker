from termcolor import colored


class Address:
    def __init__(
        self, address_hash, num_trans, total_received, total_sent, final_balance
    ):
        self.address_hash = address_hash
        self.num_trans = num_trans
        self.total_received = total_received
        self.total_sent = total_sent
        self.final_balance = final_balance
        self.transactions = None

    def set_transactions(self, transactions):
        self.transactions = transactions

    def list_transactions(self):
        res = "Transactions: "
        for tran in self.transactions:
            res += "\n\t" + str(tran)

        return res

    def get_transatcion(self, ind):
        return self.transactions[ind]

    def divide_transactions(self):
        self.transaction_recieved = []
        self.transaction_spent = []

        for tr in self.transactions:
            if not list(
                filter(lambda s: s.address == self.address_hash, tr.input_list)
            ):
                self.transaction_recieved.append(tr)
            else:
                self.transaction_spent.append(tr)

        self.check_most_friquent_recievers()
        self.check_most_friquent_senders()

    def check_most_friquent_recievers(self):
        friquent_recievers = {}
        for tr in self.transaction_spent:
            for tr_i in tr.output_list:
                if tr_i.address in friquent_recievers:
                    friquent_recievers[tr_i.address] = (
                        friquent_recievers[tr_i.address][0] + tr_i.value,
                        friquent_recievers[tr_i.address][1] + 1,
                    )
                else:
                    friquent_recievers[tr_i.address] = (tr_i.value, 1)

        friquent_recievers = sorted(
            friquent_recievers.items(), key=lambda kv: kv[1]
        )
        print(friquent_recievers)

    def check_most_friquent_senders(self):
        friquent_sender = {}
        for tr in self.transaction_recieved:
            for tr_i in tr.input_list:
                if tr_i.address in friquent_sender:
                    friquent_sender[tr_i.address] = (
                        friquent_sender[tr_i.address][0] + tr.result,
                        friquent_sender[tr_i.address][1] + 1,
                    )
                else:
                    friquent_sender[tr_i.address] = (tr.result, 1)

        friquent_sender = sorted(friquent_sender.items(), key=lambda kv: kv[1])
        print(friquent_sender)

    def get_dollar_balanace(self, bitcoin_price):
        return self.final_balance * bitcoin_price / 100000000.0

    def __str__(self):
        return "Bitcoin address: {} has total balance of: {} ({} Bitcoins).\
\n\tIt performed {} transaction: Receved {} and sent {}".format(
            colored(self.address_hash, "yellow", attrs=["underline", "bold"]),
            colored(self.final_balance, "cyan"),
            colored(format(self.final_balance / 100000000.0, ".3f"), "cyan"),
            colored(self.num_trans, "blue"),
            colored(self.total_received, "green"),
            colored(self.total_sent, "red"),
        )
