from collections import defaultdict
from ast import literal_eval as make_tuple
import numpy as np

np.set_printoptions(linewidth=100)
np.set_printoptions(edgeitems=50)

def read_file(name) :
    f = open(name,"r")
    data = f.read()
    if "\n" in data :
        data = data.replace("\n","")
    f.close()
    return list(make_tuple(data))

class IntcodeComputer() :

    def __init__(self, intcode, inputs=[]) :
        self.intcode = defaultdict(lambda: 0,{k:v for k,v in enumerate(intcode)})
        self.cursor = 0
        self.inputs = inputs
        self.stop = 0
        self.relativeBase = 0
        self.outputs = []

    def format_opcode(self,opcode) :
        digits = str(opcode)
        while len(digits) != 5 :
            digits = "0" + digits
        opcode = digits[3:]
        modes = digits[:3]
        opcode = int(opcode)
        return opcode, [int(k) for k in modes]

    def map_parameters(self, parameters, modes) :
        #print("indexes : ",parameters)
        #print("parameters : ",list(map(lambda x: self.intcode[x],parameters)))
        res = []
        for p in parameters :
            mode = modes.pop()
            if mode == 1 :
                res.append(p)
            elif mode == 2 :
                res.append(self.relativeBase + self.intcode[p])
            else :
                res.append(self.intcode[p])
        #print("res indexes : ",res)
        #print("values : ",list(map(lambda x: self.intcode[x],res)))
        return res

    def process_once(self) :
        opcode = self.intcode[self.cursor]
        n,modes = self.format_opcode(opcode)
        #print("\ncursor : ", self.cursor, ", n : ", n, ", relativeBase : ",self.relativeBase)
        if n == 99 :
            #print("code 99, over")
            self.stop = 1
        elif n == 1 :
            parameters = [self.cursor+1,self.cursor+2,self.cursor+3]
            values = self.map_parameters(parameters,modes)
            self.intcode[values[2]] = self.intcode[values[0]] + self.intcode[values[1]]
            self.cursor+=4  
        elif n ==2 :
            parameters = [self.cursor+1,self.cursor+2,self.cursor+3]
            values = self.map_parameters(parameters,modes)
            self.intcode[values[2]] = self.intcode[values[0]] * self.intcode[values[1]]
            self.cursor+=4
        elif n == 3 :
            if self.inputs == [] :
                self.inputs.append(0)
            userInput =  self.inputs.pop()
            parameter = [self.cursor+1]
            value = self.map_parameters(parameter,modes)
            self.intcode[value[0]] = userInput
            self.cursor+=2
        elif n == 4 :
            parameter = [self.cursor+1]
            value = self.map_parameters(parameter, modes)
            #print("output", self.intcode[value[0]], "with cursor ", self.cursor)
            self.outputs.append(self.intcode[value[0]])
            self.cursor+=2 
        elif n == 5 :
            parameters = [self.cursor+1,self.cursor+2]
            values = self.map_parameters(parameters, modes)
            if self.intcode[values[0]] != 0 :
                self.cursor = self.intcode[values[1]]
            else :
                self.cursor += 3
        elif n == 6 :
            parameters = [self.cursor+1,self.cursor+2]
            values = self.map_parameters(parameters, modes)
            if self.intcode[values[0]] == 0 :
                self.cursor = self.intcode[values[1]]
            else :
                self.cursor += 3
        elif n == 7 :
            parameters = [self.cursor+1,self.cursor+2,self.cursor+3]
            values = self.map_parameters(parameters, modes)
            if self.intcode[values[0]] < self.intcode[values[1]] :
                self.intcode[values[2]] = 1
            else : 
                self.intcode[values[2]] = 0
            self.cursor+=4      
        elif n == 8 :
            parameters = [self.cursor+1,self.cursor+2,self.cursor+3]
            values = self.map_parameters(parameters, modes)
            if self.intcode[values[0]] == self.intcode[values[1]] :
                self.intcode[values[2]] = 1
            else : 
                self.intcode[values[2]] = 0
            self.cursor+=4    
        elif n == 9 :
            parameter = [self.cursor+1]
            value = self.map_parameters(parameter, modes)    
            self.relativeBase += self.intcode[value[0]]
            self.cursor+=2
        return

    def process(self) :
        while not self.stop :        
            self.process_once()
        return self.outputs

    def process_till_number_of_outputs(self,number) :
        self.outputs = []
        while len(self.outputs) < number and not self.stop :
            self.process_once()
        if self.stop :
            return -1
        return self.outputs

class Game() :

    def __init__(self,intcode) :
        self.computer = IntcodeComputer(intcode)
        self.schema = np.zeros((26,45),int)
        self.score = -1

    def run_once(self) :
        output = self.computer.process_till_number_of_outputs(3)
        if output == -1 :
            return
        else :
            x,y,tileId = output
            if x == -1 and y == 0 :
                self.score = tileId
        #print(x,y,tileId)
        self.schema[y,x] = tileId
        
    def run_n_times(self, number) :
        for _ in range(number) :
            self.run_once()
        print(self.schema)
        print(np.sum(self.schema == 2))

    def run_till_stop(self) :
        while not self.computer.stop :
            self.run_once()
        print(self.schema)
        print(np.sum(self.schema == 2))

    def play(self) :
        self.computer.intcode[0] = 2

        while self.score == -1 : #construct the grid
            self.run_once()

        while not self.computer.stop :
            ball = np.argwhere(self.schema == 4)
            platform = np.argwhere(self.schema == 3)
            if len(ball)>0 and len(platform)>0 :
                xBall = ball[0,1]
                xPlatform = platform[0,1]
                if xBall == xPlatform :
                    self.computer.inputs.append(0)
                else :
                    joystick = int((ball[0,1] - platform[0,1])/abs(ball[0,1]-platform[0,1]))
                    self.computer.inputs.append(joystick)
            self.run_once()
        #print(self.schema)
        print(self.score)
        






L = read_file("input-day13")

# part1
game = Game(L)
game.run_till_stop()

# part 2
game = Game(L)
game.play()

