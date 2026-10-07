# Matrix multiplication — from the ground up

Matrix multiplication feels strange at first because it is **not element-by-element multiplication**.

The core rule is:

> **Take a row from the left matrix and a column from the right matrix. Multiply corresponding numbers, then add.**

That one rule generates the entire result.

---

## 1. Start with the smallest useful example

Suppose:

$$
A=
\begin{bmatrix}
2 & 3
\end{bmatrix}
$$

and

$$
B=
\begin{bmatrix}
4\\
5
\end{bmatrix}
$$

We want:

$$
AB
$$

Take the row from $A$:

$$
[2,\ 3]
$$

and the column from $B$:

$$
\begin{bmatrix}
4\\
5
\end{bmatrix}
$$

Pair the entries:

$$
2 \leftrightarrow 4
$$

$$
3 \leftrightarrow 5
$$

Multiply each pair:

$$
2(4)=8
$$

$$
3(5)=15
$$

then add:

$$
8+15=23
$$

Therefore:

$$
\boxed{AB=23}
$$

The underlying operation is:

$$
\boxed{2(4)+3(5)}
$$

This is the fundamental building block of matrix multiplication.

---

# 2. A practical interpretation

Imagine:

* you bought 2 units of Asset A
* you bought 3 units of Asset B

So your holdings are:

$$
H=
\begin{bmatrix}
2&3
\end{bmatrix}
$$

The asset prices are:

$$
P=
\begin{bmatrix}
£4\\
£5
\end{bmatrix}
$$

Then:

$$
HP
$$

calculates:

$$
2(£4)+3(£5)
$$

giving:

$$
£8+£15=£23
$$

So matrix multiplication has combined:

$$
\text{quantities}
$$

with:

$$
\text{prices}
$$

to calculate:

$$
\text{portfolio value}
$$

That's much closer to *why* matrix multiplication exists than simply memorising a rule.

---

# 3. The row-column rule

For every entry in the answer:

$$
\boxed{\text{row from left matrix} \times \text{column from right matrix}}
$$

More precisely:

1. Multiply matching entries.
2. Add the products.

You can mentally abbreviate this as:

$$
\boxed{\text{Row} \cdot \text{Column}}
$$

The $\cdot$ here is often called a **dot product**.

---

# 4. Let's multiply two $2\times2$ matrices

Consider:

$$
A=
\begin{bmatrix}
1&2\\
3&4
\end{bmatrix}
$$

and

$$
B=
\begin{bmatrix}
5&6\\
7&8
\end{bmatrix}
$$

We want:

$$
AB
$$

The answer will contain four entries:

$$
AB=
\begin{bmatrix}
?&?\\
?&?
\end{bmatrix}
$$

We'll calculate them one at a time.

---

## 5. Top-left entry

Take **row 1 of $A$**:

$$
[1,\ 2]
$$

and **column 1 of $B$**:

$$
\begin{bmatrix}
5\\
7
\end{bmatrix}
$$

Multiply and add:

$$
1(5)+2(7)
$$

$$
=5+14
$$

$$
=19
$$

So:

$$
AB=
\begin{bmatrix}
19&?\\
?&?
\end{bmatrix}
$$

---

# 6. Top-right entry

Still use row 1 of $A$:

$$
[1,\ 2]
$$

but now use column 2 of $B$:

$$
\begin{bmatrix}
6\\
8
\end{bmatrix}
$$

So:

$$
1(6)+2(8)
$$

$$
=6+16
$$

$$
=22
$$

We now have:

$$
AB=
\begin{bmatrix}
19&22\\
?&?
\end{bmatrix}
$$

---

# 7. Bottom-left entry

Now use row 2 of $A$:

$$
[3,\ 4]
$$

with column 1 of $B$:

$$
\begin{bmatrix}
5\\
7
\end{bmatrix}
$$

Therefore:

$$
3(5)+4(7)
$$

$$
=15+28
$$

$$
=43
$$

So:

$$
AB=
\begin{bmatrix}
19&22\\
43&?
\end{bmatrix}
$$

---

# 8. Bottom-right entry

Use:

$$
[3,\ 4]
$$

and:

$$
\begin{bmatrix}
6\\
8
\end{bmatrix}
$$

Then:

$$
3(6)+4(8)
$$

$$
=18+32
$$

$$
=50
$$

Therefore:

$$
\boxed{
AB=
\begin{bmatrix}
19&22\\
43&50
\end{bmatrix}
}
$$

---

# 9. How to know whether two matrices can be multiplied

This is the second major rule.

Suppose:

$$
A
$$

has dimensions:

$$
m\times n
$$

and:

$$
B
$$

has dimensions:

$$
n\times p
$$

Then:

$$
AB
$$

is valid.

Notice the two middle numbers:

$$
(m\times\boxed n)(\boxed n\times p)
$$

They must match.

The result then has the dimensions represented by the **outside numbers**:

$$
\boxed{m\times p}
$$

So remember:

$$
\boxed{(m\times n)(n\times p)\rightarrow m\times p}
$$

---

# 10. Example with dimensions only

Suppose:

$$
A:2\times3
$$

and:

$$
B:3\times4
$$

Then:

$$
AB
$$

looks like:

$$
(2\times\boxed3)(\boxed3\times4)
$$

The inner dimensions match:

$$
3=3
$$

so multiplication is allowed.

The answer has dimensions:

$$
\boxed{2\times4}
$$

So:

$$
\boxed{(2\times3)(3\times4)=2\times4}
$$

in terms of dimensions.

---

# 11. Why must the inner dimensions match?

This isn't an arbitrary rule.

Suppose a row from $A$ contains three numbers:

$$
[a,\ b,\ c]
$$

To perform a row-column calculation, a column from $B$ must also contain three numbers:

$$
\begin{bmatrix}
x\\
y\\
z
\end{bmatrix}
$$

Then we can pair them:

$$
ax+by+cz
$$

But imagine the column only contained two:

$$
\begin{bmatrix}
x\\
y
\end{bmatrix}
$$

What gets multiplied by $c$?

Nothing.

So the operation cannot be performed.

That's the reason behind:

$$
\boxed{\text{inner dimensions must match}}
$$

---

# 12. Why do the outside dimensions determine the answer?

Consider:

$$
A:2\times3
$$

and:

$$
B:3\times4
$$

Matrix $A$ has:

$$
2\text{ rows}
$$

Matrix $B$ has:

$$
4\text{ columns}
$$

Each result entry comes from:

$$
\text{one A row} \times \text{one B column}
$$

There are:

* 2 possible rows from $A$
* 4 possible columns from $B$

Therefore we produce:

$$
2\times4
$$

different row-column combinations.

Hence:

$$
AB:2\times4
$$

This is a better explanation than merely memorising "outside numbers."

---

# 13. A $2\times3$ by $3\times2$ example

Let's calculate one.

$$
A=
\begin{bmatrix}
1&2&3\\
4&5&6
\end{bmatrix}
$$

So:

$$
A:2\times3
$$

and:

$$
B=
\begin{bmatrix}
7&8\\
9&10\\
11&12
\end{bmatrix}
$$

So:

$$
B:3\times2
$$

Check dimensions:

$$
(2\times\boxed3)(\boxed3\times2)
$$

Valid.

The answer will be:

$$
2\times2
$$

So start with:

$$
AB=
\begin{bmatrix}
?&?\\
?&?
\end{bmatrix}
$$

---

### Top-left

Row 1 of $A$:

$$
[1,2,3]
$$

Column 1 of $B$:

$$
\begin{bmatrix}
7\\
9\\
11
\end{bmatrix}
$$

Therefore:

$$
1(7)+2(9)+3(11)
$$

$$
=7+18+33
$$

$$
=58
$$

---

### Top-right

Row 1:

$$
[1,2,3]
$$

Column 2:

$$
\begin{bmatrix}
8\\
10\\
12
\end{bmatrix}
$$

So:

$$
1(8)+2(10)+3(12)
$$

$$
=8+20+36
$$

$$
=64
$$

---

### Bottom-left

$$
4(7)+5(9)+6(11)
$$

$$
=28+45+66
$$

$$
=139
$$

---

### Bottom-right

$$
4(8)+5(10)+6(12)
$$

$$
=32+50+72
$$

$$
=154
$$

Therefore:

$$
\boxed{
AB=
\begin{bmatrix}
58&64\\
139&154
\end{bmatrix}
}
$$

---

# 14. Matrix multiplication is **not** element-wise multiplication

A very common mistake is seeing:

$$
\begin{bmatrix}
1&2\\
3&4
\end{bmatrix}
\begin{bmatrix}
5&6\\
7&8
\end{bmatrix}
$$

and doing:

$$
\begin{bmatrix}
1(5)&2(6)\\
3(7)&4(8)
\end{bmatrix}
$$

That would give:

$$
\begin{bmatrix}
5&12\\
21&32
\end{bmatrix}
$$

but that is **not standard matrix multiplication**.

Standard multiplication uses:

$$
\boxed{\text{rows} \times \text{columns}}
$$

which gave us:

$$
\begin{bmatrix}
19&22\\
43&50
\end{bmatrix}
$$

instead.

Element-wise multiplication does exist and is sometimes called the **Hadamard product**, but it is a different operation.

---

# 15. Another practical example: multiple portfolios

Suppose there are three assets with prices:

$$
P=
\begin{bmatrix}
100\\
50\\
20
\end{bmatrix}
$$

And you have two portfolios.

Portfolio 1 holds:

* 2 of Asset 1
* 4 of Asset 2
* 3 of Asset 3

Portfolio 2 holds:

* 5 of Asset 1
* 1 of Asset 2
* 10 of Asset 3

Represent that as:

$$
H=
\begin{bmatrix}
2&4&3\\
5&1&10
\end{bmatrix}
$$

Dimensions:

$$
H:2\times3
$$

$$
P:3\times1
$$

So:

$$
HP:
(2\times3)(3\times1)
\rightarrow
2\times1
$$

Calculate portfolio 1:

$$
2(100)+4(50)+3(20)
$$

$$
=200+200+60
$$

$$
=460
$$

Portfolio 2:

$$
5(100)+1(50)+10(20)
$$

$$
=500+50+200
$$

$$
=750
$$

Therefore:

$$
\boxed{
HP=
\begin{bmatrix}
460\\
750
\end{bmatrix}
}
$$

One matrix multiplication gave us the values of **both portfolios simultaneously**.

This is a useful mental model:

> Matrix multiplication calculates many weighted sums at once.

---

# 16. Order matters

Here's something quite different from ordinary arithmetic.

For numbers:

$$
3\times5=5\times3
$$

But matrices generally satisfy:

$$
\boxed{AB\neq BA}
$$

Sometimes one order is valid while the reverse order isn't even possible.

Suppose:

$$
A:2\times3
$$

and:

$$
B:3\times4
$$

Then:

$$
AB:
(2\times3)(3\times4)
$$

works.

But:

$$
BA:
(3\times4)(2\times3)
$$

would require:

$$
4=2
$$

which isn't true.

So $BA$ isn't even defined.

Therefore:

$$
\boxed{\text{matrix multiplication is order-sensitive}}
$$

This becomes extremely important later.

---

# 17. A useful geometric interpretation

Matrix multiplication can also mean:

> **Apply one transformation, then another.**

If:

$$
B
$$

transforms some vector, and then:

$$
A
$$

transforms the result, you get:

$$
A(Bx)
$$

which can be written:

$$
(AB)x
$$

So:

$$
AB
$$

can represent the **combined effect of two transformations**.

This is why matrix multiplication appears everywhere in:

* computer graphics
* 3D engines
* robotics
* machine learning
* physics
* economics
* quantitative finance

Multiplication lets us **compose transformations**.

We'll revisit this once vectors feel comfortable.

---

# 18. The two rules worth memorising

For now, reduce matrix multiplication to these two ideas.

### Rule 1: dimensions

$$
\boxed{
(m\times n)(n\times p)
\rightarrow
m\times p
}
$$

**Inside must match; outside gives the answer shape.**

### Rule 2: values

Each answer entry comes from:

$$
\boxed{\text{row from left} \cdot \text{column from right}}
$$

Meaning:

$$
[a,b,c]
\begin{bmatrix}
x\\
y\\
z
\end{bmatrix}
=
ax+by+cz
$$

If those two ideas become automatic, matrix multiplication becomes much easier.

---

# Try these

Don't rush to calculate; check the **dimensions first**.

### 1

Can we multiply:

$$
(3\times4)(4\times2)?
$$

If yes, what is the output dimension?

### 2

Can we multiply:

$$
(3\times4)(3\times2)?
$$

### 3

What is:

$$
\begin{bmatrix}
2&4
\end{bmatrix}
\begin{bmatrix}
3\\
5
\end{bmatrix}
$$

### 4

Calculate:

$$
\begin{bmatrix}
1&2\\
3&1
\end{bmatrix}
\begin{bmatrix}
2&4\\
5&3
\end{bmatrix}
$$

A good next step after this is the **dot product**, because that's the small operation hiding inside every matrix multiplication.
