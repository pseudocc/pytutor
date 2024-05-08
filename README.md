# PYTUTOR

`pytutor` is a step by step project based python learning tutor, which assumes
you already have basic knowledges of Python.

## calc

Prove a top-down approach (TDA), and why it is superior to bottom-up.

In this case we will be building a CLI program that read inputs and do a simple
math, things you may learn from this:

1. `input` to read from `stdin`
1. `print` to write to `stdout`
1. `try` `catch` for error handling
1. Basic operations on `dict`
1. Advanced: Dictionary comprehension
1. Advanced: Define and use a decorator

### Subject: [PATCH 01/10] calc: skeleton

First things first, make it runnable.

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
```

The elegance of TDA is that your code is always end-to-end runnable, you don't
need to write unit test for the function at the beginning to prove it works.

### Subject: [PATCH 02/10] calc: create an `add` fn

Since we just got started, refactoring won't tak too much efforts.

```diff
+def add(x, y):
+    return x + y
+add.symbol = "+"
+
 def calc_args():
     return {
         "left": 1,
         "right": 2,
-        "operator": ("+", lambda x, y: x + y)
+        "operator": add,
     }
 
 def calc():
     args = calc_args()
     left = args["left"]
     right = args["right"]
-    op_name, op_fn = args["operator"]
+    op_fn = args["operator"]
 
     result = op_fn(left, right)
-    print(f"{left} {op_name} {right} = {result}")
+    print(f"{left} {op_fn.symbol} {right} = {result}")
```

We defined an `add` function, and assigned `"+"` to its `symbol` field, so we
can use the `add` directly instead of a `tuple`, to me it is better than the
original one since we won't have cases that share the same `fn` but require
different `symbol`.

### Subject: [PATCH 03/10] calc: read_int(left, right)

Now we can read our input from stdin

```diff
+def read_int(raw):
+    return int(raw)
+
 def calc_args():
-    return {
-        "left": 1,
-        "right": 2,
+    payload = {
         "operator": add,
-    }
+    };
+    for side in ["left", "right"]:
+        raw = input(f"Enter {side} operand: ")
+        payload[side] = read_int(raw)
+    return payload
```

Let's read `left` and `right` from the stdin.

### Subject: [PATCH 04/10] calc: begin abstraction on read_fn

```diff
 def read_int(raw):
     return int(raw)
+read_int.help = "Enter an integer"
 
 def calc_args():
     payload = {
         "operator": add,
     };
     for side in ["left", "right"]:
-        raw = input(f"Enter {side} operand: ")
-        payload[side] = read_int(raw)
+        read_fn = read_int
+        raw = input(f"{read_fn.help} for {side}: ")
+        payload[side] = read_fn(raw)
     return payload
```

`read_fn.help` is introduced here to prompt different messages for each
`read_fn` which we will implement for the `operator` later on. And `read_int`
proves it works.

### Subject: [PATCH 05/10] calc: also read the `operator` from stdin

```diff
+def read_op(raw):
+    return add
+read_op.help = "READ_OP_PLACEHOLDER"
+
 
 def calc_args():
-    payload = {
-        "operator": add,
-    };
-    for side in ["left", "right"]:
-        read_fn = read_int
-        raw = input(f"{read_fn.help} for {side}: ")
-        payload[side] = read_fn(raw)
+    required = [
+        ("left", read_int),
+        ("right", read_int),
+        ("operator", read_op),
+    ]
+    payload = {};
+    for field, read_fn in required:
+        raw = input(f"{read_fn.help} for {field}: ")
+        payload[field] = read_fn(raw)
     return payload
```

We defined a `required` field which contains the field name and its `read_fn`
inside the `calc_args` function, now we can ask user to input them in a loop.

### Subject: [PATCH 06/10] calc: error handling -> try again

```diff
 def read_int(raw):
-    return int(raw)
+    value = None
+    try:
+        value = int(raw)
+    except ValueError:
+        print(f"Invalid integer: {raw}")
+    return value
+
 read_int.help = "Enter an integer"
 
 def calc_args():
@@ -19,7 +25,11 @@ def calc_args():
     payload = {};
     for field, read_fn in required:
         raw = input(f"{read_fn.help} for {field}: ")
-        payload[field] = read_fn(raw)
+        value = read_fn(raw)
+        while value is None:
+            raw = input("Try again: ")
+            value = read_fn(raw)
+        payload[field] = value
     return payload
```

User may input invalid values that break the whole program, so we need to
handle them by using the `try` `catch` block.

Our `read_fn` is designed to `return None` when an error occurs, and `return` a
valid value on success. Then we make a `while` loop to ask user to try again.

### Subject: [PATCH 07/10] calc: make read_op generic

```diff
 def read_op(raw):
-    return add
-read_op.help = "READ_OP_PLACEHOLDER"
+    if raw not in read_op.supported:
+        print(f"Invalid operator: {raw}")
+        return None
+    return read_op.supported[raw]
+
+read_op.supported = {
+    "add": add,
+}
+
+read_op.help = f"Enter an operator {list(read_op.supported.keys())}"
```

Let's make `read_op` to follow the `read_fn` interface (`return None` when an
error occurs). To not repeat ourselves, we store the supported operations in
`read_op.supported` so both `read_op.help` and `read_op` function block can
access its value.

### Subject: [PATCH 08/10] calc: add rest operators

```diff
+def sub(x, y):
+    return x - y
+sub.symbol = "-"
+
+def mul(x, y):
+    return x * y
+mul.symbol = "*"
+
+def div(x, y):
+    return x / y
+div.symbol = "/"
+
 
 read_op.supported = {
     "add": add,
+    "sub": sub,
+    "mul": mul,
+    "div": div,
 }
```

Add the rest of our operators, since we proved the whole flow is steady in the
last commit, it's a no-brainer here.

### Subject: [PATCH 09/10] calc: refactor, simplify our code

```diff
 read_op.supported = {
-    "add": add,
-    "sub": sub,
-    "mul": mul,
-    "div": div,
+    fn.__name__: fn for fn in [add, sub, mul, div]
 }
```

> "premature optimization is the root of all evil."

After `calc.py` meets all our requirements, it's about time to refactor the
code to make our code better.

Functions in Python have a builtin field `__name__` representing its name, so
together with [dictionary comprehensions](https://peps.python.org/pep-0274/),
we can make it one line.

### Subject: [PATCH 10/10] calc: use decorator @op("+")

```diff
+ops = []
+
+def op(symbol):
+    def decorator(fn):
+        fn.symbol = symbol
+        ops.append(fn)
+        return fn
+    return decorator
+
+@op("+")
 def add(x, y):
     return x + y
-add.symbol = "+"
 
+@op("-")
 def sub(x, y):
     return x - y
-sub.symbol = "-"
 
+@op("*")
 def mul(x, y):
     return x * y
-mul.symbol = "*"
 
+@op("/")
 def div(x, y):
     return x / y
-div.symbol = "/"

-read_op.supported = {
-    fn.__name__: fn for fn in [add, sub, mul, div]
-}
+read_op.supported = { fn.__name__: fn for fn in ops }
```

[Python decorators](https://peps.python.org/pep-0318/) could help us in two
places:

1. `op_fn.symbol`
2. `read_op.supported`

Say, one day we may want to extend `calc.py` by adding a `pow("**")` operator.
We need to do something like (without the `@op` decorator):

```diff
+def pow(x, y):
+    return x ** y
+pow.symbol = "**"

 read_op.supported = {
-    fn.__name__: fn for fn in [add, sub, mul, div]
+    fn.__name__: fn for fn in [add, sub, mul, div, pow]
 }
```

If you missed either assigning `pow.symbol` or appending `[..., pow]` the
program would crash!

But with the `@op` decorator, it's a lot simpler.

```diff
+@op("**")
+def pow(x, y):
+    return x ** y
```
