from termcolor import colored


class InputTransaction:
    def __init__(self, address, value, curr_address=None):
        self.address = address
        self.value = value
        self.curr_address = curr_address

    def __lt__(self, other):
        return self.value > other.value

    def __str__(self):
        attrs = ["underline", "bold"]
        if self.curr_address == self.address:
            attrs.append("blink")
        return "Address: {}... with value: {}".format(
            colored(self.address[:7], "yellow", attrs=attrs),
            colored(self.value, "magenta"),
        )
