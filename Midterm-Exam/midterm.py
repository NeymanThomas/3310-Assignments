import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import random as rnd

def main():
    problem2()
    problem4()
    problem5()

def problem2():
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    y = np.array([50, 80, 250, 700, 2000, 3999, 5000, 7000])
    plyFit2(x, y)
    PlyFit3(x, y)
    PlyFit4(x, y)
    PlyFit5(x, y)

def plyFit2(x, y):
    plt.scatter(x, y)
    popt, pcov = curve_fit(second_degree_poly, x, y)
    c = x
    x = np.linspace(1, 8, 1000)
    plt.plot(x, second_degree_poly(x, *popt), 'r-')
    plt.title('Second Degree')
    plt.show()
    plt.figure()
    print("===Second Degree Polynomial===")
    for i in range(len(popt)):
        print("Coef: {} = {}".format(i+1, popt[i]))
    # https://stackoverflow.com/questions/19189362/getting-the-r-squared-value-using-curve-fit 
    ss_res = np.sum((y - second_degree_poly(c, *popt))**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r_squared = 1 - (ss_res / ss_tot)
    print("R squared: {}".format(r_squared))

def PlyFit3(x, y):
    plt.scatter(x, y)
    popt, pcov = curve_fit(third_degree_poly, x, y)
    c = x
    x = np.linspace(1, 8, 1000)
    plt.plot(x, third_degree_poly(x, *popt), 'g-')
    plt.title('Third Degree')
    plt.show()
    plt.figure()
    print("===Third Degree Polynomial===")
    for i in range(len(popt)):
        print("Coef: {} = {}".format(i+1, popt[i]))
    ss_res = np.sum((y - third_degree_poly(c, *popt))**3)
    ss_tot = np.sum((y - np.mean(y))**3)
    r_squared = 1 - (ss_res / ss_tot)
    print("R squared: {}".format(r_squared))

def PlyFit4(x, y):
    plt.scatter(x, y)
    popt, pcov = curve_fit(fourth_degree_poly, x, y)
    c = x
    x = np.linspace(1, 8, 1000)
    plt.plot(x, fourth_degree_poly(x, *popt), 'b-')
    plt.title('Fourth Degree')
    plt.show()
    plt.figure()
    print("===Fourth Degree Polynomial===")
    for i in range(len(popt)):
        print("Coef: {} = {}".format(i+1, popt[i]))
    ss_res = np.sum((y - fourth_degree_poly(c, *popt))**4)
    ss_tot = np.sum((y - np.mean(y))**4)
    r_squared = 1 - (ss_res / ss_tot)
    print("R squared: {}".format(r_squared))

def PlyFit5(x, y):
    plt.scatter(x, y)
    popt, pcov = curve_fit(fifth_degree_poly, x, y)
    c = x
    x = np.linspace(1, 8, 1000)
    plt.plot(x, fifth_degree_poly(x, *popt), 'purple')
    plt.title('Fifth Degree')
    plt.show()
    plt.figure()
    print("===Fifth Degree Polynomial===")
    for i in range(len(popt)):
        print("Coef: {} = {}".format(i+1, popt[i]))
    ss_res = np.sum((y - fifth_degree_poly(c, *popt))**5)
    ss_tot = np.sum((y - np.mean(y))**5)
    r_squared = 1 - (ss_res / ss_tot)
    print("R squared: {}".format(r_squared))

def second_degree_poly(x, a, b, c):
    return a*x**2+b*x+c

def third_degree_poly(x, a, b, c, d):
    return a*x**3+b*x**2+c*x+d

def fourth_degree_poly(x, a, b, c, d, e):
    return a*x**4+b*x**3+c*x**2+d*x+e

def fifth_degree_poly(x, a, b, c, d, e, f):
    return a*x**5+b*x**4+c*x**3+d*x**2+e*x+f

def problem4():
    # components ABC are series
    A = 0.98
    B = 0.97
    C = 0.96
    # components DE are parallel
    D = 0.95
    E = 0.94
    # components FG are parallel
    F = 0.93
    G = 0.92

    # first compute the parallel components
    par_1 = 1 - ((1 - D) * (1 - E))
    par_2 = 1 - ((1 - F) * (1 - G))
    print("D and E reliability: {:.3f}%\tF and G reliability: {:.3f}%".format(par_1, par_2))

    # compute the whole system with the series components
    complete_system = A * B * C * par_1 * par_2
    print("System reliability without component H: {:.3f}%".format(complete_system))

    # Now compute the mystery component H
    H = 0.8 / complete_system
    print("The reliability of component H must be {:.3f}%".format(H))

def problem5():
    # this is the monty hall problem. The statistics for the problem basically
    # come down to if you switch you have a 2/3 chance of winning and if you
    # stay with your original guess you have a 1/3 chance of winning. We know
    # if contestants 1 - 5 are selected it is a 1/3 chance the prize was chosen.
    # if contestant 6 was chosen, the chance is 2/3.

    # Constant variable for number of simulations so if you want to change the
    # number of times it runs, just change this one variable
    SIM_NUM = 1000
    attempts = []
    results = []
    prize_counter = 0

    # the 2's and 1's being appended to the list act as the ratio of the chance
    # so 2 means 2 out of 3 chance and 1 means 1 out of 3 chance
    for i in range(SIM_NUM):
        if rnd.randint(1, 6) == 6:
            attempts.append(2)
        else:
            attempts.append(1)
    
    # So we randomly make a number from 1 to 3. This is equivalent to choosing
    # one of the 3 doors to have the prize. We then see if the randomly generated
    # integer is greater than the value at the attempt index. 2 and 3 will be greater
    # than 1 66% of the time, which is the 1/3 chance. The other option 2 will be 
    # greater than the random integer only 33% of the time, which is the 2/3 chance.
    # So finally based on if the correct door was chosen or not, we assign a 
    # Binary true or false to a list of results 
    for j in attempts:
        if rnd.randint(1, 3) > j:
            results.append(False)
        else:
            results.append(True)
    
    # count up all the correct guesses
    for r in results:
        if r == True:
            prize_counter += 1

    final_odds = prize_counter / SIM_NUM
    print("The final odds are {}".format(final_odds))


if __name__ == '__main__':
    main()