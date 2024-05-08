def add(x, y):
    return x + y
add.symbol = "+"

def read_int(raw):
    return int(raw)

def calc_args():
    payload = {
        "operator": add,
    };
    for side in ["left", "right"]:
        raw = input(f"Enter {side} operand: ")
        payload[side] = read_int(raw)
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
