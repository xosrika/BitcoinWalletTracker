import datetime

from termcolor import colored


class Transaction:
    def __init__(
        self, hash, input_size, output_size, fee, result, balance, time
    ):
        self.hash = hash
        self.input_size = input_size
        self.output_size = output_size
        self.fee = fee
        self.result = result
        self.balance = balance
        self.time = datetime.datetime.fromtimestamp(time)
        self.input_list = None
        self.output_list = None

    def set_inputs(self, inputs):
        self.input_list = inputs
        self.input_list.sort()

    def set_outputs(self, outputs):
        self.output_list = outputs
        self.output_list.sort()

    def list_inputs(self, limit):
        res = "Inputs: "
        for tran in self.input_list[:limit]:
            res += "\n\t\t\t" + str(tran)
        if self.input_size > limit:
            res += "\n\t\t\t..."
        return res

    def list_outputs(self, limit):
        res = "Outputs: "
        for tran in self.output_list[:limit]:
            res += "\n\t\t\t" + str(tran)
        if self.output_size > limit:
            res += "\n\t\t\t..."
        return res

    def str_wallet(self):
        return "Transaction hash: {}... happened {}: has result {} and final \
balance is {}.\n\tInput size is {} output size is {} payed in fees :{}\
\n\t\t{}\n\t\t{}".format(
            colored(self.hash[:7], "yellow"),
            colored(str(self.time), "blue", "on_white"),
            colored(str(self.result), "red" if self.result < 0 else "green"),
            colored(self.balance, "cyan"),
            colored(
                self.input_size,
                "white",
                "on_green",
                attrs=["underline", "bold"],
            ),
            colored(
                self.output_size, "white", "on_red", attrs=["underline", "bold"]
            ),
            self.fee,
            self.list_inputs(3),
            self.list_outputs(3),
        )

    def str_tran(self):
        return "Transaction hash: {} happened {}: \
\n\tInput size is {} output size is {} payed in fees :{}\
\n\t\t{}\n\t\t{}".format(
            colored(self.hash, "yellow", attrs=["underline"]),
            colored(str(self.time), "blue", "on_white"),
            colored(
                self.input_size,
                "white",
                "on_green",
                attrs=["underline", "bold"],
            ),
            colored(
                self.output_size, "white", "on_red", attrs=["underline", "bold"]
            ),
            self.fee,
            self.list_inputs(self.input_size),
            self.list_outputs(self.output_size),
        )

    def __str__(self):
        if self.balance is not None:
            return self.str_wallet()
        return self.str_tran()
