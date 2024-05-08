### Subject: [PATCH 01/10] calc: skeleton

```python
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
### Subject: [PATCH 02/10] calc: create an `add` fn

```diff
### Subject: [PATCH 03/10] calc: read_int(left, right)

```diff
### Subject: [PATCH 04/10] calc: begin abstraction on read_fn
```diff
### Subject: [PATCH 05/10] calc: also read the `operator` from stdin
```diff
### Subject: [PATCH 06/10] calc: error handling -> try again

### Subject: [PATCH 07/10] calc: make read_op generic

### Subject: [PATCH 08/10] calc: add rest operators
```diff
### Subject: [PATCH 09/10] calc: refactor, simplify our code

### Subject: [PATCH 10/10] calc: use decorator @op("+")
```diff
