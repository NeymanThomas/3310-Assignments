# python -m pip install nashpy
# https://nashpy.readthedocs.io/en/stable/tutorial/index.html#installing-nashpy
import nashpy as nash
import numpy as np
import math
from fractions import Fraction
from scipy.optimize import linprog


def main():
    problem_1()


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
def problem_1():
    #       Game Matrix
    #           a       b
    #       _________________
    #   a   |   8   |   3   |
    #       |-------|-------|
    #   b   |   2   |   6   |
    #       |-------|-------|
    # 
    #   a,a = 8   b,b = 3   b,a = 2   b,b = 6

    print("\nProblem 1:\nFor the given Game Matrix:\n\t\t\ta\t\tb\n\t\t_________________________________ \
    \n\ta\t|\t8\t|\t3\t|\n\t\t|---------------|---------------|\n\tb\t|\t2\t|\t6\t|\n\t\
    \t|---------------|---------------|\n")

    game_matrix = [[8, 3], [2, 6]]

    # get the oddment values: 4, 5, 3, 6
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



if __name__ == '__main__':
    main()