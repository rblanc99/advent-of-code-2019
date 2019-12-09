from itertools import permutations
from ast import literal_eval as make_tuple

def read_file(name) :
    f = open(name,"r")
    data = f.read()
    if "\n" in data :
        data = data.replace("\n","")
    f.close()
    return list(make_tuple(data))

def process(L, cursor, inputs) :
    n = L[cursor]
    digits = [int(k) for k in str(n)]
    while len(digits) != 5 :
        digits = [0] + digits
    opcode = digits[-2:]
    modes = digits[:-2]
    temp = ""
    for k in opcode :
        temp+=str(k)
    n = int(temp)
    #print("\n")
    #print("cursor= ",cursor)
    #print("n= ",n)
    #print("L= ",L)
    if n == 99 :
        #print("99 !!!!!!!!")
        return -1, cursor, L
    elif n == 1 : 
        parameters = L[cursor+1: cursor+4]
        values = map_values(L,parameters, modes)
        L[parameters[2]] = values[0] + values[1]
        return process(L,cursor+4,inputs)
    elif n == 2 : 
        parameters = L[cursor+1: cursor+4]
        values = map_values(L,parameters, modes)
        L[parameters[2]] = values[0] * values[1]
        return process(L, cursor+4, inputs)
    elif n == 3 :
        #print("inputs = ",inputs)
        user_input = inputs[0]
        L[L[cursor+1]] = user_input
        return process(L,cursor+2, inputs[1:])
    elif n == 4 :
        #print("output : ",L[L[cursor+1]], "with cursor", cursor)
        #process(L,cursor+2, inputs)
        cursor+=2
        return L[L[cursor-1]],cursor, L
    elif n == 5 :
        parameters = L[cursor+1: cursor+3]
        values = map_values(L,parameters, modes)
        if values[0] != 0 :
            return process(L,values[1], inputs)
        else :
            return process(L,cursor+3, inputs)
    elif n == 6 :
        parameters = L[cursor+1: cursor+3]
        values = map_values(L,parameters, modes)
        if values[0] == 0 :
            return process(L,values[1],inputs)
        else :
            return process(L,cursor+3,inputs)
    elif n == 7 :
        parameters = L[cursor+1: cursor+3]
        values = map_values(L,parameters, modes)
        if values[0] < values[1] :
            L[L[cursor+3]] = 1
        else : 
            L[L[cursor+3]] = 0
        return process(L,cursor+4,inputs)
    elif n == 8 :
        parameters = L[cursor+1: cursor+3]
        values = map_values(L,parameters, modes)
        #print("parameters= ",parameters)
        #print("values =",values)
        if values[0] == values[1] :
            L[L[cursor+3]] = 1
        else : 
            L[L[cursor+3]] = 0
        return process(L,cursor+4,inputs)

    
def map_values(L, parameters, modes) :
    res = [None for k in range(len(parameters))]
    modes = modes[::-1]
    for i in range(len(parameters)) :
        try:
            mode = modes[i]
        except IndexError :
            res[i] = L[parameters[i]]
        else:
            if mode :
                res[i] = parameters[i]
            else :
                res[i] = L[parameters[i]]
    return res


class Machine() :

    def __init__(self,program, cursor, phase) :
        self.program = program[:]
        self.cursor = cursor
        self.phase = phase
    
    def process_once(self, inputs) :
        output,cursor,program = process(self.program,self.cursor,inputs)
        self.cursor = cursor
        self.program = program
        return output

class Cluster() :

    def __init__(self,program, phases) :
        self.machines = [Machine(program,0, phases[k]) for k in range(5)]
        self.phases = phases
        self.output = 0

    def run_once(self) :
        for i in range(len(self.machines)) :
            self.output = self.machines[i].process_once([self.phases[i],self.output])
        return self.output

    def run(self) :
        self.run_once()
        while self.output != -1 :
            result = self.output
            for i in range(len(self.machines)) :
                self.output = self.machines[i].process_once([self.output])
        return result

            

def search_max(input) :
    allPermutationsOf5 = permutations([0,1,2,3,4])
    max = 0
    for phase in allPermutationsOf5 :
        output = Cluster(input,phase).run_once()
        if output > max :
            max = output
    return max

def search_max2(input) :
    allPermutationsOf9 = permutations([5,6,7,8,9])
    max = 0
    for phase in allPermutationsOf9 :
        output = Cluster(input,phase).run()
        if output > max :
            max = output
    return max

print(search_max(read_file("input-day7")))

print(search_max2(read_file("input-day7")))


