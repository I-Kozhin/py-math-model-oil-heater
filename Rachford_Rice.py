from numpy import *
import numpy as np
from scipy import optimize


def Rachford_Rice(z, psat, P):
    P = np.array(P)
    psat = np.array(psat)
    K = np.array(psat / P)  # постоянная равновесия
    n = len(z)
    if (sum(np.array(z * K)) > 1) and (sum(np.array(z / K)) > 1):  # двухфазная область
        def w1(w2):
            result = np.array(sum(z * (K - 1) / (1 + (K - 1) * w2)))
            return float(result)

        w = float(optimize.fsolve(w1, 0.5))  # Уравнение Речфорда-Райса
        x = np.array(
            z / (1 + (K - 1) * w))  # Мольная доля компонентов в жидкости
        y = np.array(K * x).tolist()  # Мольная доля компонентов в газе
    elif sum(np.array(z * K)) <= 1:
        w = 0
        x = z
        y = [0] * n
    elif sum(np.array(z / K)) <= 1:
        w = 1
        y = z
        x = [0] * n
    return w, x, y
