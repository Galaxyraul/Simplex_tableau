import numpy as np
import json

# Convertir ecuaciones minimo a máximo
def min_to_max(constraints,to_transform,coefficients):
    coefficients *= -1
    for index in to_transform:
        constraints[index]*=-1

# Eliminar igualdades
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
        text+=f"Problema {problem["id"]}:\n"
        objective = problem['objective']
        constraints = problem['constraints']
        operators = problem['operators']
        coefficients,base,values=build_tableau(objective,constraints,operators)
        base,values,result=core(coefficients,base,values)
        text+=get_result(base,values,result,objective)
        text+="\n"
    print(text)
    
def get_result(base,values,result,objective):
    text = f"Z={result[0]} "
    for i in range(len(base)):
        print(base[i])
        if base[i] < len(objective):
            text += f"x{base[i]}={values[i,0]} "
    return text   
def check_is_max(constraints,operators,objective):
    constraints = np.array(constraints,dtype="float")
    operators = np.array(operators,dtype="float") 
    objective = np.array(objective,dtype="float")
    equalities = np.where(operators==0)[0]
    to_transform = np.where(operators==-1)[0]
    operators = operators[operators != 0] 
    constraints = remove_equalities(equalities,constraints)
    if(to_transform.size > 0):
        min_to_max(constraints,to_transform,objective)
    return constraints,objective

def build_tableau(objective,constraints,operators):
    objective.insert(0,0)
    constraints,objective = check_is_max(constraints,operators,objective)
    coefficients = np.concatenate([objective,np.zeros(constraints.shape[0])])
    base = [i for i in range(len(objective),len(objective)+constraints.shape[0])]

    values = np.concatenate([constraints,np.identity(constraints.shape[0])*operators],axis=1)
    return[coefficients,base,values]
    
def core(coefficients,base,values):
    result = np.full(coefficients.shape,-1)
    while(True):
        C_b = np.array(coefficients[base])
        result = C_b@values - coefficients # Completamos la tabla
        if (result[1:] >= 0).all():
            break
        # Determinamos que elementos entra y sale de la base y realizamos el cambio
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

