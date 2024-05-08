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

```diff
Subject: [PATCH 01/10] calc: skeleton

First things first, make it runnable.
---
 calc.py | 18 ++++++++++++++++++
 1 file changed, 18 insertions(+)
 create mode 100644 calc.py

diff --git a/calc.py b/calc.py
new file mode 100644
index 0000000..2ef9a48
--- /dev/null
+++ b/calc.py
@@ -0,0 +1,18 @@
+def calc_args():
+    return {
+        "left": 1,
+        "right": 2,
+        "operator": ("+", lambda x, y: x + y)
+    }
+
+def calc():
+    args = calc_args()
+    left = args["left"]
+    right = args["right"]
+    op_name, op_fn = args["operator"]
+
+    result = op_fn(left, right)
+    print(f"{left} {op_name} {right} = {result}")
+
+if __name__ == "__main__":
+    calc()
-- 
```

The elegance of TDA is that your code is always end-to-end runnable, you don't
need to write unit test for the function at the beginning to prove it works.

```diff
Subject: [PATCH 02/10] calc: create an `add` fn

Since we just got started, refactoring won't tak too much efforts.
---
 calc.py | 10 +++++++---
 1 file changed, 7 insertions(+), 3 deletions(-)

diff --git a/calc.py b/calc.py
index 2ef9a48..dc3e29f 100644
--- a/calc.py
+++ b/calc.py
@@ -1,18 +1,22 @@
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
 
 if __name__ == "__main__":
     calc()
-- 
```

We defined an `add` function, and assigned `"+"` to its `symbol` field, so we
can use the `add` directly instead of a `tuple`, to me it is better than the
original one since we won't have cases that share the same `fn` but require
different `symbol`.

```diff
Subject: [PATCH 03/10] calc: read_int(left, right)

Now we can read our input from stdin
---
 calc.py | 13 +++++++++----
 1 file changed, 9 insertions(+), 4 deletions(-)

diff --git a/calc.py b/calc.py
index dc3e29f..cf16bc9 100644
--- a/calc.py
+++ b/calc.py
@@ -2,12 +2,17 @@ def add(x, y):
     return x + y
 add.symbol = "+"
 
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
 
 def calc():
     args = calc_args()
-- 
```

Let's read `left` and `right` from the stdin.

```diff
Subject: [PATCH 04/10] calc: begin abstraction on read_fn

---
 calc.py | 6 ++++--
 1 file changed, 4 insertions(+), 2 deletions(-)

diff --git a/calc.py b/calc.py
index cf16bc9..6ad3008 100644
--- a/calc.py
+++ b/calc.py
@@ -4,14 +4,16 @@ add.symbol = "+"
 
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
 
 def calc():
-- 
```

`read_fn.help` is introduced here to prompt different messages for each
`read_fn` which we will implement for the `operator` later on. And `read_int`
proves it works.
