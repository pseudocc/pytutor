def add(x, y):
    return x + y
add.symbol = "+"

def read_op(raw):
    if raw not in read_op.supported:
        print(f"Invalid operator: {raw}")
        return None
    return read_op.supported[raw]

read_op.supported = {
    "add": add,
}

read_op.help = f"Enter an operator {list(read_op.supported.keys())}"

def read_int(raw):
    value = None
    try:
        value = int(raw)
    except ValueError:
        print(f"Invalid integer: {raw}")
    return value

read_int.help = "Enter an integer"

def calc_args():
    required = [
        ("left", read_int),
        ("right", read_int),
        ("operator", read_op),
    ]
    payload = {};
    for field, read_fn in required:
        raw = input(f"{read_fn.help} for {field}: ")
        value = read_fn(raw)
        while value is None:
            raw = input("Try again: ")
            value = read_fn(raw)
        payload[field] = value
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
