import numpy as np
import json

# Convertir ecuaciones minimizeimo a máximo
def minimize_to_max(constraints,to_transform,coefficients):
    for index in to_transform:
        constraints[index]*=-1

# Eliminimizear igualdades
def remove_equalities(equalities,constraints):
    for index in equalities:
        pivot = np.argmin(constraints[index,1:]) + 1
        constraints[index] /= constraints[index,pivot]
        constraints[index,pivot] = 0
        for row in range(constraints.shape[0]):
            if row not in equalities:
                constraints[row] += constraints[index]*constraints[row,pivot]
    constraints = np.delete(constraints,equalities,axis=0)
    return constraints

def read_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
    problems = data['problems']
    text = ""
    for problem in problems:
        text+=f"Problema {problem["id"]}:"
        objective = problem['objective']
        constraints = problem['constraints']
        operators = problem['operators']
        minimize=problem['minimize']
        coefficients,base,values=build_tableau(objective,constraints,operators,minimize)
        base,values,result=core(coefficients,base,values)
        text+=get_result(base,values,result,objective)
        text+="\n"
    return text
    
def get_result(base,values,result,objective):
    text = f"Z={result[0]} "
    for i in range(len(base)):
        if base[i] < len(objective):
            text += f"x{base[i]}={values[i,0]} "
    for i in range(1, len(objective)):
        if i not in base:
            text += f"x{i} = 0 "
    return text   

def remove_greater(constraints,greaters):
    for index in greaters:
        constraints[index]*=-1
        
def check_is_max(constraints,operators,objective,minimize):
    constraints = np.array(constraints,dtype="float")
    operators = np.array(operators,dtype="float") 
    objective = np.array(objective,dtype="float")
    equalities = np.where(operators==0)[0]
    to_transform = np.where(operators==-1)[0]
    operators = operators[operators != 0] 
    remove_greater(constraints,to_transform)
    constraints = remove_equalities(equalities,constraints)
    if(minimize):
        objective *= -1
    return constraints,objective

def build_tableau(objective,constraints,operators,minimize):
    objective.insert(0,0)
    constraints,objective = check_is_max(constraints,operators,objective,minimize)
    coefficients = np.concatenate([objective,np.zeros(constraints.shape[0])])
    base = [i for i in range(len(objective),len(objective)+constraints.shape[0])]

    values = np.concatenate([constraints,np.identity(constraints.shape[0])],axis=1)
    return[coefficients,base,values]
    
def core(coefficients,base,values):
    result = np.full(coefficients.shape,-1)
    while(True):
        C_b = np.array(coefficients[base])
        result = C_b@values - coefficients # Completamos la tabla
        if (result[1:] >= 0).all():
            break
        # Determinimizeamos que elementos entra y sale de la base y realizamos el cambio
        goes_in = 1 + np.argmin(result[1:])
        goes_out = np.argmin(np.where(values[:,goes_in] <= 0, np.inf, values[:,0]*1/values[:,goes_in]))
        base[goes_out] = goes_in

        # Seleccionamos el pivote, normalizamos la fila y hacemos combinación lineal para evitar que haya multiples variables de la base en una misma ecuación
        pivot = goes_out
        values[pivot]/=values[pivot,goes_in]
        for row in range(values.shape[0]):
            if row != pivot:
                values[row] -= values[pivot]*values[row,goes_in]
    return base,values,result

def main(objective,constraints,operators):
    constraints = check_is_max(constraints,operators)
    coefficients,base,values=build_tableau(constraints,objective)
    core(coefficients,base,values)

