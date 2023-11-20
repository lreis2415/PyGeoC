import pandas as pd
import numpy as np
import math
import glob
import datetime
import time
from itertools import groupby

# from https://github.com/dmbrmv/BFI_python/blob/main/BFI.ipynb

def clump_array(a):
    """
    Split array for arrays w/o NaN
    """
    return [np.float64(a[s]) for s in np.ma.clump_unmasked(np.ma.masked_invalid(a))]


"""
Calculation only applicable to array w/o NaN. 
If some exist an array is splitting with function called clump_array

BFI calculation will be applied to every clump independently

"""
###################################################################

"""
First pass
"""


def FirstPass(Q, alpha):
    q_f_1 = [np.float64(np.NaN) for i in Q]
    q_b_1 = [np.float64(np.NaN) for i in Q]

    q_f_1[0] = Q[0]

    for j in range(len(Q) - 1):
        """
        for every split calculate quick flow

        """
        q_f_1[j + 1] = alpha * q_f_1[j] + 0.5 * (1 + alpha) * (Q[j + 1] - Q[j])

    for j in range(len(Q)):
        if q_f_1[j] < 0:
            q_b_1[j] = Q[j]
        else:
            q_b_1[j] = Q[j] - q_f_1[j]

    Q_forward_1 = [q_f_1, q_b_1]

    return Q_forward_1


###################################################################
"""
Backward pass

"""


def BackwardPass(Q_forward_1, alpha):
    """
    Q - n-dimensional list depend on the number of clumps
    """

    Qq = Q_forward_1[0]
    Qb = Q_forward_1[1]

    q_f_2 = [np.float64(np.NaN) for i in Qq]
    q_b_2 = [np.float64(np.NaN) for i in Qb]

    "last value of forward step - first in backward step"

    q_f_2[-1] = Qb[-1]

    for j in range(len(Qq) - 2, -1, -1):
        q_f_2[j] = alpha * q_f_2[j + 1] + 0.5 * (1 + alpha) * (Qb[j] - Qb[j + 1])

    for j in range(len(Qq) - 1, -1, -1):
        if q_f_2[j] < 0:
            q_b_2[j] = Qb[j]
        else:
            q_b_2[j] = Qb[j] - q_f_2[j]

    Q_backward = [q_f_2, q_b_2]

    return Q_backward


###################################################################
"""
Forward pass

"""


def ForwardPass(Q_backward, alpha):
    Qq = Q_backward[0]
    Qb = Q_backward[1]

    q_f_3 = [np.float64(np.NaN) for i in Qq]
    q_b_3 = [np.float64(np.NaN) for i in Qb]

    "Now first value of previous step - first here as well"

    q_f_3[0] = Qb[0]

    for j in range(len(Qb) - 1):
        q_f_3[j + 1] = alpha * q_f_3[j] + 0.5 * (1 + alpha) * (Qb[j + 1] - Qb[j])

    for j in range(len(Qb)):
        if q_f_3[j] < 0:
            q_b_3[j] = Qb[j]
        else:
            q_b_3[j] = Qb[j] - q_f_3[j]

    Q_forward = [q_f_3, q_b_3]

    return Q_forward


###################################################################
"""
BFI calculations for given alpha

"""


def BFI_calc(Q, alpha, passes, reflect):
    """
    we reflect the first reflect values and the last reflect values.
    this is to get rid of 'warm up' problems © Anthony Ladson
    """
    Qin = Q

    "reflect our lists"

    if len(Q) - 1 > reflect:
        Q_reflect = np.array([np.float64(np.NaN) for _ in range(len(Q) + 2 * reflect)], dtype=np.float64)

        Q_reflect[:reflect] = Q[(reflect):0:-1]
        Q_reflect[(reflect):(reflect + len(Q))] = Q
        Q_reflect[(reflect + len(Q)):(len(Q) + 2 + 2 * reflect)] = Q[len(Q) - 2:len(Q) - reflect - 2:-1]

    else:
        Q_reflect = np.array([np.float64(np.NaN) for _ in range(len(Q))], dtype=np.float64)
        Q_reflect = Q

    Q1 = FirstPass(Q_reflect, alpha)

    "how many backwards/forward passes to we need © Anthony Ladson"

    n_pass = round(0.5 * (passes - 1))

    BackwardPass(Q1, alpha)

    for i in range(n_pass):
        Q1 = ForwardPass(BackwardPass(Q1, alpha), alpha)

    ################# end of passes  ##############################
    if len(Q) - 1 > reflect:
        Qbase = Q1[1][reflect:(len(Q1[1]) - reflect)]
        Qbase = [0 if j < 0 else j for j in Qbase]
    else:
        Qbase = Q1[1]
        Qbase = [0 if j < 0 else j for j in Qbase]

    bfi = 0
    mean_for_period = 0

    if np.mean(Qin) == 0:
        bfi = 0
    else:
        for j in Qbase:
            mean_for_period += j / np.mean(Qin)
        bfi = mean_for_period / len(Qbase)

    return bfi, Qbase


"""
BFI calculations for 1000 alpha between 0.9 and 0.98

"""

import random


def BFI_calc_1000(Q, passes, reflect):
    """
    Calculation was made for 1000 random splitted alpha in
    range of 0.9 to 0.98

    we reflect the first reflect values and the last reflect values.
    this is to get rid of 'warm up' problems © Anthony Ladson
    """

    random.seed(1996)
    alpha_coefficients = [np.float64(random.uniform(0.9, 0.98)) for i in range(1000)]

    Q = np.array([np.float64(i) for i in Q], dtype=np.float64)
    Qin = Q

    "reflect our lists"

    if len(Q) - 1 > reflect:
        Q_reflect = np.array([np.float64(np.NaN) for _ in range(len(Q) + 2 * reflect)], dtype=np.float64)

        Q_reflect[:reflect] = Q[(reflect):0:-1]
        Q_reflect[(reflect):(reflect + len(Q))] = Q
        Q_reflect[(reflect + len(Q)):(len(Q) + 2 + 2 * reflect)] = Q[len(Q) - 2:len(Q) - reflect - 2:-1]

    else:
        Q_reflect = np.array([np.float64(np.NaN) for _ in range(len(Q))], dtype=np.float64)
        Q_reflect = Q

    bfi_record = []
    Qbase_record = []

    for i, alpha in enumerate(alpha_coefficients):

        Q1 = FirstPass(Q_reflect, alpha)

        "how many backwards/forward passes to we need © Anthony Ladson"

        n_pass = round(0.5 * (passes - 1))

        BackwardPass(Q1, alpha)

        for i in range(n_pass):
            Q1 = ForwardPass(BackwardPass(Q1, alpha), alpha)

        ################# end of passes  ##############################
        if len(Q) - 1 > reflect:
            Qbase = Q1[1][reflect:(len(Q1[1]) - reflect)]
            Qbase = [0 if j < 0 else j for j in Qbase]
        else:
            Qbase = Q1[1]
            Qbase = [0 if j < 0 else j for j in Qbase]

        Qbase_record.append(np.array(Qbase, dtype=np.float64))

        bfi = 0
        mean_for_period = 0

        if np.mean(Qin) == 0:
            bfi = 0
        else:
            for j in Qbase:
                mean_for_period += j / np.mean(Qin)
            bfi = mean_for_period / len(Qbase)

        bfi_record.append(np.float64(bfi))

    """
    After 1000 calculations function return
    mean value out of 1000

    And "mean" hygrograph of baseflow

    """

    # mean BFI out of 1000

    bfi_mean = 0
    for i in bfi_record:
        bfi_mean += i
    bfi_mean = bfi_mean / len(bfi_record)

    # mean hydrograph out of 1000 calculations

    Qbase_mean = [np.float64(0) for i in range(len(Qbase))]

    for Qbase_temp in Qbase_record:
        for i, value in enumerate(Qbase_temp):
            Qbase_mean[i] += value

    Qbase_mean = [np.float64(i / len(Qbase_record)) for i in Qbase_mean]

    return bfi_mean, Qbase_mean


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from test_values import Q_qilian

    Q_art = [1] * 365
    Q = Q_qilian
    bf = BFI_calc(Q, 0.95, 3, 2)
    df = pd.DataFrame({'Q': Q, 'Baseflow': bf[1]})
    df.plot()
    plt.show()
