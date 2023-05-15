import numpy as np

from parsing_double import parsing_double


def enthalpy(components, n, T):
    parameter1 = ['td_function_diapason_1', 'heat_capacity_vapor']  # Выбор необходимых параметров
    HCV = parsing_double(components, parameter1)  # Извлечение изобарной теплоемкости из бд
    parameter2 = ['td_function_diapason_1', 'enthalpy']
    Enth = parsing_double(components, parameter2)  # Извлечение энтальпии из бд
    Enth_comp = [0] * n
    for i in range(n):  # Расчет полной энтальпии по компонентам
        Enth1 = ((HCV[i])[0] + T * (np.array((HCV[i])[1] / 2) + T * (np.array((HCV[i])[2] / 3) + T * ((HCV[i])[3] / 4 + T * (HCV[i])[4]) / 5)) + Enth[i] / T)
        Enth2 = float(Enth1) * T * 8.31
        Enth_comp[i] = float(Enth2)  # Выходной массив

    return Enth_comp
