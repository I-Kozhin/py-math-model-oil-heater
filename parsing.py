import json


# когда у нас один параметр
def parsing(components, parameter):
    path = 'thermo_db.json'
    n = len(components)
    A = [0] * n
    with open(path, 'r') as f:
        data = json.loads(f.read())
        for i in range(n):
            A[i] = float(data[components[i]][parameter])
    return A
