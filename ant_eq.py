from parsing import parsing


# Давление насыщеных паров
def ant_eq(components, n, T):
    parameter = ('antoine_A')
    an_A = parsing(components, parameter)
    parameter = ('antoine_B')
    an_B = parsing(components, parameter)
    parameter = ('antoine_C')
    an_C = parsing(components, parameter)
    p_sat = [0] * n
    for i in range(n):
        psat = 2.71 ** (an_A[i] - (an_B[i] / (T + an_C[i])))
        psat1 = (psat * 1e5) / 750.61
        p_sat[i] = float(psat1)
    return p_sat
