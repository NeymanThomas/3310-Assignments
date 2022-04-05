import numpy as np
from fractions import Fraction

def main():
    #simplex_1()
    copypasted()

# carpenter example looked at in class
def simplex_1():
    m = gen_matrix(2, 2)
    constrain(m, '20,30,L,690')
    constrain(m, '5,4,L,120')
    obj(m, '25,30,0')
    print(maxz(m))

def simplex_2():
    m = gen_matrix(2, 2)
    constrain(m, '2,-1,G,10')
    constrain(m, '1,1,L,20')
    obj(m, '5,10,0')
    print(maxz(m))

#https://www.geeksforgeeks.org/simplex-algorithm-tabular-method/
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
# c = [25, 30]
# A = [[20, 30], [5, 4]]
# b = [690, 120]

#####################################################################

"""
# Generate a numpy array with enough rows for each constraint plus the objective function
# and enough columns for the variables, slack variables, and the corresponding value.
def gen_matrix(var, cons):
    tab = np.zeros((cons + 1, var + cons + 2))
    return tab

# Checks to see if 1+ pivots are required due to a negative element in the furthest right column.
# This exculdes the bottom value.
def next_round_r(table):
    m = min(table[:-1, -1])
    if m >= 0:
        return False
    else:
        return True

# Checks to see if 1+ pivots are required due to a negative element in the bottom row.
# this excludes the final value.
def next_round(table):
    lr = len(table[:, 0])
    m = min(table[lr - 1, :-1])
    if m >= 0:
        return False
    else:
        return True

# determines where negative elements are located in the furthest right column
def find_neg_r(table):
    lc = len(table[0, :])
    m = min(table[:-1, lc - 1])
    if m <= 0:
        n = np.where(table[:-1, lc - 1] == m) [0][0]
    else:
        n = None
    return n

# determines where negative elements are located in the bottom row
def find_neg(table):
    lr = len(table[:, 0])
    m = min(table[lr - 1, :-1])
    if m <= 0:
        n = np.where(table[lr - 1, :-1] == m) [0][0]
    else:
        n = None
    return n

# finds the pivot element corresponding to the given table values
def loc_piv_r(table):
    total = []
    r = find_neg_r(table)
    row = table[r, :-1]
    m = min(row)
    c = np.where(row == m) [0][0]
    col = table[:-1, c]
    for i, b in zip(col, table[:-1, -1]):
        if i**2 > 0 and b/i > 0:
            total.append(b/i)
        else:
            total.append(10000)
    index = total.index(min(total))
    return [index, c]

# finds a pivot element corresponding to a negative element in the bottom row.
def loc_piv(table):
    if next_round(table):
        total = []
        n = find_neg(table)
        for i, b in zip(table[:-1, n], table[:-1. -1]):
            if b/i > 0 and i**2 > 0:
                total.append(b/i)
            else:
                total.append(10000)
        index = total.index(min(total))
        return [index, n]

# pivots about an element to remove the negative entry in the final column 
# or row and return the updated table.
def pivot(row,col,table):
    lr = len(table[:, 0])
    lc = len(table[0, :])
    t = np.zeros((lr, lc))
    pr = table[row, :]
    if table[row,col]**2 > 0:
        e = 1/table[row, col]
        r = pr*e
        for i in range(len(table[:, col])):
            k = table[i, :]
            c = table[i, col]
            if list(k) == list(pr):
                continue
            else:
                t[i, :] = list(k-r*c)
        t[row, :] = list(r)
        return t
    else:
        print('Cannot pivot on this element.')

# function used for user input. 'G' represents greater than or equal to and
# 'L' represents less than or equal to.
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

# function for solving minimization problems.
def convert_min(table):
    table[-1, :-2] = [-1*i for i in table[-1, :-2]]
    table[-1, -1] = -1*table[-1, -1]    
    return table

# function to generate only the required number of variables
def gen_var(table):
    lc = len(table[0, :])
    lr = len(table[:, 0])
    var = lc - lr - 1
    v = []
    for i in range(var):
        v.append('x'+str(i+1))
    return v

# Checks if +1 contraints can be added to the matrix. If false, the program will
# not allow the user to add additional constraints.
def add_cons(table):
    lr = len(table[:, 0])
    empty = []
    for i in range(lr):
        total = 0
        for j in table[i, :]:                       
            total += j**2
        if total == 0: 
            empty.append(total)
    if len(empty) > 1:
        return True
    else:
        return False

# function takes the tableau as an argument as well as the equation.
# This is converted using the previous function and will be inserted into
# the tableau.
def constrain(table,eq):
    if add_cons(table) == True:
        lc = len(table[0, :])
        lr = len(table[:, 0])
        var = lc - lr - 1      
        j = 0
        while j < lr:            
            row_check = table[j, :]
            total = 0
            for i in row_check:
                total += float(i**2)
            if total == 0:                
                row = row_check
                break
            j +=1
        eq = convert(eq)
        i = 0
        while i<len(eq) - 1:
            row[i] = eq[i]
            i += 1        
        row[-1] = eq[-1]
        row[var + j] = 1    
    else:
        print('Cannot add another constraint.')

# Checks to see if the objective function can be added.
def add_obj(table):
    lr = len(table[:, 0])
    empty = []
    for i in range(lr):
        total = 0        
        for j in table[i, :]:
            total += j**2
        if total == 0:
            empty.append(total)    
    if len(empty) == 1:
        return True
    else:
        return False

# Adds the objective function to the tableau if it satisfies add_obj()
def obj(table,eq):
    if add_obj(table) == True:
        eq = [float(i) for i in eq.split(',')]
        lr = len(table[:, 0])
        row = table[lr-1, :]
        i = 0        
        while i < len(eq) - 1:
            row[i] = eq[i]* 1
            i += 1
        row[-2] = 1
        row[-1] = eq[-1]
    else:
        print('You must finish adding constraints before the objective function can be added.')

# maximization function
def maxz(table):
    while next_round_r(table) == True:
        table = pivot(loc_piv_r(table)[0], loc_piv_r(table)[1], table)
    while next_round(table) == True:
        table = pivot(loc_piv(table)[0], loc_piv(table)[1], table)        
    lc = len(table[0, :])
    lr = len(table[:, 0])
    var = lc - lr - 1 
    i = 0
    val = {}
    for i in range(var):
        col = table[:, i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]            
            val[gen_var(table)[i]] = table[loc, -1]
        else:
            val[gen_var(table)[i]] = 0
    val['max'] = table[-1, -1]
    return val

# minimization function
def minz(table):
    table = convert_min(table)
    while next_round_r(table) == True:
        table = pivot(loc_piv_r(table)[0], loc_piv_r(table)[1], table)    
    while next_round(table) == True:
        table = pivot(loc_piv(table)[0], loc_piv(table)[1], table)       
    lc = len(table[0, :])
    lr = len(table[:, 0])
    var = lc - lr - 1
    i = 0
    val = {}
    for i in range(var):
        col = table[:, i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]             
            val[gen_var(table)[i]] = table[loc, -1]
        else:
            val[gen_var(table)[i]] = 0
            val['min'] = table[-1, -1]*-1
    return val

"""

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
                continue
            else:
                t[i,:] = list(k-r*c)
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
    else:
        print('Cannot add another constraint.')

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

# adds the onjective functio nto the matrix.
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
    else:
        print('You must finish adding constraints before the objective function can be added.')

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
        return val

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
        return 








def copypasted():
    print("\n                 ****SiMplex Algorithm ****\n\n")
    
    # inputs 
    
    # A will contain the coefficients of the constraints
    A = np.array([[1, 1, 0, 1], [2, 1, 1, 0]])
    # b will contain the amount of resources 
    b = np.array([8, 10])           
    # c will contain coefficients of objective function Z      
    c = np.array([1, 1, 0, 0])             
    
    # B will contain the basic variables that make identity matrix
    cb = np.array(c[3])
    B = np.array([[3], [2]])          
    # cb contains their corresponding coefficients in Z   
    cb = np.vstack((cb, c[2]))        
    xb = np.transpose([b])                 
    # combine matrices B and cb
    table = np.hstack((B, cb))             
    table = np.hstack((table, xb))         
    # combine matrices B, cb and xb
    # finally combine matrix A to form the complete simplex table
    table = np.hstack((table, A))         
    # change the type of table to float
    table = np.array(table, dtype ='float') 
    # inputs end
    
    # if min problem, make this var 1
    MIN = 0
    
    print("Table at itr = 0")
    print("B \tCB \tXB \ty1 \ty2 \ty3 \ty4")
    for row in table:
        for el in row:
                    # limit the denominator under 100
            print(Fraction(str(el)).limit_denominator(100), end ='\t') 
        print()
    print()
    print("Simplex Working....")
    
    # when optimality reached it will be made 1
    reached = 0     
    itr = 1
    unbounded = 0
    alternate = 0
    
    while reached == 0:
    
        print("Iteration: ", end =' ')
        print(itr)
        print("B \tCB \tXB \ty1 \ty2 \ty3 \ty4")
        for row in table:
            for el in row:
                print(Fraction(str(el)).limit_denominator(100), end ='\t')
            print()
    
        # calculate Relative profits-> cj - zj for non-basics
        i = 0
        rel_prof = []
        while i<len(A[0]):
            rel_prof.append(c[i] - np.sum(table[:, 1]*table[:, 3 + i]))
            i = i + 1
    
        print("rel profit: ", end =" ")
        for profit in rel_prof:
            print(Fraction(str(profit)).limit_denominator(100), end =", ")
        print()
        i = 0
        
        b_var = table[:, 0]
        # checking for alternate solution
        while i<len(A[0]):
            j = 0
            present = 0
            while j<len(b_var):
                if int(b_var[j]) == i:
                    present = 1
                    break
                j+= 1
            if present == 0:
                if rel_prof[i] == 0:
                    alternate = 1
                    print("Case of Alternate found")
                    # print(i, end =" ")
            i+= 1
        print()
        flag = 0
        for profit in rel_prof:
            if profit>0:
                flag = 1
                break
            # if all relative profits <= 0
        if flag == 0:
            print("All profits are <= 0, optimality reached")
            reached = 1
            break
    
        # kth var will enter the basis
        k = rel_prof.index(max(rel_prof))
        min = 99999
        i = 0;
        r = -1
        # min ratio test (only positive values)
        while i<len(table):
            if (table[:, 2][i]>0 and table[:, 3 + k][i]>0): 
                val = table[:, 2][i]/table[:, 3 + k][i]
                if val<min:
                    min = val
                    r = i     # leaving variable
            i+= 1
    
            # if no min ratio test was performed
        if r ==-1:
            unbounded = 1
            print("Case of Unbounded")
            break
    
        print("pivot element index:", end =' ')
        print(np.array([r, 3 + k]))
    
        pivot = table[r][3 + k]
        print("pivot element: ", end =" ")
        print(Fraction(pivot).limit_denominator(100))
            
            # perform row operations
        # divide the pivot row with the pivot element
        table[r, 2:len(table[0])] = table[
                r, 2:len(table[0])] / pivot
                
        # do row operation on other rows
        i = 0
        while i<len(table):
            if i != r:
                table[i, 2:len(table[0])] = table[i,
                    2:len(table[0])] - table[i][3 + k] * table[r, 2:len(table[0])]
            i += 1
    
        
        # assign the new basic variable
        table[r][0] = k
        table[r][1] = c[k]
        
        print()
        print()
        itr+= 1
        
    
    print()
    
    print("***************************************************************")
    if unbounded == 1:
        print("UNBOUNDED LPP")
        exit()
    if alternate == 1:
        print("ALTERNATE Solution")
    
    print("optimal table:")
    print("B \tCB \tXB \ty1 \ty2 \ty3 \ty4")
    for row in table:
        for el in row:
            print(Fraction(str(el)).limit_denominator(100), end ='\t')
        print()
    print()
    print("value of Z at optimality: ", end =" ")
    
    basis = []
    i = 0
    sum = 0
    while i<len(table):
        sum += c[int(table[i][0])]*table[i][2]
        temp = "x"+str(int(table[i][0])+1)
        basis.append(temp)
        i+= 1
    # if MIN problem make z negative
    if MIN == 1:
        print(-Fraction(str(sum)).limit_denominator(100))
    else:
        print(Fraction(str(sum)).limit_denominator(100))
    print("Final Basis: ", end =" ")
    print(basis)
    
    print("Simplex Finished...")
    print()

if __name__ == '__main__':
    main()