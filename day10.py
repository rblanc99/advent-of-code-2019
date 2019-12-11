import numpy as np

def read_file(name) :
    f = open(name, 'r')
    data = f.readlines()
    f.close()
    return np.array(list(map(mapAsteroids,data)))
def mapAsteroids(line) :
    arr = [k for k in line]
    if '\n' in arr :
        arr.remove('\n')
    return list(map(lambda x: 1 if x=='#' else (2 if x=="X" else 0),arr))

def see(pointA, pointB, M) :
    if (not M[pointA]) or (not M[pointB]) :
        return False
    x1,y1 = pointA
    x2,y2 = pointB
    if y1 == y2 :
        for x in range(min(x1,x2)+1,max(x2,x1)):
            if M[x,y1] :
                return False
        return True
    if x1 == x2 :
        for y in range(min(y1,y2)+1,max(y2,y1)):
            if M[x1,y] :
                return False
        return True
    slope = (y2-y1)/(x2-x1)
    for x in range(x1+1,x2):
        #print("point regardé : ",x,y1+slope*(x-x1))
        if y1+slope*(x-x1) == int(y1+slope*(x-x1)) and M[x,y1+int(slope*(x-x1))]:
            return False
    return True

def fillCountMatrix(M) :
    n,m = M.shape
    countMatrix = np.zeros((n*m,n*m),int)
    listOfIndexes = list(np.ndindex((n,m)))
    for i in range(n*m):
        for j in range(i+1,n*m) :
            if see(listOfIndexes[i],listOfIndexes[j],M) :
                countMatrix[i,j] = 1
                countMatrix[j,i] = 1
    print("countMatrix of size",countMatrix.shape)
    return countMatrix, listOfIndexes

def getMax(countMatrix, listOfIndexes) :
    finalMatrix = list(map(lambda x: np.sum(x),countMatrix))
    print("rowMatrix of size",np.array(finalMatrix).shape)
    return np.max(finalMatrix), listOfIndexes[np.where(finalMatrix == np.max(finalMatrix))[0][0]]

def detect_once(M) :
    n,m = M.shape
    point = np.where(M==2)
    #print(point)
    point = tuple(map(lambda x: x[0],point))
    res = np.zeros((n,m),int)
    count = 0
    listOfIndexes = list(np.ndindex((n,m)))
    pointIndex = listOfIndexes.index(point)
    for i in range(pointIndex) :
        if see(listOfIndexes[i],point,M) :
            res[listOfIndexes[i]] = 1
            count+=1
    for i in range(pointIndex+1,n*m) :
        if see(point,listOfIndexes[i],M):
            res[listOfIndexes[i]] = 1
            count+=1
    return res, count, point

def vaporize(M) :
    totalAsteroidsDestroyed = 1
    while totalAsteroidsDestroyed <200 :
        res, count, turret = detect_once(M)
        #turnClockwise(res,totalAsteroidsDestroyed,turret)
        totalAsteroidsDestroyed+=count
    turnClockwise(res, totalAsteroidsDestroyed-count, turret)
    return

def setTurret(M,turret) :
    x,y = turret
    M[x,y] = 2  

def turnClockwise(M,nb,turret) :
    x1,y1 = turret
    nbAsteroidsDestroyed = nb
    '''
    for x in range(0,x1) :
        if M[x,y1] :
            print("first asteroid destroyed : ",x,y1)
            nbAsteroidsDestroyed += 1
            M[x,y1] = 0
    for x in range(x1+1,n) :
        if M[x,y1] :
            print("another asteroid destroyed : ",x,y1)
            nbAsteroidsDestroyed += 1
            M[x,y1] = 0    
    '''
    firstQuarter, secondQuarter, thirdQuarter, fourthQuarter = [],[],[],[]
    firstDict, secondDict, thirdDict, fourthDict = {},{},{},{}
    rows, columns = np.nonzero(M)
    nonZeroPoints = list(map(lambda x,y: (x,y),rows,columns))
    
    for point in nonZeroPoints :
        slope = (point[1]-y1)/(point[0]-x1)
        if point[1] >= y1 and point[0]<x1:
            #print("first quarter : ",point)
            firstQuarter.append(slope)
            firstDict[slope] = point
        elif point[1] > y1 and point[0]>=x1:
            #print("second quarter : ",point)
            secondQuarter.append(slope)
            secondDict[slope] = point
        elif point[1] <= y1 and point[0]>=x1:
            #print("third quarter : ",point)
            thirdQuarter.append(slope)
            thirdDict[slope] = point
        else :
            #print("fourth quarter : ",point)
            fourthQuarter.append(slope)
            fourthDict[slope] = point
    firstQuarter.sort()
    secondQuarter.sort()
    thirdQuarter.sort()
    fourthQuarter.sort()
    #print(firstQuarter,secondQuarter,thirdQuarter,fourthQuarter)
    for slope in firstQuarter[::-1] :
        point = firstDict[slope]
        print(nbAsteroidsDestroyed, "e asteroid destroyed : ",point)
        nbAsteroidsDestroyed+=1
    for slope in secondQuarter[::-1] :
        point = secondDict[slope]
        print(nbAsteroidsDestroyed, "e asteroid destroyed : ",point)
        nbAsteroidsDestroyed+=1
    for slope in thirdQuarter[::-1] :
        point = thirdDict[slope]
        print(nbAsteroidsDestroyed, "e asteroid destroyed : ",point)
        nbAsteroidsDestroyed+=1
    for slope in fourthQuarter[::-1] :
        point = fourthDict[slope]
        print(nbAsteroidsDestroyed, "e asteroid destroyed : ",point)
        nbAsteroidsDestroyed+=1
    return
    

    

#example = np.array([[0,1,0,0,1],[0,0,0,0,0],[1,1,1,1,1],[0,0,0,0,1],[0,0,0,1,1]])
#print(example)

#print(see((0,1),(4,3),example))
#f = fillCountMatrix(example)
#rint(f)
#s = sumRows(f)
#print(s)

M = read_file("input-day10")
C,I = fillCountMatrix(M)
maxAsteroids,turret = getMax(C,I)
print("nombre max d'asteroides : ", maxAsteroids, "at position", turret)
setTurret(M,turret)
vaporize(M)
#res,count,point = detect_once(M)
#print(res)
#print(turnClockwise(res,0,(3,8)))
#print(M)
#print("Matrix of size",M.shape)
#print(see((1,5),(9,1),M))


#print(detect_once(M))


