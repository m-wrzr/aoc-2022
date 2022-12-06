# -> find 14 distinct characters == message

with open("input.txt") as f:
    signal, window = f.read(), 14

    for i in range(len(signal) - window + 1):
        if len(set(signal[i : i + window])) == window:
            # start of signal
            print(i + window)
            break
