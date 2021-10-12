

from random import randint, uniform
from ortools.linear_solver import pywraplp
from ortools.init import pywrapinit
import numpy as np
from time import time

def generate_tech_matrix(cant_variables, cant_disponibilidad, min_requerimientos = 0.0, max_requerimientos = 1.0, rand_type = 'float'):
    matrix = []
    for i in range(cant_variables):
        if rand_type == 'float':
            req = [ round(uniform(min_requerimientos, max_requerimientos), 2) for _ in range(cant_disponibilidad) ]
        else:
            req = [ randint(min_requerimientos, max_requerimientos) for _ in range(cant_disponibilidad) ]
            
        matrix.append(np.array(req))
    return np.array(matrix)

# este codigo utiliza es exactamente lo mismo que en las secciones anteriores
# solo que se ejecuta todo de una sola vez y recibe los parametros necesarios 
# mencionados en el video de mezcla

def mezcla(
    cant_variables = 5, # cantidad de variables de decision
    min_utilidad = 10000, # valor minimo de la utilidad
    max_utilidad = 20000, # valor maximo de la utilidad
    cant_disponibilidad = 5, # cantidad de elementos que restringen la disponibilidad. columnas en la matriz tecnológica.
    min_disponibilidad = 100, # valor minimo de la disponibilidad
    max_disponibilidad = 500, # valor maximo de la disponibilidad
    min_requerimientos = 0.0, # valor minimo que se considerará al crear la matriz tecnológica
    max_requerimientos = 1.0, # valor maximo que se considerará al crear la matriz tecnológica
    get_all_data = False, # si es falso, solamente retorna si es factible o no el problema, el valor optimo y los valores de las variables.
                            # si es verdadero, retorna el tiempo usado, la matriz de utilidad, la matriz de disponibilidad y la matriz tecnológica
    rand_type = 'float' # determina si los valores de la matriz tecnológica son ints o floats
):
    
    
    #gen data
    utilidades = np.array([randint(min_utilidad, max_utilidad) for _ in range(cant_variables)])
    disponibilidades = np.array([randint(min_disponibilidad, max_disponibilidad) for _ in range(cant_disponibilidad)])
    tech_matrix = generate_tech_matrix(cant_variables, cant_disponibilidad, rand_type = rand_type)
    
    #solve
    solver = pywraplp.Solver.CreateSolver('GLOP')
    inf = solver.infinity()
    x = {}
    for i in range(cant_variables):
        x[i] = solver.IntVar(0, inf, f'x{i}')
        
    for i in range(cant_disponibilidad):
        cons = solver.Sum(tech_matrix[j][i] * x[j] for j in range(cant_variables))
        solver.Add(cons <= disponibilidades[i] )
    z = solver.Sum(utilidades[i]*x[i] for i in range(cant_variables))
    solver.Maximize(z)
    
    t_init = time()
    status = solver.Solve()
    t_end = time()
    
    # check result
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['status'] = 'factible'
        result['value'] = solver.Objective().Value()
        result['variable_values()'] = [x[i].solution_value() for i in range(cant_variables)]
        if get_all_data:
            result['time'] = t_end - t_init
            result['utilidades'] = utilidades
            result['disponibilidades'] = disponibilidades
            result['tech_matrix'] = tech_matrix
    else:
        result['status'] = 'infactible'
    
    return result

print(mezcla(
    cant_variables = 10,
    min_utilidad = 100000,
    max_utilidad = 200000,
    cant_disponibilidad = 3,
    min_disponibilidad = 3,
    max_disponibilidad = 11,
    min_requerimientos = 0,
    max_requerimientos = 2,
    get_all_data = True,
    rand_type = 'float'
))