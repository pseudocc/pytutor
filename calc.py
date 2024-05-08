def add(x, y):
    return x + y
add.symbol = "+"

def read_int(raw):
    return int(raw)
read_int.help = "Enter an integer"

def calc_args():
    payload = {
        "operator": add,
    };
    for side in ["left", "right"]:
        read_fn = read_int
        raw = input(f"{read_fn.help} for {side}: ")
        payload[side] = read_fn(raw)
    return payload

def calc():
    args = calc_args()
    left = args["left"]
    right = args["right"]
    op_fn = args["operator"]

    result = op_fn(left, right)
    print(f"{left} {op_fn.symbol} {right} = {result}")

if __name__ == "__main__":
    calc()
