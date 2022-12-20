# mix the file, move each number forward or backward in the file a number of
# positions equal to the value of the number being moved.
# The list is circular
from __future__ import annotations

from typing import List


class LinkedItem:
    order: int
    value: int
    shift_move: int

    l: LinkedItem
    r: LinkedItem

    def __init__(self, order: int, value: int) -> None:
        self.order = order
        self.value = value

        # only need to shift mod list length
        self.shift_move = 0
        self.l = None
        self.r = None

    def shift_position(self):
        """only right shifts via modulo"""
        for _ in range(abs(self.shift_move)):
            l = self.l
            r = self.r
            rr = r.r

            l.r = r
            r.l = l
            r.r = self
            self.l = r
            self.r = rr
            rr.l = self


DECRYPTION_KEY = 1
DECRYPTION_KEY = 811589153

SHIFT_AMOUNT = 1
SHIFT_AMOUNT = 10

with open("input.txt", encoding="utf-8") as f:
    numbers: List[LinkedItem] = [
        LinkedItem(i, int(n) * DECRYPTION_KEY)
        for i, n in enumerate(f.read().splitlines())
    ]
    N = len(numbers)

    # init doubly linked list
    for i in range(N):
        numbers[i].l = numbers[(i - 1) % N]
        numbers[i].r = numbers[(i + 1) % N]

        # ! idea from reddit thread, had >/< separated before
        numbers[i].shift_move = numbers[i].value % (N - 1)

    # go through original list items and shift
    for _ in range(SHIFT_AMOUNT):
        for i in range(N):
            item = next((x for x in numbers if x.order == i), None)
            item.shift_position()

    # bring into proper list from start
    ordered = [next((x for x in numbers if x.value == 0), None)]
    for _ in range(N - 1):
        ordered.append(ordered[-1].r)

    # start counting at position of literal '0'
    result = 0

    for i in range(3):
        result += ordered[((i + 1) * 1000) % N].value

    print(f"Result: {result}")
