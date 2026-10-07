# Why C is faster than Python for numeric operations

**Date:** 2026-07-12
**Topic:** What's actually happening under the hood — Python objects, boxing, and the interpreter loop
**Turn:** 004e

## User request

Why is it so much faster in C? Why does the Python function call overhead dominate? What is actually going on under the hood?

## Work and response

To understand this, you need to see what Python does with a single number vs what C does.

### What Python does with `x + y`

```python
x = 3.14
y = 2.71
z = x + y
```

Here's what the CPython interpreter actually executes:

1. **Load `x`:** Look up the name `x` in the local namespace. Find the PyObject at that memory address. Check its type tag — it's a `float`. 
2. **Load `y`:** Same thing again. Name lookup, type check.
3. **Call `__add__`:** Python doesn't add floats directly. It calls `x.__add__(y)`, which is a method dispatch. This means: look up `__add__` in `x`'s type's method table, then call it.
4. **Inside `__add__`:** Unbox both floats — extract the raw C `double` from inside the Python `float` object. Now you have two raw `double` values.
5. **Add:** Execute one CPU instruction (`FADD` on x86).
6. **Box the result:** Wrap the raw `double` back into a new Python `float` object. Allocate memory on the heap for it. Set its reference count to 1.
7. **Assign to `z`:** Store the reference in the local namespace.

Step 4 and 5 (the actual math) are nanoseconds. Steps 1–3 and 6–7 (the Python machinery) are hundreds of nanoseconds. The addition itself is less than 1% of the total work.

### What C does with `x + y`

```c
double x = 3.14;
double y = 2.71;
double z = x + y;
```

1. **Add:** One CPU instruction. Done.

No name lookups. No type checks. No method dispatch. No boxing or unboxing. No heap allocation. No reference counting. The values are already in registers or on the stack as raw 64-bit IEEE 754 doubles.

### What "boxing" means

A Python `float` is not a raw number. It's a struct on the heap:

```
PyFloatObject {
    PyObject_HEAD    // reference count, type pointer (16 bytes)
    double ob_fval;  // the actual number (8 bytes)
}
```

To do math on it, Python must:
- **Unbox:** Read `ob_fval` from inside the struct
- **Box:** Create a new struct, set refcount to 1, store the result in `ob_fval`

C just has the `double` — 8 bytes, no wrapper, no heap allocation.

### Why function call overhead matters

Every Python function call involves:

```python
def add(a, b):
    return a + b

# Calling add(x, y) costs:
# 1. Push a new stack frame
# 2. Bind 'a' and 'b' in the new local namespace
# 3. Execute the body
# 4. Unwind the stack frame
# 5. Return value (boxed)
```

If you call `add()` 1,000,000 times in a loop, the stack-frame push/pop happens 1,000,000 times. That's ~50–100 nanoseconds per call in C, but ~200–500 nanoseconds in Python — and the actual work inside the function (the addition) is ~1 nanosecond.

Now compare to `np.add(arr1, arr2)`:

```python
# One Python function call. NumPy internally:
# 1. Checks both arrays are float64, contiguous, same shape
# 2. Calls a C loop: for (i=0; i<n; i++) out[i] = a[i] + b[i];
# 3. Returns the result array
```

One stack frame. One type check. Then a tight C loop with no boxing, no unboxing, no method dispatch. The Python overhead is amortised over 1,000,000 additions.

### The numbers (rough)

| Operation | Python (per element) | NumPy (per element) | Ratio |
|-----------|---------------------|---------------------|-------|
| Addition | ~100 ns | ~1 ns | 100× |
| Function call | ~200 ns | ~0.0002 ns | 1,000,000× |
| Loop overhead | ~50 ns | ~0.00005 ns | 1,000,000× |

The function call and loop overhead don't just add cost — they multiply it. A Python loop with a function call inside it pays the loop overhead, the function call overhead, the boxing, and the unboxing, for every single element. NumPy pays none of that. The C loop runs at memory-bandwidth speed, not interpreter speed.

### Why our rolling VaR loop is still fine

We call `historical_var()` exactly once per trading day — ~1,600 times for our dataset. Inside each call, `np.quantile()` sorts 252 numbers in C. The outer Python loop costs 1,600 × 200ns ≈ 0.3ms. The inner C quantile costs 1,600 × ~5µs ≈ 8ms. The Python overhead is ~4% of the total. It's negligible.

If instead we had a Python loop that did element-by-element addition on 1,600 × 252 = 400,000 numbers, the Python overhead would be ~40ms vs NumPy's ~0.4ms — 100× slower. That's when you vectorise.