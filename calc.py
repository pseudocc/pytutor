def calc_args():
    return {
        "left": 1,
        "right": 2,
        "operator": ("+", lambda x, y: x + y)
    }

def calc():
    args = calc_args()
    left = args["left"]
    right = args["right"]
    op_name, op_fn = args["operator"]

    result = op_fn(left, right)
    print(f"{left} {op_name} {right} = {result}")

if __name__ == "__main__":
    calc()
