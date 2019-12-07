from itertools import permutations
from ast import literal_eval as make_tuple

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
        print("99 !!!!!!!!")
        return -1
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
        print("output : ",L[L[cursor+1]], "with cursor", cursor)
        #process(L,cursor+2, inputs)
        return L[L[cursor+1]]
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

def amplify(phases, inputCode, startCode) :
    print("testing phase : ",phases)
    current_code = startCode
    for i in range(5) :
        print("processing for phase ",phases[i]," and input ",current_code," and list ",inputCode)
        current_code = process(inputCode[:],0, [phases[i],current_code])
    return current_code

def amplify2(phases, inputCode, startCode) :
    print(inputCode == L2)
    current_code = amplify(phases,inputCode[:], startCode)
    if current_code == -1 :
        return startCode
    return amplify2(phases, inputCode,current_code)
    

def search_max(input) :
    allPermutationsOf5 = permutations([0,1,2,3,4])
    max = 0
    for phase in allPermutationsOf5 :
        amplification = amplify(phase, input, 0)
        if amplification > max :
            max = amplification
    return max

def search_max2(input) :
    allPermutationsOf9 = permutations([5,6,7,8,9])
    max = 0
    for phase in allPermutationsOf9 :
        amplification = amplify2(phase, input, 0)
        if amplification > max :
            max = amplification
    return max


def read_file(name) :
    f = open(name,"r")
    data = f.read()
    if "\n" in data :
        data = data.replace("\n","")
    f.close()
    return list(make_tuple(data))


#print(search_max(read_file("input-day7")))
L = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]

L2 = L[:]

round1Code = amplify([5,6,7,8,9],L,0)

print(amplify([5,6,7,8,9],L[:],round1Code))

print(L == L2)

