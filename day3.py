import numpy as np
from operator import add

def tracer_chemin(path) :
    position = (0,0)
    L = []
    L.append(position)
    for direction in path :
        x,y = position
        if direction[0] == "R" :
            for i in range(1,int(direction[1:])+1):
                L.append((x+i,y))
            x+= int(direction[1:])
        if direction[0] == "L" :
            for i in range(1,int(direction[1:])+1):
                L.append((x-i,y))
            x-= int(direction[1:])
        if direction[0] == "U" :
            for i in range(1,int(direction[1:])+1):
                L.append((x,y+i))
            y+= int(direction[1:])
        if direction[0] == "D" :
            for i in range(1,int(direction[1:])+1):
                L.append((x,y-i))
            y-= int(direction[1:])
        position = x,y
    return L

def Intersection(path1, path2): 
    lst1 = tracer_chemin(path1)
    lst2 = tracer_chemin(path2)
    inter = list(set(lst1).intersection(lst2))
    indexesInPath1 = list(map(lambda x: lst1.index(x),inter))
    indexesInPath2 = list(map(lambda x: lst2.index(x),inter))
    return inter,indexesInPath1, indexesInPath2


def read_file(path) :
    input = open(path,"r").read()
    input = input.split("\n")
    path1 = input[0].split(',')
    path2 = input[1].split(',')
    return path1,path2

def distance_min(path1,path2) :
    intersections,_,_ = Intersection(path1,path2)
    distances = list(map((lambda position: abs(position[0])+abs(position[1])), intersections))
    distances.remove(0)
    return min(distances)

def shortestNumberOfSteps(path1,path2) :
    _,steps1,steps2 = Intersection(path1,path2)
    steps1.remove(0)
    steps2.remove(0)
    return min(list(map(add,steps1,steps2)))

path1,path2 = read_file("input")

a= "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(',')
b= "U62,R66,U55,R34,D71,R55,D58,R83".split(',')


print(distance_min(path1,path2))

print(shortestNumberOfSteps(path1,path2))