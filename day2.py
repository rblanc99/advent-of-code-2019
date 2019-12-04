from ast import literal_eval as make_tuple
from copy import deepcopy

def compute(tuple, noun, verb) :
    L = preprocess(list(tuple), noun, verb)
    cursor = 0
    return process(L,cursor)

def process(L, cursor) :
    n = L[cursor]
    if n == 99 :
        return L
    elif n == 1 : 
        indexes = L[cursor+1: cursor+4]
        L[indexes[2]] = L[indexes[0]] + L[indexes[1]]
        return process(L,cursor+4)
    elif n == 2 : 
        indexes = L[cursor+1: cursor+4]
        L[indexes[2]] = L[indexes[0]] * L[indexes[1]]
        return process(L, cursor+4)


def read_file(name) :
    input = open(name,"r").read()
    if input[0] != "(" :
        input = "("+input
    if input[-1] != ")":
        input+=")"
    if "\n" in input :
        input = input.replace("\n","")
    return make_tuple(input)
    

def preprocess(L, noun, verb) : 
    L[1] = noun
    L[2] = verb
    return L

def search_params(L) :
    for noun in range(100) :
        for verb in range(100):
            tested_list = deepcopy(L)
            if compute(tested_list,noun,verb)[0] == 19690720 :
                return (noun, verb)
    return "rien trouvé..."

print(search_params((1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,1,6,19,23,1,13,23,27,1,6,27,31,1,31,10,35,1,35,6,39,1,39,13,43,2,10,43,47,1,47,6,51,2,6,51,55,1,5,55,59,2,13,59,63,2,63,9,67,1,5,67,71,2,13,71,75,1,75,5,79,1,10,79,83,2,6,83,87,2,13,87,91,1,9,91,95,1,9,95,99,2,99,9,103,1,5,103,107,2,9,107,111,1,5,111,115,1,115,2,119,1,9,119,0,99,2,0,14,0
)))