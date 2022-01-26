import matplotlib.pyplot as plt
#import numpy
#import scipy
# matplotlib for plots, numpy for arrays, scipy for fitting

def main():
    S=[995]
    I=[5]
    R=[0]
    a=7/4975
    time=[0]
    positive=0
    j=0
    while j <100 and positive==0:
        if S[j]-a*S[j]*I[j] < 0 or I[j]-0.6*I[j]+a*I[j]*S[j] < 0:
            positive=1
        else:
            S.append(S[j]-a*S[j]*I[j])
            I.append(I[j]-0.6*I[j]+a*I[j]*S[j])
            R.append(R[j]+0.6*I[j])
            time.append(j+1)
            j=j+1
    plt.plot(time, S, 'b-', label='S')
    plt.plot(time, I, 'r-', label='I')
    plt.plot(time, R, 'g-', label='R')
    plt.legend(loc='best')
    plt.show()

def problem4():
    print("problem 4")

if __name__ == '__main__':
    main()