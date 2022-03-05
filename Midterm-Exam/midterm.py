import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def main():
    #problem2()
    problem4()

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

if __name__ == '__main__':
    main()