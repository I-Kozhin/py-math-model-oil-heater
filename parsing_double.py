import json

# Два параметра
import numpy as np


def parsing_double(components, parameter):
    path = 'thermo_db.json'
    n = len(components)
    A = [0] * n
    with open(path, 'r') as f:
        data = json.loads(f.read())
        for i in range(n):
            A[i] = np.array(data[components[i]][parameter[0]][parameter[1]], dtype=float).tolist()

    return A
