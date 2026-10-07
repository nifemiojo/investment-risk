# Matrices — from zero

A **matrix** is just a rectangular grid of numbers.

For example:

$$
A=
\begin{bmatrix}
3 & 7\\
2 & 5
\end{bmatrix}
$$

At first, treat it literally as a table:

|       | Column 1 | Column 2 |
| ----- | -------: | -------: |
| Row 1 |        3 |        7 |
| Row 2 |        2 |        5 |

That's already most of the initial idea.

Matrices become powerful because we can treat the **entire table as one mathematical object** and perform operations on it.

---

# 1. A practical example first

Suppose you run two shops selling **coffee** and **tea**.

Yesterday:

* Shop A sold 30 coffees and 20 teas.
* Shop B sold 25 coffees and 40 teas.

We can store all four numbers in one matrix:

$$
S=
\begin{bmatrix}
30 & 20\\
25 & 40
\end{bmatrix}
$$

We decide:

* rows represent shops
* columns represent products

So:

$$
\begin{array}{c|cc}
& \text{Coffee} & \text{Tea}\\
\hline
\text{Shop A} & 30 & 20\\
\text{Shop B} & 25 & 40
\end{array}
$$

The matrix itself does **not** know what the numbers mean. We assign the meaning.

That's an important mental model:

> A matrix is structured numeric data plus an interpretation.

---

# 2. Rows and columns

Consider:

$$
A=
\begin{bmatrix}
4 & 7 & 1\\
2 & 9 & 6
\end{bmatrix}
$$

It has:

* 2 rows
* 3 columns

So we say its **dimensions** or **shape** are:

$$
2\times3
$$

Read this as:

> "2 by 3"

Always:

$$
\boxed{\text{rows} \times \text{columns}}
$$

Not columns × rows.

So:

$$
\begin{bmatrix}
1&2\\
3&4\\
5&6
\end{bmatrix}
$$

is:

$$
3\times2
$$

because there are 3 rows and 2 columns.

---

# 3. Individual entries

We often need to refer to one particular number.

Suppose:

$$
A=
\begin{bmatrix}
4 & 7 & 1\\
2 & 9 & 6
\end{bmatrix}
$$

We write:

$$
a_{ij}
$$

where:

* $i$ = row
* $j$ = column

So:

$$
a_{12}=7
$$

because 7 is at:

* row 1
* column 2

Similarly:

$$
a_{23}=6
$$

because 6 is at row 2, column 3.

A useful phrase to remember:

> **row first, column second**

Like coordinates.

---

# 4. Different kinds of matrices

Don't worry about memorising these yet. Just recognise the patterns.

### Row matrix / row vector

One row:

$$
\begin{bmatrix}
3&7&9
\end{bmatrix}
$$

Shape:

$$
1\times3
$$

---

### Column matrix / column vector

One column:

$$
\begin{bmatrix}
3\\
7\\
9
\end{bmatrix}
$$

Shape:

$$
3\times1
$$

These are usually called **vectors**, and we'll eventually see that vectors and matrices are closely related.

---

### Square matrix

Same number of rows and columns:

$$
\begin{bmatrix}
1&2\\
3&4
\end{bmatrix}
$$

is $2\times2$.

And:

$$
\begin{bmatrix}
1&2&3\\
4&5&6\\
7&8&9
\end{bmatrix}
$$

is $3\times3$.

Square matrices turn out to be especially important.

---

# 5. Adding matrices

Matrix addition is very intuitive.

Suppose:

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

Then:

$$
A+B
$$

means add corresponding positions:

$$
A+B=
\begin{bmatrix}
1+5&2+6\\
3+7&4+8
\end{bmatrix}
$$

Therefore:

$$
\boxed{
A+B=
\begin{bmatrix}
6&8\\
10&12
\end{bmatrix}
}
$$

You can imagine stacking the matrices on top of one another and adding corresponding cells.

---

# 6. There is an important restriction

You can only add matrices with the **same shape**.

For example:

$$
2\times3 + 2\times3
$$

is valid.

But:

$$
2\times3 + 3\times2
$$

is not.

Why?

Because there isn't a one-to-one corresponding cell structure.

For example:

$$
\begin{bmatrix}
1&2&3\\
4&5&6
\end{bmatrix}
$$

cannot sensibly be added cell-by-cell to:

$$
\begin{bmatrix}
1&2\\
3&4\\
5&6
\end{bmatrix}
$$

Their shapes differ.

---

# 7. Multiplying a matrix by a number

This is called **scalar multiplication**.

"Scalar" is just a mathematical word for an ordinary single number.

Suppose:

$$
A=
\begin{bmatrix}
1&2\\
3&4
\end{bmatrix}
$$

Then:

$$
3A
$$

means multiply **every entry** by 3:

$$
3A=
\begin{bmatrix}
3(1)&3(2)\\
3(3)&3(4)
\end{bmatrix}
$$

so:

$$
\boxed{
3A=
\begin{bmatrix}
3&6\\
9&12
\end{bmatrix}
}
$$

This is straightforward.

For example, if your matrix represented salaries and everyone got a 10% increase, multiplying by:

$$
1.1
$$

would increase every salary by 10%.

---

# 8. Matrix multiplication is the unusual part

This is where matrices become much more interesting.

Matrix multiplication is **not**:

$$
\begin{bmatrix}
a&b\\
c&d
\end{bmatrix}
\begin{bmatrix}
e&f\\
g&h
\end{bmatrix}
=
\begin{bmatrix}
ae&bf\\
cg&dh
\end{bmatrix}
$$

That's a common beginner assumption.

Instead, matrix multiplication combines **rows with columns**.

Let's build it from a real example.

---

# 9. Revenue example

Suppose a shop sells:

* 30 coffees
* 20 teas

Represent quantities as:

$$
Q=
\begin{bmatrix}
30&20
\end{bmatrix}
$$

Now suppose prices are:

* coffee = £4
* tea = £3

Represent prices as:

$$
P=
\begin{bmatrix}
4\\
3
\end{bmatrix}
$$

Notice the shapes:

$$
Q: 1\times2
$$

and

$$
P: 2\times1
$$

Now multiply:

$$
QP
$$

We pair the row:

$$
\begin{bmatrix}30&20\end{bmatrix}
$$

with the column:

$$
\begin{bmatrix}4\\3\end{bmatrix}
$$

and calculate:

$$
30(4)+20(3)
$$

Therefore:

$$
QP=120+60=180
$$

Revenue is:

$$
\boxed{£180}
$$

This operation may already look familiar.

It's essentially:

> quantity × price, summed across products.

---

# 10. The fundamental matrix multiplication rule

Suppose:

$$
A=
\begin{bmatrix}
a&b
\end{bmatrix}
$$

and:

$$
B=
\begin{bmatrix}
c\\
d
\end{bmatrix}
$$

Then:

$$
AB=ac+bd
$$

You can think:

$$
\boxed{\text{row} \cdot \text{column}}
$$

This single idea explains all matrix multiplication.

---

# 11. Let's multiply two larger matrices

Take:

$$
A=
\begin{bmatrix}
1&2\\
3&4
\end{bmatrix}
$$

and:

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

Start with the top-left answer.

Take **row 1 of $A$**:

$$
\begin{bmatrix}
1&2
\end{bmatrix}
$$

and **column 1 of $B$**:

$$
\begin{bmatrix}
5\\
7
\end{bmatrix}
$$

Multiply corresponding values and add:

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

Now top-right.

Row 1 of $A$:

$$
\begin{bmatrix}
1&2
\end{bmatrix}
$$

Column 2 of $B$:

$$
\begin{bmatrix}
6\\
8
\end{bmatrix}
$$

So:

$$
1(6)+2(8)=22
$$

giving:

$$
\begin{bmatrix}
19&22\\
?&?
\end{bmatrix}
$$

---

Bottom-left:

$$
3(5)+4(7)
$$

$$
=15+28=43
$$

---

Bottom-right:

$$
3(6)+4(8)
$$

$$
=18+32=50
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

# 12. A visual mental model

For every output cell:

> Pick one row from the left matrix and one column from the right matrix.

Then:

1. multiply matching positions
2. add the results

So:

$$
\begin{bmatrix}
\boxed{1}&\boxed{2}\\
3&4
\end{bmatrix}
\begin{bmatrix}
\boxed{5}&6\\
\boxed{7}&8
\end{bmatrix}
$$

produces:

$$
1(5)+2(7)=19
$$

for the first answer cell.

A useful phrase is:

$$
\boxed{\text{row by column}}
$$

---

# 13. Why do matrix dimensions matter when multiplying?

Suppose:

$$
A
$$

is:

$$
2\times3
$$

and:

$$
B
$$

is:

$$
3\times4
$$

Then:

$$
AB
$$

is valid.

Why?

Because each row in $A$ contains **3 numbers**, and each column in $B$ contains **3 numbers**.

They can therefore pair up.

Write the dimensions next to each other:

$$
(2\times\boxed{3})(\boxed{3}\times4)
$$

The **inside numbers must match**.

Then the answer takes the **outside numbers**:

$$
\boxed{2\times4}
$$

So:

$$
\boxed{
(2\times3)(3\times4)
\rightarrow
2\times4
}
$$

This is one of the most useful rules in matrices.

---

# 14. Another example

Can we multiply:

$$
(4\times2)(2\times7)?
$$

Yes:

$$
(4\times\boxed2)(\boxed2\times7)
$$

The middle dimensions match.

The result is:

$$
\boxed{4\times7}
$$

---

What about:

$$
(4\times2)(3\times5)?
$$

No:

$$
(4\times\boxed2)(\boxed3\times5)
$$

because:

$$
2\neq3
$$

Therefore multiplication is undefined.

---

# 15. A surprising consequence: order matters

With normal numbers:

$$
3\times5=5\times3
$$

So multiplication is **commutative**.

Matrices generally don't behave like that.

Usually:

$$
AB\neq BA
$$

And sometimes:

$$
AB
$$

exists while:

$$
BA
$$

doesn't even exist.

For example:

$$
A:2\times3
$$

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

doesn't work because:

$$
4\neq2
$$

So matrix order is significant.

This becomes extremely important in programming, graphics, machine learning and physics.

---

# 16. The zero matrix

Similar to the number $0$, matrices have a zero-like object.

For example:

$$
0=
\begin{bmatrix}
0&0\\
0&0
\end{bmatrix}
$$

Then:

$$
A+0=A
$$

For example:

$$
\begin{bmatrix}
1&2\\
3&4
\end{bmatrix}
+
\begin{bmatrix}
0&0\\
0&0
\end{bmatrix}
=
\begin{bmatrix}
1&2\\
3&4
\end{bmatrix}
$$

---

# 17. The identity matrix

There's also a matrix equivalent of multiplying by $1$.

For a $2\times2$ matrix it's:

$$
I=
\begin{bmatrix}
1&0\\
0&1
\end{bmatrix}
$$

This is called the **identity matrix**.

For appropriate matrices:

$$
AI=A
$$

and:

$$
IA=A
$$

For example:

$$
\begin{bmatrix}
2&3\\
4&5
\end{bmatrix}
\begin{bmatrix}
1&0\\
0&1
\end{bmatrix}
=
\begin{bmatrix}
2&3\\
4&5
\end{bmatrix}
$$

So conceptually:

$$
\boxed{I\text{ plays a role similar to }1}
$$

while the zero matrix plays a role similar to $0$.

---

# 18. The transpose

Another basic operation is called the **transpose**.

It means:

> turn rows into columns.

Suppose:

$$
A=
\begin{bmatrix}
1&2&3\\
4&5&6
\end{bmatrix}
$$

Then its transpose is written:

$$
A^T
$$

and is:

$$
A^T=
\begin{bmatrix}
1&4\\
2&5\\
3&6
\end{bmatrix}
$$

Notice that $A$ was:

$$
2\times3
$$

while $A^T$ is:

$$
3\times2
$$

So transpose flips the dimensions.

---

# 19. A powerful mental model: matrices as transformations

So far we've viewed matrices as tables of data.

There's another interpretation that becomes much more important later:

> **A matrix can represent a function that transforms vectors.**

Suppose:

$$
v=
\begin{bmatrix}
x\\
y
\end{bmatrix}
$$

and:

$$
A=
\begin{bmatrix}
2&0\\
0&3
\end{bmatrix}
$$

Then:

$$
Av=
\begin{bmatrix}
2&0\\
0&3
\end{bmatrix}
\begin{bmatrix}
x\\
y
\end{bmatrix}
$$

gives:

$$
Av=
\begin{bmatrix}
2x\\
3y
\end{bmatrix}
$$

So this matrix performs the transformation:

$$
(x,y)\rightarrow(2x,3y)
$$

It stretches:

* $x$ by $2$
* $y$ by $3$

For example:

$$
\begin{bmatrix}
2&0\\
0&3
\end{bmatrix}
\begin{bmatrix}
4\\
5
\end{bmatrix}
=
\begin{bmatrix}
8\\
15
\end{bmatrix}
$$

So:

$$
(4,5)\rightarrow(8,15)
$$

This perspective is enormously important.

Matrices can represent things like:

* rotation
* scaling
* translation with homogeneous coordinates
* financial relationships
* systems of equations
* probability transitions
* neural-network layers
* computer graphics transformations
* portfolio exposures

---

# 20. Why matrices are so useful in software

Suppose you have prices for 3 assets:

$$
p=
\begin{bmatrix}
100\\
50\\
200
\end{bmatrix}
$$

and three portfolios:

$$
H=
\begin{bmatrix}
2&3&1\\
1&0&4\\
5&2&0
\end{bmatrix}
$$

Each row represents holdings in one portfolio.

Then:

$$
Hp
$$

calculates **all three portfolio values at once**.

First portfolio:

$$
2(100)+3(50)+1(200)
$$

$$
=550
$$

Second:

$$
1(100)+0(50)+4(200)
$$

$$
=900
$$

Third:

$$
5(100)+2(50)+0(200)
$$

$$
=600
$$

Therefore:

$$
Hp=
\begin{bmatrix}
550\\
900\\
600
\end{bmatrix}
$$

That's a useful way to see what matrix multiplication really buys you.

Instead of thinking:

> "Matrix multiplication is a weird rule."

Think:

> "Matrix multiplication lets me apply many weighted combinations simultaneously."

That's a much better intuition.

---

# 21. Matrices and systems of equations

Here's another major application.

Suppose:

$$
2x+3y=8
$$

and:

$$
4x+y=10
$$

We can package this into matrices.

The coefficients:

$$
A=
\begin{bmatrix}
2&3\\
4&1
\end{bmatrix}
$$

The unknowns:

$$
x=
\begin{bmatrix}
x\\
y
\end{bmatrix}
$$

The answers:

$$
b=
\begin{bmatrix}
8\\
10
\end{bmatrix}
$$

Then the entire system becomes:

$$
\boxed{Ax=b}
$$

because:

$$
\begin{bmatrix}
2&3\\
4&1
\end{bmatrix}
\begin{bmatrix}
x\\
y
\end{bmatrix}
=
\begin{bmatrix}
2x+3y\\
4x+y
\end{bmatrix}
$$

So instead of writing two separate equations:

$$
2x+3y=8
$$

$$
4x+y=10
$$

we can write one matrix equation:

$$
Ax=b
$$

This is the doorway into **linear algebra**.

---

# 22. Why it's called "linear algebra"

You'll eventually study equations of the form:

$$
Ax=b
$$

Matrices provide a compact language for manipulating entire systems of linear relationships.

A useful big-picture hierarchy is:

```text
Numbers
   ↓
Vectors
   ↓
Matrices
   ↓
Systems of linear relationships
   ↓
Linear algebra
```

It's not merely "algebra with tables."

The deeper subject is about:

> **relationships and transformations in multidimensional spaces.**

Matrices are the main computational representation of those relationships.

---

# 23. A programming analogy

Since matrices are ultimately structured data, you could imagine one in C# as:

```csharp
double[,] matrix =
{
    { 1, 2, 3 },
    { 4, 5, 6 }
};
```

Conceptually:

```text
matrix[row, column]
```

So:

```csharp
matrix[0, 1]
```

would retrieve:

```text
2
```

Mathematics typically numbers positions starting at 1:

$$
a_{1,2}=2
$$

while programming languages commonly index from 0:

```csharp
matrix[0, 1] == 2
```

Same idea, different indexing convention.

---

# 24. The core concepts I'd learn first

Don't try to learn determinants, inverses, eigenvalues etc. yet.

Get these six things comfortable first:

1. **Reading a matrix**
2. **Rows and columns**
3. **Dimensions**
4. **Matrix addition**
5. **Scalar multiplication**
6. **Matrix multiplication**

Especially matrix multiplication.

If:

$$
A:m\times n
$$

and:

$$
B:n\times p
$$

then burn this structure into your intuition:

$$
\boxed{
(m\times n)(n\times p)
\rightarrow
m\times p
}
$$

And every element in the output comes from:

$$
\boxed{\text{row of A} \cdot \text{column of B}}
$$

---

# 25. Quick exercise

Don't calculate everything yet. Just answer whether the multiplication is possible and what the resulting dimensions would be.

### A

$$
(3\times4)(4\times2)
$$

### B

$$
(3\times4)(3\times2)
$$

### C

$$
(5\times2)(2\times7)
$$

### D

$$
(1\times3)(3\times1)
$$

Then calculate this one manually:

$$
\begin{bmatrix}
2&3
\end{bmatrix}
\begin{bmatrix}
4\\
5
\end{bmatrix}
$$

Send me your answers. **Matrix dimensions + matrix multiplication** are the two things I'd verify you've got before we move on to vectors, inverses, determinants and solving (Ax=b).
