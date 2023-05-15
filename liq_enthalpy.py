import numpy as np

from parsing import parsing
from parsing_double import parsing_double


def liq_enthalpy(components, n, T):
    parameter1 = ('normal_boiling_temperature')  # Температура кипения компонента
    T_boil = parsing(components, parameter1)  # Извечелечени из бд
    parameter2 = ['heat_capacity_liquid_1', 'heat_capacity']  # Изобарная теплоемкость по жидкости
    Heat_Cap = parsing_double(components, parameter2)  # Извлечение из бд
    parameter3 = ('condensation_heat_molar')
    Ph_trans = parsing(components, parameter3)  # Энегрия необходимая для совершения фазового перехода
    parameter4 = ['td_function_diapason_1', 'heat_capacity_vapor']  # Изобарная теплоемкость по газовой фазе
    HCV = parsing_double(components, parameter4)  # Извлечение изобарной теплоемкости по газу из бд
    parameter5 = ['td_function_diapason_1', 'enthalpy']
    Enth = parsing_double(components, parameter5)  # Извлечение энтальпии из бд

    Enth_comp = [0] * n
    E_comp = [0] * n
    Liq_ent = [0] * n

    for i in range(n):
        Enth1 = np.array((HCV[i])[0] + T_boil[i] * ((HCV[i])[1] / 2 + T_boil[i] * (
                    (HCV[i])[2] / 3 + T_boil[i] * ((HCV[i])[3] / 4 + T_boil[i] * (HCV[i])[4] / 5))) + Enth[i] / T_boil[
                             i])
        Enth2 = Enth1 * T_boil[i] * 8.31
        Enth_comp[i] = Enth2  # Выходной массив по газу
        # Расчет энергии, необходимой для конденсации газа
        E = (Heat_Cap[i])[0] * (T - T_boil[i])
        E_comp[i] = E
        # Расчет полной удельной энтальпии жидкой фазы
        Liq_ent1 = Enth_comp[i] + E_comp[i] - Ph_trans[i]
        Liq_ent[i] = float(Liq_ent1)

    return Liq_ent
