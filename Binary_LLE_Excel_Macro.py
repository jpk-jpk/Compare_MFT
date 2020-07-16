import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Functions
def f(x1,t12, t21, a):
    return (1 - x1) * x1 * (t12 / (-np.exp(a * t12) * (-1 + x1) + x1) + t21 / (1+ (-1 + np.exp(a * t21)) * x1)) - (-1 + x1) * np.log(1 - x1) + x1 *np.log(x1)
def f1(x1, t12, t21, a):
    return t21 * ((-1 + x1) ** 2 - np.exp(a * t21) * x1 ** 2) / (1 + (-1 + np.exp(a* t21)) * x1) ** 2 + (np.exp(a * t12) * t12 * (-1 + x1) ** 2 - t12 * x1 **2) / (-np.exp(a * t12) * (-1 + x1) + x1) ** 2 - np.log(1 - x1) + np.log(x1)
def f2(x1, t12, t21, a):
    return 2 * np.exp(a * t12) * t12 / (np.exp(a * t12) * (-1 + x1) - x1) ** 3 - 2* np.exp(a * t21) * t21 / (1 + (-1 + np.exp(a * t21)) * x1) ** 3 + 1 / (x1 -x1 ** 2)
def f3(x1, t12, t21, a):
    return -6 * np.exp(a * t12) * (-1 + np.exp(a * t12)) * t12 / (-np.exp(a * t12) *(-1 + x1) + x1) ** 4 + ((-1 + 2 * x1) / (-1 + x1) ** 2 - 6 * t21 * (-1 +x1) / (1 + (-1 + np.exp(a * t21)) * x1) ** 4 + 6 * t21 * (-2 + x1) / (1 +(-1 + np.exp(a * t21)) * x1) ** 3 + 6 * t21 / (1 + (-1 + np.exp(a * t21)) *x1) ** 2) / x1 ** 2

#Finding Equal Area
def EAR(f2x1, f2x2, t12, t21, a):
    Phases = "LL"
    f1max = f1(f2x1, t12, t21, a)
    f1min = f1(f2x2, t12, t21, a)
    for i in range(30):
        f1mean = (f1max + f1min) / 2
        f1x1max = f2x1
        f1x1min = 0.0001
        for i in range(30):
            f1x1mean = (f1x1max + f1x1min) / 2
            if abs((f1x1max - f1x1min) / f1x1mean) < 0.00001:
                f1x1 = f1x1mean
                break
            elif f1(f1x1mean, t12, t21, a) > f1mean:
                f1x1max = f1x1mean
            else:
                f1x1min = f1x1mean

        f1x2max = 0.9999
        f1x2min = f2x2
        for i in range(30):
            f1x2mean = (f1x2max + f1x2min) / 2
            if abs((f1x2max - f1x2min) / f1x2mean) < 0.00001:
                f1x2 = f1x2mean
                break
            if f1(f1x2mean, t12, t21, a) > f1mean:
                f1x2max = f1x2mean
            else:
                f1x2min = f1x2mean

        area1 = f(f1x2, t12, t21, a) - f(f1x1, t12, t21, a)
        area2 = f1mean * (f1x2 - f1x1)
        if area2 < 0.00001:
            if abs(area1 - area2) < 0.00001:
                break
        else:
            if abs((area1 - area2) / area2) < 0.00001:
                break
        if area1 > area2:
            f1min = f1mean
        else:
            f1max = f1mean
    if abs(f1x1-f1x2)<0.0001:
        return "No Solution or Single Fluid Phase"
    else:
        return np.array([f1x1,f1x2,f2x1,f2x2])

def main_prgm(T, a_1, b, c, d):
    #Preset of handling unit of composition (usually 0.0001)
    unit = 0.0001

    #Preset of initial guess and convergence radius (do not change!!)
    init_min = unit / 10
    init_max = 1 - init_min
    isconverge = unit / 4
    delta_in_newton = unit / 100
    delta_in_bisection = unit / 100

    #Reading of NRTL parameters from Microsoft Excel Worksheet
    t12 = a_1[0] + b[0] / T + c[0] * np.log(T) + d[0] * T
    t21 = a_1[1] + b[1] / T + c[1] * np.log(T) + d[1] * T
    a = 0.2

    f2z = init_min
    trial = 1
    for i in range(30):
        f2zold = f2z
        f2z = f2zold - f2(f2zold, t12, t21, a) / f3(f2zold, t12, t21, a)
        if (f2z < 0 or f2z > 1) and trial == 1:
            trial = 2
            f2z = init_max
            continue
        elif (f2z < 0 or f2z > 1) and trial == 2:
            print("Single Phase")
            x1 = 0.0
            xx1 = 0.0
            return "No Solution or Single Fluid Phase"
        if abs((f2z - f2zold) / f2z) < delta_in_newton:
            break

    #Finding X_L and X_R for f''(x)=0 (Trial 1)
    f2xmin = init_min
    f2xmax = f2z
    for i in range(30):
        f2xmean = (f2xmax + f2xmin) / 2
        if abs((f2xmax - f2xmin) / f2xmean) < delta_in_bisection:
            break
        elif f2(f2xmean, t12, t21, a) > 0:
            f2xmin = f2xmean
        else:
            f2xmax = f2xmean
    if abs(f2z - f2xmean) > isconverge:
        f2x1 = f2xmean
        f2x2 = f2z
        return EAR(f2x1, f2x2, t12, t21, a)

    #Finding X_L and X_R for f''(x)=0 (Trial 2)
    f2xmin = f2z
    f2xmax = init_max
    for i in range(30):
        f2xmean = (f2xmax + f2xmin) / 2
        if abs((f2xmax - f2xmin) / f2xmean) < delta_in_bisection:
            break
        if f2(f2xmean, t12, t21, a) < 0:
            f2xmin = f2xmean
        else:
            f2xmax = f2xmean
    if np.round((f2z / unit), 4)!= np.round((f2xmean / unit), 4):
        f2x1 = f2z
        f2x2 = f2xmean
        Phases = "Critical"
        return EAR(f2x1, f2x2, t12, t21, a)
    else:
        return "No Solution or Single Fluid Phase"
    

def X_Change(system, comp1, comp2, parameters, tmin, tmax, step):
    plt.clf()
    a_1, b, c, d = parameters.T
    tmin += 273.15
    tmax += 273.15
    yy = pd.DataFrame()
    for i in np.arange(tmin,tmax, step):
        xx = main_prgm(i, a_1, b, c, d)
        if not isinstance(xx, str):
            xx = np.append(xx, i)
            yy = yy.append(pd.DataFrame(xx).T)
    yy.columns=['f1x1','f1x2','f2x1','f2x2', 'Temp(K)']
    yy['Temp(K)'] -= 273.15
    yy.columns=['f1x1','f1x2','f2x1','f2x2', 'Temp(C)']
    ax = yy.plot(x="f1x1",y="Temp(C)", color="blue", label="x1")
    yy.plot(x="f1x2",y="Temp(C)", color="r", label="xx1", ax=ax)
    ##yy.plot( x="f1x2",y="Temp(K)", color="g", label="f1x2", ax=ax)
    ##yy.plot( x="d",y="x", color="orange", label="b vs. d", ax=ax)
    ##yy.plot( x="a",y="x", color="purple", label="x vs. a", ax=ax)
    ax.set_xlabel("Mole Fraction of "+comp1)
    ax.set_ylabel("Temperature (C)")
    plt.title(system+'_'+comp1+'_'+comp2)
    plt.grid()
    plt.savefig("D:\\Output\\"+system+'_'+comp1+'_'+comp2+'.png')
    plt.close()
        
j = pd.read_csv(r'D:\PI 32\Sprint1\Olaya_data_for_python.csv')
for i in range(len(j)):
    parameters = np.array(j.loc[i, "Parameters"].strip("(").strip(")").split(","), dtype = 'float').reshape((2,4))
    tmin = float(j.loc[i, "Tmin"])
    tmax = float(j.loc[i, "Tmax"])
    step = float(j.loc[i, "step"])
    system = str(j.loc[i, "System"])
    comp1 = str(j.loc[i, "Component_i"])
    comp2 = str(j.loc[i, "Component_j"])
    #print(system, comp1, comp2, parameters, tmin, tmax, step)
    print(system, comp1, comp2)
    X_Change(system, comp1, comp2, parameters, tmin, tmax, step)
    print("System:",i+1, "Done")
    
