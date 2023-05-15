import numpy as np
import scipy.optimize
from ant_eq import ant_eq
from enthalpy import enthalpy
from liq_enthalpy import liq_enthalpy
from molar_mass import molar_mass
from Rachford_Rice import Rachford_Rice


def main_heater(T):
    # [К] Начальная температура поступающей смеси
    T = T + 273.15
    # [Па] Давление перед нагревателем
    P_in = 1.399e6
    # [Па] Давление после нагревателем
    P_out = 1.349e6
    # Компонентный состав смеси
    components = ['CH4', 'C2H6', 'C3H8', 'n_C4H10', 'n_C5H12']
    n = len(components)
    # Доли компонентов в смеси
    z = [0.08, 0.08, 0.20, 0.31, 0.33]
    # [Вт] Тепловая мощность нагревателя
    Qt = 22410
    # [кг/ч] Расход смеси через нагреватель
    Qm = 271.7
    iterations = 1
    T_exg = [0] * iterations
    w_ing = [0] * iterations
    w_outg = [0] * iterations

    # Расчет
    for i in range(iterations):
        # [Па] Давление насыщенных паров смеси
        p_sat = ant_eq(components, n, T)
        # Расчет мольной доли отгона, долей компонентов в жидкой и паровой фазе
        w_in, x_in, y_in = Rachford_Rice(z, p_sat, P_in)
        # [Дж/кгмоль] Расчет полной удельной энтальпии паровой фазы
        V_enth = enthalpy(components, n, T)
        # [Дж/кгмоль] Расчет полной удельной энтальпии жидкой фазы
        L_enth = liq_enthalpy(components, n, T)

        V_enth = np.array(V_enth)
        y_in = np.array(y_in)
        L_enth = np.array(L_enth)
        x_in = np.array(x_in)

        # [Дж/кгмоль] Расчет полной удельной энтальпии смеси
        F_enth = w_in * sum(np.array(y_in * V_enth)) + (1 - w_in) * sum(np.array(x_in * L_enth))
        # [кг/моль] Расчет молярной массы смеси
        mix_mm = molar_mass(components, n, z)
        # [Дж/кгмоль] Расчет кол-ва энергии, используемого на подогрев/охлаждение смеси
        E = ((mix_mm * Qt) / Qm) * 3600
        # [Дж/кгмоль] Расчет правой части уравнения теплового баланса
        Pr_ch = F_enth + E

        # Расчет нелинейной системы уравнений, для определения температуры выходящего потока
        def Nagr_eq(T_v):
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

        # [К] Температура выходящего потока
        T_ex = scipy.optimize.fsolve(Nagr_eq, 500)
        T_C = T_ex - 273.15  # Перевод в градусы цельсия (при необходимости)

        def Nagr_eq_T_ex(T_v):
            p_sat = ant_eq(components, n, T_v)
            w_out, x_out, y_out = Rachford_Rice(z, p_sat, P_out)

            return w_out

        # Данные для графиков (при необходимости)
        T_exg[i] = float(T_C)
        w_ing[i] = w_in
        w_outg[i] = Nagr_eq_T_ex(T_ex)
    print(T_exg)  # температура выходного потока (С)
    print(w_ing)  # газовая фаза на входе (% масс)
    print(w_outg)  # газовая фаза на выходе (% масс)


def main():
    for i in range(-50, 105, 5):
        print('При температуре на входе', i)
        main_heater(i)


if __name__ == '__main__':
    main()
