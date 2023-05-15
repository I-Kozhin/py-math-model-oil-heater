import numpy as np

from ant_eq import ant_eq
from Rachford_Rice import Rachford_Rice
from enthalpy import enthalpy
from liq_enthalpy import liq_enthalpy


def T_out(components, n, T_v, z, P_out, Pr_ch):
    p_sat = ant_eq(components, n, T_v)
    V_enth = enthalpy(components, n, T_v)
    L_enth = liq_enthalpy(components, n, T_v)
    w_out, x_out, y_out = Rachford_Rice(z, p_sat, P_out)
    V_enth = np.array(V_enth)
    y_out = np.array(y_out)
    L_enth = np.array(L_enth)
    x_out = np.array(x_out)
    r = w_out * sum(np.array(V_enth * y_out)) + (1 - w_out) * sum(np.array(L_enth * x_out)) - Pr_ch

    return r

