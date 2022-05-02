# Thomas Neyman
# MATH 3310
# May 2 2022

# python -m pip install nashpy
# https://nashpy.readthedocs.io/en/stable/tutorial/index.html#installing-nashpy
import nashpy as nash
import numpy as np
from fractions import Fraction
from scipy.optimize import linprog


def main():
    # change the values for the game matrix to create a new game
    oddments_game_matrix = [[8, 3], [2, 6]]
    #oddments_game_matrix = [[1, -1], [-1, 1]]
    problem_1(oddments_game_matrix)

    problem_2()

    problem_3()


"""
======================================================================
Method used for oddments:
1. Subtract the 2 digits in the first column and write the difference
under the second column ignoring the sign.
2. Subtract the 2 digits in the second column and write the difference
under the first column ignoring the sign.
3. repeat the first 2 steps for the rows.
4. calculate the oddments to determine the best strategy for each player.


                    Cost Matrix for game:

                        Player B
                    ____a_______b____           _________________
           Choice a |  a,a  |  a,b  |           |   2   |   5   |
Player A            |-------|-------|   -->     |-------|-------|
           Choice b |  b,a  |  b,b  |           |   3   |  -3   |
                    |-------|-------|           |-------|-------|


Oddments    |   b,a - b,b   |   a,b - a,a   |   a,b - b,b   |   b,a - a,a   |
            |               |               |               |               |
            | 3 - (-3) = 6  |   5 - 2 = 3   | 5 - (-3) = 8  |   3 - 2 = 1   |
            |               |               |               |               |
            |   P_A a = 6   |   P_A b = 3   |   P_B a = 8   |   P_B b = 1   |

    The value of the row and column oddments should add up to the same
    value. Taking the rows and the columns: 
            6 + 3 == 8 + 1
    
    Probability of Player A using oddment a ->  6 / (6 + 3) = 2/3
    Probability of Player A using oddment b ->  3 / (6 + 3) = 1/3
    Probability of Player B using oddment a ->  8 / (8 + 1) = 8/9
    Probability of Player B using oddment b ->  1 / (8 + 1) = 1/9

    Value of the game:
    Take the first row, multiply a and b by their respective column oddments.
    Then divide the value by the total of oddments
    ((2 * 8) + (5 * 1)) / 9  = 7/3

    So in conclusion, Player A should go with choice a and Player B
    should go with choice a, as well. 

======================================================================
"""

# function solves a 2 player, total conflict game using oddments method
# both player's optimal choices are returned and their overall outcome
def problem_1(game_matrix):
    #       Game Matrix
    #           a       b
    #       _________________
    #   a   |   8   |   3   |
    #       |-------|-------|
    #   b   |   2   |   6   |
    #       |-------|-------|
    # 
    #   a,a = 8   b,b = 3   b,a = 2   b,b = 6

    print("\n_____Problem 1:_____\nFor the given Game Matrix:\n\t\t\ta\t\tb\n\t\t_________________________________ \
    \n\ta\t|\t{}\t|\t{}\t|\n\t\t|---------------|---------------|\n\tb\t|\t{}\t|\t{}\t|\n\t\
    \t|---------------|---------------|\n".format(game_matrix[0][0], game_matrix[0][1], game_matrix[1][0], game_matrix[1][1]))

    # get the oddment values
    oddment_row_a = abs(game_matrix[1][1] - game_matrix[1][0])
    oddment_row_b = abs(game_matrix[0][1] - game_matrix[0][0])
    oddment_column_a = abs(game_matrix[0][1] - game_matrix[1][1])
    oddment_column_b = abs(game_matrix[0][0] - game_matrix[1][0])

    # determine the probabilities
    row_a_prob = Fraction(oddment_row_a, (oddment_row_a + oddment_row_b))
    row_b_prob = Fraction(oddment_row_b, (oddment_row_a + oddment_row_b))
    column_a_prob = Fraction(oddment_column_a, (oddment_column_a + oddment_column_b))
    column_b_prob = Fraction(oddment_column_b, (oddment_column_a + oddment_column_b))

    # calculate the game Value
    game_value = ((game_matrix[0][0] * oddment_column_a) + (game_matrix[0][1] * oddment_column_b)) / oddment_row_a + oddment_row_b

    # now determine which player chooses what
    i, j = None, None

    print("For player A choosing rows and Player B choosing columns:")
    if row_a_prob > row_b_prob:
        i = 0
        print("Player A is more likely to choose choice 'a', with a probability of ", row_a_prob)
    else:
        i = 1
        print("Player A is more likely to choose choice 'b', with a probability of ", row_b_prob)
    
    if column_a_prob > column_b_prob:
        j = 0
        print("Player B is more likely to choose choice 'a', with a probability of ", column_a_prob)
    else:
        j = 1
        print("Player B is more likely to choose choice 'b', with a probability of ", column_b_prob)
    
    outcome = game_matrix[i][j]
    print("This will result in an outcome score of ", outcome)
    print("The total game value is ", game_value, end='\n\n')


"""
                Problem 2 Game Matrix:

              a           b           c
        _____________________________________
    a   |   -2,2    |   2,-2    |    0,0    |
        |-----------|-----------|-----------|  
    b   |   -1,1    |   -2,2    |   2,-2    |
        |-----------|-----------|-----------|
    c   |   2,-2    |   1,-1    |   -2,2    |
        |-----------|-----------|-----------|
"""
def problem_2():

    # player A and B cost matrix
    A = np.array([[-2, 2, 0], [-1, -2, 2], [2, 1, -2]])
    B = np.array([[2, -2, 0], [1, 2, -2], [-2, -1, 2]])

    # rock paper scissors
    #A = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])
    #B = np.array([[0, 1, -1], [-1, 0, 1], [1, -1, 0]])

    print("\n_____Problem 2:_____\nFor the given Game Matrix:\n\t\t\ta\t\tb\t\tc\n\t\t_________________________________________________ \
    \n\ta\t|\t{},{}\t|\t{},{}\t|\t{},{}\t|\t\n\t\t|---------------|---------------|---------------|\n\tb\t|\t{},{}\t|\t{},{}\t|\t{},{}\t|\t\n\t\
    \t|---------------|---------------|---------------|\n\tc\t|\t{},{}\t|\t{},{}\t|\t{},{}\t|\t\n\t\t|---------------|---------------|---------------|\n\
    ".format(A[0][0], B[0][0], A[0][1], B[0][1], A[0][2], B[0][2], A[1][0], B[1][0], A[1][1], B[1][1], A[1][2], B[1][2],\
        A[2][0], B[2][0], A[2][1], B[2][1], A[2][2], B[2][2]))

    game1 = nash.Game(A, B)

    # show what kind of game is being played
    print(game1, end='\n\n')

    # find the Nash Equilibrium 
    equilibria = game1.support_enumeration()
    for i in equilibria:
        print(i)
    
    # Explain the values given by the equilibria
    print("\nPlayer A has the same probability of choosing option 'b' or 'c'")
    print("Player B's highest probability is to choose option 'c'")

    print("\nSo if both players chose their optimal choice, the outcome would be at position\n'b,c' or 'c,c', since Player A has two equally optimal choices.")
    print("outcome 1: ({} {})\noutcome 2: ({} {})".format(A[1][2], B[1][2], A[2][2], B[2][2]))

    # Code taken from Nash.py in class
    G = 1-A
    (n,m) = np.shape(G)
    A_ub = -np.transpose(G)

    # we add an artificial variable to maximize, present in all inequalities
    A_ub = np.append(A_ub, np.ones((m,1)), axis = 1)

    # all inequalities should be inferior to 0
    b_ub = np.zeros(m)

    # the sum of all variables except the artificial one should be equal to one
    A_eq = np.ones((1,n+1))
    A_eq[0][n] = 0
    b_eq = 1
    c = np.zeros(n + 1)

    # -1 to maximize the artificial variable we’re going to add
    c[n] = -1
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
    bounds=(0,None),method='revised simplex')
    print((res.x[:-1], -res.fun), end='\n\n')


"""
                Problem 3 Game Matrix:

              a           b           c
        _____________________________________
    a   |   -2,2    |   2,-2    |    0,0    |
        |-----------|-----------|-----------|  
    b   |   -1,1    |   -2,2    |   2,-2    |
        |-----------|-----------|-----------|
    c   |   2,-2    |   1,-1    |   -2,2    |
        |-----------|-----------|-----------|

    Player A has the best results in row c, since there are 2 positives and only 1
    negative. So it is in Player A's best interest to get player B to choose anything
    but c, preferably a.
    
    On the other hand, Player B has the best results in column a, able to get a 2 or
    1, with a chance of getting -2. It is in Player B's best interest to get Player A
    to choose anything but c, preferably a.

    Option 1:

    Player B states that they will choose option 'a' not matter what. They have the 
    best odds of getting a positive score in that column, after all.

    Player A threatens that if Player B doesn't change their choice , they
    will always choose 'c'.

    This is a threat because this action would be harmful to Player B. 

    After making this threat, the available outcomes are as follows:

              a           b           c
        _____________________________________
    a   |   -2,2    |     X     |     X     |
        |-----------|-----------|-----------|  
    b   |   -1,1    |     X     |     X     |
        |-----------|-----------|-----------|
    c   |   2,-2    |     X     |     X     |
        |-----------|-----------|-----------|
    
    Player A can either commit to their threat and force the outcome to be (2, -1) or
    they can choose 'a' or 'b'. They would never want to do this however unless they 
    thought player B was lying.

    Option 2:

    Player B promises Player A that if they don't choose option 'c', they won't choose
    option 'c' either. This is a promise because player A doesn't want player B to 
    choose option 'c' ideally, and player B just saved player A from getting a double
    'c' outcome, resulting in a -2 for them.

    Player A can either keep the promise that was made or choose option 'c' anyway. They
    would never want to choose 'b', since there is no positive outcome for them if
    player B stays true to their promise, so they will either choose 'a' or 'c' anyway.

    After making this promise, the available outcomes are as follows:

              a           b           c
        _____________________________________
    a   |   -2,2    |    2,-2   |     X     |
        |-----------|-----------|-----------|  
    b   |   -1,1    |    -2,2   |     X     |
        |-----------|-----------|-----------|
    c   |   2,-2    |    1,-1   |     X     |
        |-----------|-----------|-----------|
"""
def problem_3():
    # player A and B cost matrix
    A = np.array([[-2, 2, 0], [-1, -2, 2], [2, 1, -2]])
    B = np.array([[2, -2, 0], [1, 2, -2], [-2, -1, 2]])

    print("\n_____Problem 3:_____\nFor the given Game Matrix:\n\t\t\ta\t\tb\t\tc\n\t\t_________________________________________________ \
    \n\ta\t|\t{},{}\t|\t{},{}\t|\t{},{}\t|\t\n\t\t|---------------|---------------|---------------|\n\tb\t|\t{},{}\t|\t{},{}\t|\t{},{}\t|\t\n\t\
    \t|---------------|---------------|---------------|\n\tc\t|\t{},{}\t|\t{},{}\t|\t{},{}\t|\t\n\t\t|---------------|---------------|---------------|\n\
    ".format(A[0][0], B[0][0], A[0][1], B[0][1], A[0][2], B[0][2], A[1][0], B[1][0], A[1][1], B[1][1], A[1][2], B[1][2],\
        A[2][0], B[2][0], A[2][1], B[2][1], A[2][2], B[2][2]))

    print("\nOption 1:\nPlayer B states they will choose 'a' no matter what.")
    print("Player A threatens that if they don't change their choice, they will choose 'c'.")
    print("After this threat, the available outcomes are as follows:")

    print("\t\t\ta\t\tb\t\tc\n\t\t_________________________________________________ \
    \n\ta\t|\t{},{}\t|\tX\t|\tX\t|\t\n\t\t|---------------|---------------|---------------|\n\tb\t|\t{},{}\t|\tX\t|\tX\t|\t\n\t\
    \t|---------------|---------------|---------------|\n\tc\t|\t{},{}\t|\tX\t|\tX\t|\t\n\t\t|---------------|---------------|---------------|\n\
    ".format(A[0][0], B[0][0], A[1][0], B[1][0], A[2][0], B[2][0]))

    # option 1
    A = np.array([[-2], [-1], [2]])
    B = np.array([[2], [1], [-2]])

    game2 = nash.Game(A, B)

    # show what kind of game is being played
    print(game2, end='\n\n')

    # find the Nash Equilibrium 
    equilibria = game2.support_enumeration()
    for i in equilibria:
        print(i)
    
    print("Player A can only choose 'c' here for a positive outcome.")
    print("Player B can't make a decision, they decided they would only choose 'a'.")
    print("So the outcome is going to be ", A[2], B[2])

    # Code taken from Nash.py in class
    G = 1-A
    (n,m) = np.shape(G)
    A_ub = -np.transpose(G)

    # we add an artificial variable to maximize, present in all inequalities
    A_ub = np.append(A_ub, np.ones((m,1)), axis = 1)

    # all inequalities should be inferior to 0
    b_ub = np.zeros(m)

    # the sum of all variables except the artificial one should be equal to one
    A_eq = np.ones((1,n+1))
    A_eq[0][n] = 0
    b_eq = 1
    c = np.zeros(n + 1)

    # -1 to maximize the artificial variable we’re going to add
    c[n] = -1
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
    bounds=(0,None),method='revised simplex')
    print((res.x[:-1], -res.fun))

    # original cost matrix
    A = np.array([[-2, 2, 0], [-1, -2, 2], [2, 1, -2]])
    B = np.array([[2, -2, 0], [1, 2, -2], [-2, -1, 2]])

    print("\nOption 2:\nPlayer B promises Player A that if they don't choose option 'c', they won't choose option 'c' either.")
    print("Player A can either keep the promise that was made or choose option 'c' anyway.")
    print("After this promise, the available outcomes are as follows:")

    print("\t\t\ta\t\tb\t\tc\n\t\t_________________________________________________ \
    \n\ta\t|\t{},{}\t|\t{},{}\t|\tX\t|\t\n\t\t|---------------|---------------|---------------|\n\tb\t|\t{},{}\t|\t{},{}\t|\tX\t|\t\n\t\
    \t|---------------|---------------|---------------|\n\tc\t|\t{},{}\t|\t{},{}\t|\tX\t|\t\n\t\t|---------------|---------------|---------------|\n\
    ".format(A[0][0], B[0][0], A[0][1], B[0][1], A[1][0], B[1][0], A[1][1], B[1][1], A[2][0], B[2][0], A[2][1], B[2][1]))

    # option 2
    A = np.array([[-2, 2], [-1, -2], [2, 1]])
    B = np.array([[2, -2], [1, 2], [-2, -1]])

    game3 = nash.Game(A, B)

    # show what kind of game is being played
    print(game3, end='\n\n')

    # find the Nash Equilibrium 
    equilibria = game3.support_enumeration()
    for i in equilibria:
        print(i)
    
    print("Player A has a 20 80 split between 'a' and 'c' respectively, so they are most likely to choose 'c'.")
    print("Player B has a 20 80 split between 'a' and 'b' respectively, so they are most likely to choose 'b'")
    print("So the outcome is going to be ", A[2][1], B[2][1])

    # Code taken from Nash.py in class
    G = 1-A
    (n,m) = np.shape(G)
    A_ub = -np.transpose(G)

    # we add an artificial variable to maximize, present in all inequalities
    A_ub = np.append(A_ub, np.ones((m,1)), axis = 1)

    # all inequalities should be inferior to 0
    b_ub = np.zeros(m)

    # the sum of all variables except the artificial one should be equal to one
    A_eq = np.ones((1,n+1))
    A_eq[0][n] = 0
    b_eq = 1
    c = np.zeros(n + 1)

    # -1 to maximize the artificial variable we’re going to add
    c[n] = -1
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
    bounds=(0,None),method='revised simplex')
    print((res.x[:-1], -res.fun))


if __name__ == '__main__':
    main()