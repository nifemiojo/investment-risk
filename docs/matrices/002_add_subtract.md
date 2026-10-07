# Matrix addition and subtraction

Start with the simplest possible idea:

> **Matrix addition and subtraction work cell-by-cell.**

Suppose:

$$
A=
\begin{bmatrix}
2 & 5\\
3 & 7
\end{bmatrix}
$$

and

$$
B=
\begin{bmatrix}
4 & 1\\
6 & 2
\end{bmatrix}
$$

## 1. Matrix addition

To calculate:

$$
A+B
$$

add numbers in the **same position**:

$$
A+B=
\begin{bmatrix}
2+4 & 5+1\\
3+6 & 7+2
\end{bmatrix}
$$

So:

$$
\boxed{
A+B=
\begin{bmatrix}
6 & 6\\
9 & 9
\end{bmatrix}
}
$$

The mental model is:

```text
[ top-left     top-right  ]
[ bottom-left  bottom-right ]

        +

[ top-left     top-right  ]
[ bottom-left  bottom-right ]
```

Each position interacts only with the corresponding position.

---

# 2. Matrix subtraction

Exactly the same idea, except subtract corresponding entries.

Using the same matrices:

$$
A=
\begin{bmatrix}
2 & 5\\
3 & 7
\end{bmatrix}
,\qquad
B=
\begin{bmatrix}
4 & 1\\
6 & 2
\end{bmatrix}
$$

calculate:

$$
A-B
$$

Position by position:

$$
A-B=
\begin{bmatrix}
2-4 & 5-1\\
3-6 & 7-2
\end{bmatrix}
$$

Therefore:

$$
\boxed{
A-B=
\begin{bmatrix}
-2 & 4\\
-3 & 5
\end{bmatrix}
}
$$

Negative numbers are completely fine.

---

# 3. The crucial rule: dimensions must match

You can only add or subtract matrices if they have **exactly the same dimensions**.

For example:

$$
A=
\begin{bmatrix}
1&2&3\\
4&5&6
\end{bmatrix}
$$

has dimensions:

$$
2\times3
$$

and:

$$
B=
\begin{bmatrix}
7&8&9\\
10&11&12
\end{bmatrix}
$$

also has dimensions:

$$
2\times3
$$

Therefore:

$$
A+B
$$

is valid.

We get:

$$
A+B=
\begin{bmatrix}
1+7 & 2+8 & 3+9\\
4+10 & 5+11 & 6+12
\end{bmatrix}
$$

so:

$$
\boxed{
A+B=
\begin{bmatrix}
8&10&12\\
14&16&18
\end{bmatrix}
}
$$

---

## But this doesn't work

Suppose:

$$
A=
\begin{bmatrix}
1&2&3\\
4&5&6
\end{bmatrix}
$$

which is:

$$
2\times3
$$

while:

$$
B=
\begin{bmatrix}
7&8\\
9&10
\end{bmatrix}
$$

is:

$$
2\times2
$$

Then:

$$
A+B
$$

is **not defined**.

Why?

Because there isn't a corresponding entry for every position.

For example, $A$ has a third column:

$$
\begin{bmatrix}
1&2&\boxed3\\
4&5&\boxed6
\end{bmatrix}
$$

but $B$ doesn't:

$$
\begin{bmatrix}
7&8\\
9&10
\end{bmatrix}
$$

So the rule is:

$$
\boxed{
(m\times n)+(m\times n)
\text{ is valid}
}
$$

but:

$$
\boxed{
(m\times n)+(p\times q)
}
$$

is only valid when:

$$
m=p
$$

and:

$$
n=q
$$

---

# 4. A practical example

Suppose you track the daily profit from three products at two stores.

Monday:

$$
M=
\begin{bmatrix}
100 & 50 & 80\\
70 & 120 & 60
\end{bmatrix}
$$

Tuesday:

$$
T=
\begin{bmatrix}
90 & 60 & 100\\
80 & 110 & 75
\end{bmatrix}
$$

Rows represent stores, columns represent products.

To find total profit across both days:

$$
M+T
$$

So:

$$
M+T=
\begin{bmatrix}
100+90 & 50+60 & 80+100\\
70+80 & 120+110 & 60+75
\end{bmatrix}
$$

giving:

$$
\boxed{
\begin{bmatrix}
190&110&180\\
150&230&135
\end{bmatrix}
}
$$

Matrix addition is useful because the structure is preserved.

The top-left number still represents the same store/product combination; we've simply combined its values.

---

# 5. Subtraction is often useful for measuring change

Suppose January sales were:

$$
J=
\begin{bmatrix}
100&200\\
150&250
\end{bmatrix}
$$

and February sales were:

$$
F=
\begin{bmatrix}
120&180\\
170&300
\end{bmatrix}
$$

To calculate the change from January to February:

$$
F-J
$$

Notice the order:

$$
\boxed{\text{new} - \text{old}}
$$

Calculate:

$$
F-J=
\begin{bmatrix}
120-100 & 180-200\\
170-150 & 300-250
\end{bmatrix}
$$

So:

$$
\boxed{
F-J=
\begin{bmatrix}
20&-20\\
20&50
\end{bmatrix}
}
$$

The interpretation is useful:

* $20$: increased by 20
* $-20$: decreased by 20
* $20$: increased by 20
* $50$: increased by 50

So subtraction can produce a **difference matrix**.

This is common in finance and data analysis:

$$
\boxed{\Delta X=X_{\text{new}}-X_{\text{old}}}
$$

where $\Delta$, pronounced **delta**, means "change in."

---

# 6. Matrix subtraction is really addition of negatives

There's another way of understanding subtraction.

With ordinary numbers:

$$
5-3=5+(-3)
$$

Matrices work the same way.

Suppose:

$$
A=
\begin{bmatrix}
5&8\\
2&4
\end{bmatrix}
$$

and:

$$
B=
\begin{bmatrix}
1&3\\
6&2
\end{bmatrix}
$$

Then:

$$
-B=
\begin{bmatrix}
-1&-3\\
-6&-2
\end{bmatrix}
$$

Therefore:

$$
A-B=A+(-B)
$$

So:

$$
\begin{bmatrix}
5&8\\
2&4
\end{bmatrix}
+
\begin{bmatrix}
-1&-3\\
-6&-2
\end{bmatrix}
$$

gives:

$$
\begin{bmatrix}
4&5\\
-4&2
\end{bmatrix}
$$

This matters later because mathematically, subtraction doesn't really need to be a completely separate operation:

$$
\boxed{A-B=A+(-B)}
$$

---

# 7. Order matters for subtraction

Addition behaves nicely:

$$
A+B=B+A
$$

For example:

$$
2+5=5+2
$$

and matrices behave the same way.

But subtraction does **not**:

$$
A-B\neq B-A
$$

in general.

For example:

$$
A=
\begin{bmatrix}
5&7
\end{bmatrix}
$$

and:

$$
B=
\begin{bmatrix}
2&3
\end{bmatrix}
$$

Then:

$$
A-B=
\begin{bmatrix}
3&4
\end{bmatrix}
$$

whereas:

$$
B-A=
\begin{bmatrix}
-3&-4
\end{bmatrix}
$$

In fact:

$$
\boxed{B-A=-(A-B)}
$$

---

# 8. Algebra with matrices looks familiar

Once the dimensions are compatible, many ordinary algebra rules carry over.

For example:

$$
A+B-C
$$

means exactly what you'd expect:

$$
(A+B)-C
$$

Suppose:

$$
A=
\begin{bmatrix}
1&2\\
3&4
\end{bmatrix}
$$

$$
B=
\begin{bmatrix}
5&6\\
7&8
\end{bmatrix}
$$

$$
C=
\begin{bmatrix}
2&1\\
3&2
\end{bmatrix}
$$

First:

$$
A+B=
\begin{bmatrix}
6&8\\
10&12
\end{bmatrix}
$$

then subtract $C$:

$$
\begin{bmatrix}
6&8\\
10&12
\end{bmatrix}
-
\begin{bmatrix}
2&1\\
3&2
\end{bmatrix}
$$

giving:

$$
\boxed{
\begin{bmatrix}
4&7\\
7&10
\end{bmatrix}
}
$$

---

# 9. Element notation

You'll eventually see matrix addition expressed more compactly.

If:

$$
C=A+B
$$

then each entry of $C$ is:

$$
\boxed{c_{ij}=a_{ij}+b_{ij}}
$$

Don't let the notation make it look more complicated than it is.

It simply says:

> The number in row $i$, column $j$ of $C$ equals the corresponding number from $A$ plus the corresponding number from $B$.

For subtraction:

$$
\boxed{c_{ij}=a_{ij}-b_{ij}}
$$

Same cell-by-cell idea.

---

# 10. Mental model

For addition and subtraction, matrices behave much like arrays.

If you had:

```csharp
double[,] a =
{
    { 1, 2 },
    { 3, 4 }
};

double[,] b =
{
    { 5, 6 },
    { 7, 8 }
};
```

Matrix addition conceptually does:

```csharp
result[row, col] = a[row, col] + b[row, col];
```

for every valid `row, col`.

That's essentially the whole algorithm.

This is known as an **element-wise operation**:

$$
\boxed{\text{corresponding element} \rightarrow \text{corresponding element}}
$$

---

# 11. Addition vs multiplication

Keep these mentally separate because beginners often mix them up.

### Matrix addition

Same dimensions required:

$$
(2\times3)+(2\times3)
$$

Then work **cell by cell**.

### Matrix multiplication

Dimensions don't need to be identical.

Instead, the inner dimensions must match:

$$
(2\times3)(3\times4)
$$

Then work **row by column**.

So:

$$
\boxed{
\text{Addition: same shape + element-wise}
}
$$

versus:

$$
\boxed{
\text{Multiplication: inner dimensions match + row-by-column}
}
$$

---

# 12. Try these

### Question 1

$$
A=
\begin{bmatrix}
3&7\\
4&2
\end{bmatrix}
$$

$$
B=
\begin{bmatrix}
5&1\\
2&6
\end{bmatrix}
$$

Calculate:

$$
A+B
$$

---

### Question 2

Using the same matrices, calculate:

$$
A-B
$$

---

### Question 3

Can these matrices be added?

$$
A:3\times4
$$

$$
B:3\times4
$$

---

### Question 4

Can these be subtracted?

$$
A:2\times5
$$

$$
B:5\times2
$$

---

### Question 5 — interpretation

Yesterday's positions:

$$
Y=
\begin{bmatrix}
100&50\\
30&80
\end{bmatrix}
$$

Today's positions:

$$
T=
\begin{bmatrix}
120&40\\
35&100
\end{bmatrix}
$$

Calculate:

$$
T-Y
$$

and try to interpret what the positive and negative numbers mean.

The key rule to retain is simply:

$$
\boxed{
A\pm B
\text{ requires A and B to have the same dimensions}
}
$$

and then:

$$
\boxed{\text{operate on corresponding entries}}
$$
