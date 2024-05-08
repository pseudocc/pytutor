def add(x, y):
    return x + y
add.symbol = "+"

def read_op(raw):
    return add
read_op.help = "READ_OP_PLACEHOLDER"

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
