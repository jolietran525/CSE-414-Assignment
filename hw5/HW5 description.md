**CSE 414 Homework 5: Transactions**

**Objectives:** To evaluate the properties of transaction schedules, and write transaction statements that would be used in an application.

**Assignment tools:**

- Any word processing or drawing tools you prefer (e.g., Google docs to pdf, Word, [draw.io](https://www.draw.io/)).

**Assigned date:** Monday, November 7th

**Due date:** Monday, November 14th, 11pm

**What to turn in:** See submission instructions at the bottom.

**Assignment Details**

**Part 1:** Schedules and Anomalies (10 points)

Consider a database with objects X, Y, and Z and assume that there are two transactions T1 and T2 that attempt the following operations.

T1: R(X), R(Y), W(X)

T2: R(X), R(Y), W(Y), R(X), R(Y), W(X), R(Z), W(Z)

1) Write an example schedule that interleaves operations between T1 and T2, that is NOT conflict serializable.
1) If T1 is instead just “R(X)”, this corresponds to T1 just being a single query like

SELECT \* FROM Flights WHERE id=1024;

Should the database treat a single SQL statement like this as a transaction? Why or why not?

Part 2: Conflict Serializability (20 points)

Consider the following three transactions and schedule (time goes from top to bottom). Is this schedule conflict-serializable? Show why or why not.

T1 T2 T3 R(A)![](Aspose.Words.e9a9452c-1e8e-44cc-ae5d-4ad1328ab236.001.png)

W(A)

R(A) W(A)

R(A)

R(B)

R(B) W(B)

W(B)

R(B) commit

commit

commit

Part 3: Two-Phase Locking (20 points)

1) Now modify the above schedule by adding locks, which may block some transactions from doing their operations until the lock is released. You’ll need to **rewrite** the above schedule in a table form. (The lecture slides show how to represent blocking in your schedules.)

Use two-phase locking (doesn’t need to be “strict”) in your modified schedule to ensure a conflict-serializable schedule for the transactions above.

Use the notation L(A) to indicate that the transaction acquires the lock on element A and U(A) to indicate that the transaction releases its lock on.

2) If 2PL ensures conflict-serializability, why do we need strict 2PL? Explain briefly.

**Submission Instructions**

The files you will need to submit to Gradescope

- Part1.pdf
- Part2.pdf
- Part3.pdf

*Points may be deducted for incorrect file names.* Submit your answers to Gradescope.
