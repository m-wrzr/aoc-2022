# start-of-packet marker
# four characters that are all different
# -> find 4 letter sequence with unique characters

with open("input.txt") as f:
    signal, window = f.read(), 4

    for i in range(len(signal) - window + 1):
        if len(set(signal[i : i + window])) == window:
            # start of signal
            print(i + window)
            break
