import matplotlib.pyplot as plt
#import numpy
#import scipy
# matplotlib for plots, numpy for arrays, scipy for fitting

def main():
    problem4()
    problem5()

def problem4():
    # The number of years to repeat the model
    N = 5
    # starting number of workers working at the power plant
    workers = [4000]
    # start time at 1 just so it starts at 1 on the plot instead of 0
    time = [1]

    for i in range(N):
        for j in range(12):
            if j == 0:
                # 100 workers leave in January
                workers.append(workers[j + (i * 12)] - 100)
            elif j == 5:
                # 400 students arrive in June
                workers.append(workers[j + (i * 12)] + 400)
            elif j == 7:
                # 200 students leave in August
                workers.append(workers[j + (i * 12)] - 200)
            elif j == 11:
                # 200 workers retire in December
                workers.append(workers[j + (i * 12)] - 200)
            else:
                # otherwise the amount of workers stays the same
                workers.append(workers[j + (i * 12)])
            time.append(j + (i * 12) + 1)

    arrayLength = len(workers)
    result = "Amount of Workers after {} months: {}".format(arrayLength - 1, workers[arrayLength - 1])

    plt.plot(time, workers, color = 'green', label = 'Workers')
    plt.legend(loc = 'best')
    plt.ylabel("Number of Workers")
    plt.xlabel("Months Passed")
    plt.suptitle(result)
    plt.show()

def problem5():
    # for an entire population of 6000 people
    N = 6000
    # number of susceptible people, recovered people, and infected people
    S, R, I = [5090], [0], [10]
    # recovery percent and interaction coefficient
    a, b = 0.25, 5 / 50900
    # the number of weeks
    week = [0]

    j = 0
    while j < 100:
        S.append(S[j] - b * S[j] * I[j])
        I.append(I[j] + b * S[j] * I[j] - a * I[j])
        R.append(R[j] + a * I[j])
        week.append(j + 1)
        j += 1
    
    plt.plot(week, S, color = 'blue', label = 'Susceptible')
    plt.plot(week, I, color = 'red', label = 'Infected')
    plt.plot(week, R, color = 'green', label = 'Recovered')
    plt.legend(loc = 'best')
    plt.ylabel("Population")
    plt.xlabel("Weeks Passed")
    plt.show()

if __name__ == '__main__':
    main()