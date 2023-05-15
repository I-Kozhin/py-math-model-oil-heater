#  Молярная масса смеси
import numpy as np
from parsing import parsing


def molar_mass(components, n, z):
    parameter1 = ('molar_mass') # Выбор необходимых параметров
    mol_mass = parsing(components, parameter1)
    mol_mass = np.array(mol_mass)
    z = np.array(z)
    mix_mm = sum(np.array(z * mol_mass))  # [кг/моль] Молярная масса смеси
    return mix_mm

