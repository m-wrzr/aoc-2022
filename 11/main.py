import re
from math import prod
from typing import List

# monkeys operate based on how worried you are about each item

# "Starting items" lists your worry level for each item the monkey is currently holding in the order they will be inspected
# "Operation" shows how your worry level changes as that monkey inspects an item.
# "Test" shows how the monkey uses your worry level to decide where to throw an item next

# items go to end of next monkeys buffer

# Monkey 0:
#   Monkey inspects an item with a worry level of 79.
#     Worry level is multiplied by 19 to 1501.
#     Monkey gets bored with item. Worry level is divided by 3 to 500.
#     Current worry level is not divisible by 23.
#     Item with worry level 500 is thrown to monkey 3.

# Task: count number of times a monkey inspected an item for the two most active monkeys


class Monkey:
    # parse line input
    def __init__(self, _, items, operation, test, to_true, to_false):
        self.items: List[int] = [int(i) for i in re.findall(r"\d+", items)]
        self.operation: function = Monkey.parse_lambda(operation)
        self.mod: int = Monkey.parse_last(test)
        self.to_true: int = Monkey.parse_last(to_true)
        self.to_false: int = Monkey.parse_last(to_false)

    # get new worry level, ! removes item from list
    def remove_inspected(self, n_simplify: int = 1):
        return int(self.operation(self.items.pop(0)) / n_simplify)

    def get_next_monkey(self, item: int):
        return self.to_true if item % self.mod == 0 else self.to_false

    def __repr__(self):
        return f"Monkey({self.items}, {self.operation}, {self.mod}, {self.to_true}, {self.to_false})"

    @staticmethod
    # from line get symbol and return corresponding lambda
    def parse_lambda(operation: str):
        operation = operation.split(" ")

        symbol, amount = operation[-2], operation[-1]

        match symbol:
            case "+":
                return lambda x: x + int(amount) if amount.isdigit() else x + x
            case "*":
                return lambda x: x * int(amount) if amount.isdigit() else x * x
            case _:
                raise ValueError(f"Unknown operation: {symbol}")

    @staticmethod
    # get last number in string
    def parse_last(l: str):
        return int(l.split(" ")[-1])


# create sublists of lines with fixed length
lines = open("input.txt").read().splitlines()
lines = [[l for l in lines[i : i + 7] if l] for i in range(0, len(lines), 7)]

monkeys: List[Monkey] = [Monkey(*line) for line in lines]
monkeys_n_inspection: List[int] = len(monkeys) * [0]

# find largest common factor, to simplify worry level
monkey_mod = prod([m.mod for m in monkeys])

# a)
simplify_divisor, cycles = 3, 20

# b)
simplify_divisor, cycles = 1, 10000


for _ in range(cycles):
    for i, monkey in enumerate(monkeys):
        while monkey.items:
            item = monkey.remove_inspected(n_simplify=simplify_divisor)
            next = monkey.get_next_monkey(item)

            # simplify worry level for large numbers
            monkeys[next].items.append(item % monkey_mod)

            monkeys_n_inspection[i] += 1


print(f"Result: {prod(sorted(monkeys_n_inspection, reverse=True)[:2])}")
