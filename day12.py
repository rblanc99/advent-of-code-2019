import re

def read_file(file) :
    f = open(file,'r')
    data = f.readlines()
    f.close()
    regex = re.compile("[xyz,><\n]")
    for i in range(len(data)) :
        data[i]= regex.sub("",data[i])
        data[i] = data[i].split("=")
        data[i].remove("")
        data[i] = list(map(lambda x: int(x),data[i]))
    return data

class Moon() :

    def __init__(self,coordinates) :
        x,y,z = coordinates
        self.position = (x,y,z)
        self.initialPosition = (x,y,z)
        self.velocity = (0,0,0)
        self.loop = 0

    def apply_gravity(self,moon) :
        x1,y1,z1 = self.position
        vx1,vy1,vz1 = self.velocity
        x2,y2,z2 = moon.position
        vx2,vy2,vz2 = moon.velocity
        if x1 > x2 :
            vx1-= 1
            vx2+= 1
        elif x1 < x2 :
            vx1+=1
            vx2-=1
        if y1 > y2 :
            vy1-= 1
            vy2+= 1
        elif y1 < y2 :
            vy1+=1
            vy2-=1
        if z1 > z2 :
            vz1-= 1
            vz2+= 1
        elif z1 < z2 :
            vz1+=1
            vz2-=1
        self.velocity = (vx1,vy1,vz1)
        moon.velocity = (vx2,vy2,vz2)
        return

    def apply_velocity(self) :
        x,y,z = self.position
        a,b,c = self.velocity
        self.position = (x+a,y+b,z+c)
        return

class Galaxy() :

    def __init__(self,coordinateSystem) :
        self.step = 0
        self.moons = []
        for coords in coordinateSystem :
            self.moons.append(Moon(coords))
        self.loopsFound = 0
        self.initialX = []
        self.initialY = []
        self.initialZ = []
        self.loops = (0,0,0)
        for moon in self.moons :
            x,y,z = moon.position
            self.initialX.append(x)
            self.initialY.append(y)
            self.initialZ.append(z)


    def apply_gravity(self) :
        for i in range(len(self.moons)) :
            for j in range(i+1,len(self.moons)) :
                self.moons[i].apply_gravity(self.moons[j])
        return 
    
    def apply_velocity(self) :
        for moon in self.moons :
            moon.apply_velocity()
        return

    def one_step(self) :
        self.step +=1
        self.apply_gravity()
        self.apply_velocity()
        self.check_for_loops()
        return

    def n_steps(self,n) :
        for _ in range(n) :
            self.one_step()
        #self.print_positions()
        print(self.calculate_energy())

    def print_positions(self) :
        for moon in self.moons :
            print(moon.position,moon.velocity)

    def calculate_energy(self) :
        energy = 0
        for moon in self.moons :
            pot = sum(list(map(lambda x: abs(x),moon.position)))
            kin = sum(list(map(lambda x: abs(x),moon.velocity)))
            energy += kin*pot
        return energy
        
    def check_for_loops(self) :
        positions = [0,1,2,3]
        positions = list(map(lambda x: self.moons[x].position,positions))
        vitesses = [0,1,2,3]
        vitesses = list(map(lambda x: self.moons[x].velocity,vitesses))
        x,y,z = [position[0] for position in positions],[position[1] for position in positions],[position[2] for position in positions]
        a,b,c = [vitesse[0] for vitesse in vitesses],[vitesse[1] for vitesse in vitesses],[vitesse[2] for vitesse in vitesses]
        if x == self.initialX and a == [0,0,0,0] and self.loops[0] == 0 :
            self.loopsFound +=1
            a,b,c = self.loops
            self.loops = (self.step,b,c)
            print("x loop : ",self.step)
        if y == self.initialY and b == [0,0,0,0] and self.loops[1] == 0:
            self.loopsFound +=1
            a,b,c = self.loops
            self.loops = (a,self.step,c)
            print("y loop : ",self.step)        
        if z == self.initialZ and c == [0,0,0,0] and self.loops[2] == 0:
            self.loopsFound +=1
            a,b,c = self.loops
            self.loops = (a,b,self.step)
            print("z loop : ",self.step)        
    
    def get_all_loops(self) :
        while self.loopsFound < 3 :
            self.one_step()
        return self.loops


def decomp(N) :
    res = []
    d = 2
    while N%d == 0 :
        res.append(d)
        N = N//d
    d = 3
    while d <= N :
        while N%d == 0 :
            res.append(d)
            N = N//d
        d+=2
    return res

import numpy as np

def gcm(L) :
    commonFactors = set([])
    factorsList = []
    for N in L :
        factors = np.array(decomp(N))
        factorsList.append(factors)
        commonFactors.update(np.unique(factors))
    res = 1
    for factor in commonFactors :
        max = 0
        for factors in factorsList :
            power = np.count_nonzero(factors == factor)
            if power > max :
                max = power
        res*=factor**max
    return res


# part one
galaxy = Galaxy(read_file('input-day12'))
print("total energy after 1000 steps :")
galaxy.n_steps(1000)

#part two
galaxy = Galaxy(read_file('input-day12'))
print("number os steps to match a previous state :\n",gcm(galaxy.get_all_loops()))