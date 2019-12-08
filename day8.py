import numpy as np
import time

np.set_printoptions(edgeitems=100)

def read_file(name) :
    f = open(name, 'r')
    data = f.read()
    f.close()
    return data

def format(data) :
    rows = np.empty((0,25),int)
    for i in range(int(len(data)/25)) :
        rows = np.append(rows,[[int(k) for k in data[25*i:25*i+25]]],axis=0)
    layers = np.empty((0,6,25),int)
    for i in range(int(len(rows)/6)) :
        layer = np.empty((0,25),int)
        for j in range(6) :
            layer = np.append(layer,[rows[6*i+j]],axis=0)
        layers = np.append(layers,[layer],axis=0)
    return layers

# row shape : (1,25)
# rows shape : (600,25) where 600 is the number of rows in the data
# layer shape : (6,25)
# layers shape : (100,6,25) where 100 is the number of layers in the data

def searchLayerWithFewer0(layers) :
    minDigits = 1000
    layerWithMinDigits = None
    for layer in layers :
        count = np.count_nonzero(layer == 0)
        if count < minDigits :
            minDigits = count
            layerWithMinDigits = layer
    return layerWithMinDigits

def countDigits(digit,layer) :
    return np.count_nonzero(layer == digit)


input_day8 = read_file("input-day8")
image = format(input_day8)


minLayer = searchLayerWithFewer0(image)
print(countDigits(1,minLayer)*countDigits(2,minLayer))

def decode(image) :
    _,nbRows,nbColumns = image.shape
    result = np.empty((nbRows,nbColumns),int)
    for i in range(nbRows) :
        for j in range(nbColumns) :
            layer = 0
            while image[layer,i,j] == 2 :
                layer+=1
            result[i,j] = image[layer,i,j]
    return result

decoded = decode(image)
print(decoded)