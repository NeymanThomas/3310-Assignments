import numpy as np
from fractions import Fraction

# Maximize f_1(X) = 25x1 + 30x2
# subject to: 
# 20x1 + 30x2 <= 690
# 5x1 + 4x2 <= 120
# x1, x2 >= 0
#
# We adjoin a new constraint to ensure that any solution improves the
# best value of the objective function found so far
# Add: -25x1 - 30x2 <= 0 - since all constraints must be <=
#
# We now have to do what we did before which is converting each inequality 
# to an equality, by adding in new slack variables.
#
# 20x1 + 30x2 + y1 = 690
# 5x1 + 4x2 + y2 = 120
# -25x1 - 20x2 + z = 0
#
# Some formatting for tables and processing ideas used with inspiration
# from the link:
# https://www.geeksforgeeks.org/simplex-algorithm-tabular-method/

def main():
    simplex_1()
    simplex_2()
    simplex_3()
    simplex_4()

# carpenter example looked at in class
def simplex_1():
    print("\n===== Carpenter Problem from class =====\n")
    m = gen_matrix(2, 2)
    print("Start:\n-------\t-------\t-------\t-------\t-------\t-------")
    print("x1 \tx2 \ty1 \ty2 \tz \tRHS")
    constrain(m, '20,30,L,690')
    constrain(m, '5,4,L,120')
    obj(m, '25,30,0')
    print("-----------------------------------------------\n\nRow Operations:", end="")
    print(maxz(m))

# Example 2 gone over in class
def simplex_2():
    print("\n===== Example 2 from class =====\n")
    m = gen_matrix(2, 2)
    print("Start:\n-------\t-------\t-------\t-------\t-------\t-------")
    print("x1 \tx2 \ty1 \ty2 \tz \tRHS")
    constrain(m, '2,1,L,6')
    constrain(m, '1,3,L,9')
    obj(m, '3,1,0')
    print("-----------------------------------------------\n\nRow Operations:", end="")
    print(maxz(m))

# Example using a 3 dimensional problem
def simplex_3():
    print("\n===== Example for 3D (1) =====\n")
    m = gen_matrix(3, 3)
    print("Start:\n-------\t-------\t-------\t-------\t-------\t-------\t-------\t-------")
    print("x1 \tx2 \tx3 \ty1 \ty2 \ty3 \tz \tRHS")
    constrain(m, '2,1,0,L,10')
    constrain(m, '1,2,-2,L,20')
    constrain(m, '0,1,2,L,5')
    obj(m, '2,-1,2,0')
    print("---------------------------------------------------------------\n\nRow Operations:", end="")
    print(maxz(m))

# Example using a 3 dimensional problem
def simplex_4():
    print("\n===== Example for 3D (2) =====\n")
    m = gen_matrix(3, 3)
    print("Start:\n-------\t-------\t-------\t-------\t-------\t-------\t-------\t-------")
    print("x1 \tx2 \tx3 \ty1 \ty2 \ty3 \tz \tRHS")
    constrain(m, '4,1,1,L,30')
    constrain(m, '2,3,1,L,60')
    constrain(m, '1,2,3,L,40')
    obj(m, '3,2,1,0')
    print("---------------------------------------------------------------\n\nRow Operations:", end="")
    print(maxz(m))


# generates an empty matrix with adequate size for variables and constraints.
def gen_matrix(var,cons):
    tab = np.zeros((cons+1, var+cons+2))
    return tab

# checks the furthest right column for negative values ABOVE the last row. If negative values exist, another pivot is required.
def next_round_r(table):
    m = min(table[:-1,-1])
    if m>= 0:
        return False
    else:
        return True

# checks that the bottom row, excluding the final column, for negative values. If negative values exist, another pivot is required.
def next_round(table):
    lr = len(table[:,0])
    m = min(table[lr-1,:-1])
    if m>=0:
        return False
    else:
        return True

# Similar to next_round_r function, but returns row index of negative element in furthest right column
def find_neg_r(table):
    # lc = number of columns, lr = number of rows
    lc = len(table[0,:])
    # search every row (excluding last row) in final column for min value
    m = min(table[:-1,lc-1])
    if m<=0:
        # n = row index of m location
        n = np.where(table[:-1,lc-1] == m)[0][0]
    else:
        n = None
    return n

#returns column index of negative element in bottom row
def find_neg(table):
    lr = len(table[:,0])
    m = min(table[lr-1,:-1])
    if m<=0:
        # n = row index for m
        n = np.where(table[lr-1,:-1] == m)[0][0]
    else:
        n = None
    return n

# locates pivot element in tableu to remove the negative element from the furthest right column.
def loc_piv_r(table):
        total = []
        # r = row index of negative entry
        r = find_neg_r(table)
        # finds all elements in row, r, excluding final column
        row = table[r,:-1]
        # finds minimum value in row (excluding the last column)
        m = min(row)
        # c = column index for minimum entry in row
        c = np.where(row == m)[0][0]
        # all elements in column
        col = table[:-1,c]
        # need to go through this column to find smallest positive ratio
        for i, b in zip(col,table[:-1,-1]):
            # i cannot equal 0 and b/i must be positive.
            if i**2>0 and b/i>0:
                total.append(b/i)
            else:
                # placeholder for elements that did not satisfy the above requirements. Otherwise, our index number would be faulty.
                total.append(0)
        element = max(total)
        for t in total:
            if t > 0 and t < element:
                element = t
            else:
                continue

        index = total.index(element)
        return [index,c]
# similar process, returns a specific array element to be pivoted on.
def loc_piv(table):
    if next_round(table):
        total = []
        n = find_neg(table)
        for i,b in zip(table[:-1,n],table[:-1,-1]):
            if i**2>0 and b/i>0:
                total.append(b/i)
            else:
                # placeholder for elements that did not satisfy the above requirements. Otherwise, our index number would be faulty.
                total.append(0)
        element = max(total)
        for t in total:
            if t > 0 and t < element:
                element = t
            else:
                continue

        index = total.index(element)
        return [index,n]

# Takes string input and returns a list of numbers to be arranged in tableu
def convert(eq):
    eq = eq.split(',')
    if 'G' in eq:
        g = eq.index('G')
        del eq[g]
        eq = [float(i)*-1 for i in eq]
        return eq
    if 'L' in eq:
        l = eq.index('L')
        del eq[l]
        eq = [float(i) for i in eq]
        return eq

# The final row of the tablue in a minimum problem is the opposite of a maximization problem so elements are multiplied by (-1)
def convert_min(table):
    table[-1,:-2] = [-1*i for i in table[-1,:-2]]
    table[-1,-1] = -1*table[-1,-1]
    return table

# generates x1,x2,...xn for the varying number of variables.
def gen_var(table):
    lc = len(table[0,:])
    lr = len(table[:,0])
    var = lc - lr -1
    v = []
    for i in range(var):
        v.append('x'+str(i+1))
    return v

# pivots the tableau such that negative elements are purged from the last row and last column
def pivot(row,col,table):
    # number of rows
    lr = len(table[:,0])
    # number of columns
    lc = len(table[0,:])
    t = np.zeros((lr,lc))
    pr = table[row,:]
    if table[row,col]**2>0: #new
        e = 1/table[row,col]
        r = pr*e
        for i in range(len(table[:,col])):
            k = table[i,:]
            c = table[i,col]
            if list(k) == list(pr):
                print()
                for j in list(k):
                    print(Fraction(str(j)).limit_denominator(100), end='\t')
                continue
            else:
                t[i,:] = list(k-r*c)
                print()
                for k in t[i,:]:
                    print(Fraction(str(k)).limit_denominator(100), end='\t')

        t[row,:] = list(r)
        return t
    else:
        print('Cannot pivot on this element.')

# checks if there is room in the matrix to add another constraint
def add_cons(table):
    lr = len(table[:,0])
    # want to know IF at least 2 rows of all zero elements exist
    empty = []
    # iterate through each row
    for i in range(lr):
        total = 0
        for j in table[i,:]:
            # use squared value so (-x) and (+x) don't cancel each other out
            total += j**2
        if total == 0:
            # append zero to list ONLY if all elements in a row are zero
            empty.append(total)
    # There are at least 2 rows with all zero elements if the following is true
    if len(empty)>1:
        return True
    else:
        return False

# adds a constraint to the matrix
def constrain(table,eq):
    if add_cons(table) == True:
        lc = len(table[0,:])
        lr = len(table[:,0])
        var = lc - lr -1
        # set up counter to iterate through the total length of rows
        j = 0
        while j < lr:
            # Iterate by row
            row_check = table[j,:]
            # total will be sum of entries in row
            total = 0
            # Find first row with all 0 entries
            for i in row_check:
                total += float(i**2)
            if total == 0:
                # We've found the first row with all zero entries
                row = row_check
                break
            j +=1

        eq = convert(eq)
        i = 0
        # iterate through all terms in the constraint function, excluding the last
        while i<len(eq)-1:
            # assign row values according to the equation
            row[i] = eq[i]
            i +=1
        #row[len(eq)-1] = 1
        row[-1] = eq[-1]

        # add slack variable according to location in tableau.
        row[var+j] = 1

        # print the row contents
        for i in row:
            print(i, end ='\t')
        print()
    else:
        print('Error: cannot add another constraint.')

# checks to determine if an objective function can be added to the matrix
def add_obj(table):
    lr = len(table[:,0])
    # want to know IF exactly one row of all zero elements exist
    empty = []
    # iterate through each row
    for i in range(lr):
        total = 0
        for j in table[i,:]:
            # use squared value so (-x) and (+x) don't cancel each other out
            total += j**2
        if total == 0:
            # append zero to list ONLY if all elements in a row are zero
            empty.append(total)
    # There is exactly one row with all zero elements if the following is true
    if len(empty)==1:
        return True
    else:
        return False

# adds the onjective function to the matrix.
def obj(table,eq):
    if add_obj(table)==True:
        eq = [float(i) for i in eq.split(',')]
        lr = len(table[:,0])
        row = table[lr-1,:]
        i = 0
    # iterate through all terms in the constraint function, excluding the last
        while i<len(eq)-1:
            # assign row values according to the equation
            row[i] = eq[i]*-1
            i +=1
        row[-2] = 1
        row[-1] = eq[-1]

        # print the row contents
        for i in row:
            print(i, end ='\t')
        print()
    else:
        print('Error in objective function: Constraints need to be added properly')

# solves maximization problem for optimal solution, returns dictionary w/ keys x1,x2...xn and max.
def maxz(table, output='summary'):
    while next_round_r(table)==True:
        table = pivot(loc_piv_r(table)[0],loc_piv_r(table)[1],table)
    while next_round(table)==True:
        table = pivot(loc_piv(table)[0],loc_piv(table)[1],table)

    lc = len(table[0,:])
    lr = len(table[:,0])
    var = lc - lr -1
    i = 0
    val = {}
    for i in range(var):
        col = table[:,i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[gen_var(table)[i]] = table[loc,-1]
        else:
            val[gen_var(table)[i]] = 0
    val['max'] = table[-1,-1]
    for k,v in val.items():
        val[k] = round(v,6)
    if output == 'table':
        return table
    else:
        return f"\n\nResult:\n{val}\n"

# solves minimization problems for optimal solution, returns dictionary w/ keys x1,x2...xn and min.
def minz(table, output='summary'):
    table = convert_min(table)

    while next_round_r(table)==True:
        table = pivot(loc_piv_r(table)[0],loc_piv_r(table)[1],table)
    while next_round(table)==True:
        table = pivot(loc_piv(table)[0],loc_piv(table)[1],table)

    lc = len(table[0,:])
    lr = len(table[:,0])
    var = lc - lr -1
    i = 0
    val = {}
    for i in range(var):
        col = table[:,i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[gen_var(table)[i]] = table[loc,-1]
        else:
            val[gen_var(table)[i]] = 0
    val['min'] = table[-1,-1]*-1
    for k,v in val.items():
        val[k] = round(v,6)
    if output == 'table':
        return table
    else:
        return f"\n\nResult:\n{val}\n"


if __name__ == '__main__':
    main()