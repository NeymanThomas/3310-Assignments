from turtle import right
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numpy.polynomial.polynomial import Polynomial as ply
from scipy.interpolate import lagrange

def main():
    problem_1()
    problem_2()
    problem_3()

# Code generously provided by professor
# This code is simply used to get the y value in a form that can be plotted
def PolyCoefficients(x, coeffs):
    o = len(coeffs)
    y = 0
    for i in range(o):
        # This line is changed so that it sorts in descending order instead of ascending
        y += coeffs[o - i - 1]*x**i
    return y

def problem_1():
    c = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    y = np.array([36, 70, 100, 150, 250, 502, 800, 1224])
    w = lagrange(c, y)
    plt.scatter(c, y)
    # use linspace to add 1000 extra points, showing more of a curve
    c = np.linspace(1, 8, 1000)
    # for extended results use code below instead
    #c = np.linspace(1, 10, 1000)
    plt.plot(c, PolyCoefficients(c, ply(w).coef), 'g-')
    plt.show()

def third_degree_poly(x, a, b, c, d):
    return a*x**3+b*x**2+c*x+d

def problem_2():
    c = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    y = np.array([36, 70, 100, 150, 250, 502, 800, 1224])
    plt.scatter(c, y)
    popt, pcov = curve_fit(third_degree_poly, c, y)
    c = np.linspace(1, 8, 1000)
    plt.plot(c, third_degree_poly(c, *popt), 'r-')
    plt.show()
    plt.figure()
    c = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    # This prints the values of our coefficients a, b, c, and d
    print(popt)
    print(sum((y - third_degree_poly(c, *popt))**3))

def second_degree_poly(x, a, b, c):
    return a*x**2+b*x+c

def problem_3():
    c = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    y = np.array([36, 70, 100, 150, 250, 502, 800, 1224])
    plt.scatter(c, y)
    popt, pcov = curve_fit(second_degree_poly, c, y)
    c = np.linspace(1, 12, 1000)
    plt.plot(c, second_degree_poly(c, *popt), 'purple')
    plt.show()
    plt.figure()
    c = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    # This prints the values of our coefficients a, b, and c
    print(popt)
    print(sum((y - second_degree_poly(c, *popt))**2))

if __name__ == '__main__':
    main()