def add(x, y):
    return x + y
add.symbol = "+"

def calc_args():
    return {
        "left": 1,
        "right": 2,
        "operator": add,
    }

def calc():
    args = calc_args()
    left = args["left"]
    right = args["right"]
    op_fn = args["operator"]

    result = op_fn(left, right)
    print(f"{left} {op_fn.symbol} {right} = {result}")

if __name__ == "__main__":
    calc()
