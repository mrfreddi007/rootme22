#!/usr/bin/env python3
"""Yet Another Reverse Polish Notation calculator.
I hope it doesn't suck too much.
This python script is published under the terms of the WTFPL.
More information on: http://www.wtfpl.net/about/
(Compatible with Python 3.7, 3.8, 3.9, 3.10 & 3.11)
"""
import argparse
import sys
import math
from collections import _chain
import readline
import rlcompleter  # noqa


class InvalidOperationError(Exception):
    "Invalid operation"

    def __init__(self, message):
        super().__init__(message)
        self.digits = []


class OneDigitError(InvalidOperationError):
    "Invalid operation with a 'one-digit' operation"

    def __init__(self, message, digit=None):
        super().__init__(message)
        self.digits = [digit]


class TwoDigitError(InvalidOperationError):
    "Invalid operation with a 'two-digit' operation"

    def __init__(self, message, digit1=None, digit2=None):
        super().__init__(message)
        self.digits = [digit2, digit1]


def to_float(item):
    return float(item.replace(",", "."))


def is_numeric(item):
    "Return True if the item is numeric"
    try:
        to_float(item)
        return True
    except (ValueError, TypeError):
        pass
    return False


class Rpn:
    "Reverse Polish Notation class"

    def __init__(self):
        self.stack = []
        self.NO_ITEM_OPS = {
            "drop": self.drop,
            "clear": self.clear,
            "e": self.e,
            "pi": self.pi,
            "help": self.help,
        }
        self.ONE_ITEM_OPS = {
            "sqrt": self.sqrt,
            "dup": self.dup,
            "floor": self.floor,
            "ceil": self.ceil,
            "abs": self.abs,
            "ln": self.ln,
            "sin": self.sin,
            "cos": self.cos,
            "tan": self.tan,
        }
        self.TWO_ITEM_OPS = {
            "+": self.plus,
            "-": self.minus,
            "*": self.multiply,
            "/": self.divide,
            "^": self.power,
            "**": self.power,
            "pwr": self.power,
            "swap": self.swap,
            "log": self.log,
            "mod": self.mod,
            "%": self.mod,
            "divmod": self.divmod,
        }
        self.ALL_OPS = list(
            _chain(
                self.TWO_ITEM_OPS.keys(),
                self.ONE_ITEM_OPS.keys(),
                self.NO_ITEM_OPS.keys(),
            )
        )

    def help(self):
        "Display help"
        operators = filter(lambda x: x != "help", self.ALL_OPS)
        print("Available operators:")
        print(", ".join(operators))

    def handle_op(self, operator):
        """
        Handle any operation known by the calculator.
        """
        # If not in the operators, abort
        if operator not in self.ALL_OPS:
            raise InvalidOperationError(f"Error: `{operator}` unknown")

        if operator in self.NO_ITEM_OPS:
            func = self.NO_ITEM_OPS[operator]
            return func()
        elif operator in self.ONE_ITEM_OPS:
            if len(self.stack) < 1:
                raise InvalidOperationError(f"{operator}: Invalid stack length")
            digit = self.stack.pop()
            func = self.ONE_ITEM_OPS[operator]
            return func(digit)
        elif operator in self.TWO_ITEM_OPS:
            if len(self.stack) < 2:
                raise InvalidOperationError(f"{operator}: Invalid stack length")
            digit1, digit2 = self.stack.pop(), self.stack.pop()
            func = self.TWO_ITEM_OPS[operator]
            return func(digit1, digit2)

    # -- Stack operations
    def push(self, input_buffer):
        "Push items in the stack and process them if they're operators"
        result = []
        items = input_buffer.split()
        for item in items:
            try:
                if is_numeric(item):
                    self.stack.append(to_float(item))
                else:
                    result = self.handle_op(item)
            except InvalidOperationError as msg:
                print(msg)
                # catch digits back
                if msg.digits:
                    self.stack.extend(msg.digits)

            while result:
                self.stack.append(result.pop())

        print(f"stack: {self.stack}")

    def drop(self):
        "Drop the last inserted item out of the stack"
        if not self.stack:
            raise InvalidOperationError("drop: Invalid stack length")
        # drop the "drop" command
        self.stack.pop()

    def clear(self):
        "Clear the stack"
        self.stack = []

    def swap(self, digit1, digit2):
        "Swap the last two items in the stack"
        return [digit2, digit1]

    def dup(self, digit1):
        "Duplicates the last item in the stack"
        return [digit1, digit1]

    def get_status(self):
        "Return the last item in the stack (should be a digit)"
        if self.stack:
            return str(self.stack[-1])
        return "The stack is empty."

    # -- Math operators
    def plus(self, digit1, digit2):
        "Add two digits"
        return [digit1 + digit2]

    def minus(self, digit1, digit2):
        "Substract two digits"
        return [digit2 - digit1]

    def multiply(self, digit1, digit2):
        "Multiply two digits"
        return [digit1 * digit2]

    def divide(self, digit1, digit2):
        "Divide two digits"
        try:
            return [digit2 / digit1]
        except ZeroDivisionError:
            raise TwoDigitError(
                "divide: Division by Zero", digit1=digit1, digit2=digit2
            )

    def e(self):
        "Put 'e' constant in the stack"
        return [math.e]

    def pi(self):
        "Put 'pi' constant in the stack"
        return [math.pi]

    def sqrt(self, digit):
        "Extract the square root of the digit"
        try:
            return [math.sqrt(digit)]
        except ValueError as e:
            raise OneDigitError(f"sqrt: {e}", digit)

    def floor(self, digit):
        "Rounding down the digit"
        return [math.floor(digit)]

    def ceil(self, digit):
        "Rounding up the digit"
        return [math.ceil(digit)]

    def abs(self, digit):
        "Absolute value of the digit"
        return [math.fabs(digit)]

    def ln(self, digit):
        "Natural logarithm"
        try:
            return [math.log(digit)]
        except ValueError as e:
            raise OneDigitError(f"ln: {e}", digit)

    def log(self, digit1, digit2):
        "N-based logarithm"
        try:
            return [math.log(digit2, digit1)]
        except (ValueError, ZeroDivisionError) as e:
            raise TwoDigitError(f"ln: {e}", digit1, digit2)

    def power(self, digit1, digit2):
        "Raise the digit2 to the power of the digit1"
        return [digit2**digit1]

    def mod(self, digit1, digit2):
        "Remainder of the division"
        return [digit2 % digit1]

    def divmod(self, digit1, digit2):
        "Quotient and remainder"
        quotient = self.divide(digit1, digit2).pop()
        quotient = float(int(quotient))
        remainder = self.mod(digit1, digit2).pop()
        return [remainder, quotient]

    def sin(self, digit1):
        "Sinus"
        return [math.sin(digit1)]

    def cos(self, digit1):
        "Cosinus"
        return [math.cos(digit1)]

    def tan(self, digit1):
        "Tangent"
        return [math.tan(digit1)]


if __name__ == "__main__":  # pragma: no cover

    rpn = Rpn()

    parser = argparse.ArgumentParser("Reverse Polish Notation calculator")
    parser.add_argument(
        "operands",
        nargs="*",
        help="if you only need to calculate a simple expression, just type your operands on the command line (e.g.: `rpn.py '16 3 * 5 +'`)",
    )
    args = parser.parse_args()
    if args.operands:
        rpn.push(" ".join(args.operands))
        print(rpn.get_status())
        sys.exit(0)

    def completer(text, state):
        options = [i for i in rpn.ALL_OPS if i.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None

    if "libedit" in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)

    while True:
        try:
            input_buffer = input("> ")
            if input_buffer.lower() == "exit":
                break
            rpn.push(input_buffer)
            print(rpn.get_status())
        except (EOFError, KeyboardInterrupt):
            break
    print("\nbye")