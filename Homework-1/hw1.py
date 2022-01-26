import matplotlib.pyplot as plt
#import numpy
#import scipy
# matplotlib for plots, numpy for arrays, scipy for fitting

def main():

    problem4()
    
    problem5()

    S = [995]
    I = [5]
    R = [0]
    a  = 7 / 4975
    time = [0]
    positive = 0
    j = 0
    while j < 100 and positive == 0:
        if S[j] - a * S[j] * I[j] < 0 or I[j] - 0.6 * I[j] + a * I[j] * S[j] < 0:
            positive = 1 
        else:
            S.append(S[j] - a * S[j] * I[j])
            I.append(I[j] - 0.6 * I[j] + a * I[j] * S[j])
            R.append(R[j] + 0.6 * I[j])
            time.append(j + 1)
            j = j + 1
    plt.plot(time, S, 'b-', label='S')
    plt.plot(time, I, 'r-', label='I')
    plt.plot(time, R, 'g-', label='R')
    plt.legend(loc = 'best')
    plt.show()

def problem4():
    # The number of years to repeat the model
    N = 5
    # starting number of workers working at the power plant
    workers = [4000]
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
    print("yeah")

if __name__ == '__main__':
    main()