import random as rnd
import numpy as np

ITERATIONS = 12

# A table is filled with values that represent the table in the homework.
# From there, 3 separate methods for solving this problem are run. The first
# method is how I thought about the problem and also how I rationalized my
# decision. The first method only chooses 1 option from the 4 available 
# choices in the list. To me, this is essentially 25% chance. Only one out
# of the four options would be chosen. HOWEVER, randomness and probability
# don't work that way, so a second function that ACTUALLY determines if the
# nature is used based on a 25% chance is used instead. The problem with the
# second method is that all rows must have the same result, so if A chose E,
# then B C and D must also choose E. This mistake is fixed in method 3.
def main():
    table = np.array([[7,10,-30,25],
                        [3,3,3,3],
                        [2,2,10,-2],
                        [6,9,10,-13]])
    method_1(table)
    method_2(table)
    method_3(table)

# simple method that chooses one out of the 4 options from the list of options
def method_1(table):
    A, B, C, D = 0, 0, 0, 0

    for i in range(ITERATIONS):
        A = A + rnd.choice(table[0])
        B = B + rnd.choice(table[1])
        C = C + rnd.choice(table[2])
        D = D + rnd.choice(table[3])

    print("\n===== METHOD 1 =====\n")
    print(f"After {ITERATIONS} iterations, the results for each choice are:")
    print(f"A: {A}\nB: {B}\nC: {C}\nD: {D}")

# method that actually determines the 25% chance each time an option is being decided
def method_2(table):
    A, B, C, D = 0, 0, 0, 0

    for i in range(ITERATIONS):
        A = A + choose_A(table[0])
        B = B + choose_B(table[1])
        C = C + choose_C(table[2])
        D = D + choose_D(table[3])
    
    print("\n===== METHOD 2 =====\n")
    print(f"After {ITERATIONS} iterations, the results for each choice are:")
    print(f"A: {A}\nB: {B}\nC: {C}\nD: {D}")

# method using the correct approach for solving the problem, using the same result
# for each row instea of independent results.
def method_3(table):
    A, B, C, D = 0, 0, 0, 0

    for i in range(ITERATIONS):
        # see if E was chosen
        if rnd.random() <= 0.25:
            A = A + table[0][0]
            B = B + table[1][0]
            C = C + table[2][0]
            D = D + table[3][0]
        # see if F was chosen
        if rnd.random() <= 0.25:
            A = A + table[0][1]
            B = B + table[1][1]
            C = C + table[2][1]
            D = D + table[3][1]
        # see if G was chosen
        if rnd.random() <= 0.25:
            A = A + table[0][2]
            B = B + table[1][2]
            C = C + table[2][2]
            D = D + table[3][2]
        # see if H was chosen
        if rnd.random() <= 0.25:
            A = A + table[0][3]
            B = B + table[1][3]
            C = C + table[2][3]
            D = D + table[3][3]

    print("\n===== METHOD 3 (correct) =====\n")
    print(f"After {ITERATIONS} iterations, the results for each choice are:")
    print(f"A: {A}\nB: {B}\nC: {C}\nD: {D}")

def choose_A(row):
    a = 0
    for i in range(len(row)):
        if rnd.random() <= 0.25:
            a = a + row[i]
    return a

def choose_B(row):
    b = 0
    for i in range(len(row)):
        if rnd.random() <= 0.25:
            b = b + row[i]
    return b

def choose_C(row):
    c = 0
    for i in range(len(row)):
        if rnd.random() <= 0.25:
            c = c + row[i]
    return c

def choose_D(row):
    d = 0
    for i in range(len(row)):
        if rnd.random() <= 0.25:
            d = d + row[i]
    return d


if __name__ == '__main__':
    rnd.seed(15)
    main()