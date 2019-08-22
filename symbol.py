

def get_symbols(filename):
    with open(filename, "r") as f:
        symbols = [v.rstrip() for v in f.readlines()]
    return symbols
