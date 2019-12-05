from ast import literal_eval as make_tuple

def process(L, cursor) :
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
        return "fini"
    elif n == 1 : 
        parameters = L[cursor+1: cursor+4]
        values = map_values(L,parameters, modes)
        L[parameters[2]] = values[0] + values[1]
        return process(L,cursor+4)
    elif n == 2 : 
        parameters = L[cursor+1: cursor+4]
        values = map_values(L,parameters, modes)
        L[parameters[2]] = values[0] * values[1]
        return process(L, cursor+4)
    elif n == 3 :
        user_input = int(input("Paramètre : "))
        L[L[cursor+1]] = user_input
        return process(L,cursor+2)
    elif n == 4 :
        print("output : ",L[L[cursor+1]], "with cursor", cursor)
        return process(L,cursor+2)
    elif n == 5 :
        parameters = L[cursor+1: cursor+3]
        values = map_values(L,parameters, modes)
        if values[0] != 0 :
            return process(L,values[1])
        else :
            return process(L,cursor+3)
    elif n == 6 :
        parameters = L[cursor+1: cursor+3]
        values = map_values(L,parameters, modes)
        if values[0] == 0 :
            return process(L,values[1])
        else :
            return process(L,cursor+3)
    elif n == 7 :
        parameters = L[cursor+1: cursor+3]
        values = map_values(L,parameters, modes)
        if values[0] < values[1] :
            L[L[cursor+3]] = 1
        else : 
            L[L[cursor+3]] = 0
        return process(L,cursor+4)
    elif n == 8 :
        parameters = L[cursor+1: cursor+3]
        values = map_values(L,parameters, modes)
        print("parameters= ",parameters)
        print("values =",values)
        if values[0] == values[1] :
            L[L[cursor+3]] = 1
        else : 
            L[L[cursor+3]] = 0
        return process(L,cursor+4)


    
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

def read_file(name) :
    input = open(name,"r").read()
    if "\n" in input :
        input = input.replace("\n","")
    return make_tuple(input)

print(process(list(read_file("input-day5")),0))