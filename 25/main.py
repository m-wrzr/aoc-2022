# sum of the fuel requirements of all of the hot air balloons
# powers of five; 1, 5, 25, 125, ...
# 2, 1, 0, -, =    //      2= -> 8    // 20 -> 10


DIGITS = ["=", "-", "0", "1", "2"]


def to_digit(d: str) -> int:
    """to digit"""
    match d:
        case "-":
            return -1
        case "=":
            return -2
        case _:
            return int(d)


def snafu_to_base_ten(snafu: str):
    """convert from base 5 to base 10"""
    sum_single = 0

    for i, c in enumerate(reversed(snafu)):
        sum_single += to_digit(c) * (5**i)

    return sum_single


def base_ten_to_snafu(number: int):
    """convert from base 10 to base 5"""

    if number == 0:
        return ""

    # offset by 2, otherwise handling of negative numbers is more complicated
    number = number + 2

    # remainder for recursive call + digit for current position
    return base_ten_to_snafu(number // 5) + DIGITS[number % 5]


sum_overall = 0

with open("input.txt", encoding="utf-8") as f:
    while line := f.readline().strip():
        sum_overall += snafu_to_base_ten(line)


print(f"Result: {base_ten_to_snafu(sum_overall)}")
