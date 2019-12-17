import re
from collections import defaultdict
import numpy as np
from math import ceil

def read_file(name) :
    f = open(name,'r')
    data = f.readlines()
    f.close()
    regex = re.compile('[,=>\n]')
    for i in range(len(data)) :
        data[i] = regex.sub("",data[i])
        data[i] = data[i].split(" ")
        data[i].remove("")
        data[i] = [(int(data[i][n]),data[i][n+1]) for n in range(0, len(data[i]), 2)]
    return data

def create_dict(L) :
    chemistryDict = {}
    for recipe in L :
        resQuantity, resId = recipe.pop()
        chemistryDict[resId] = (resQuantity,recipe)
    return chemistryDict

class Chemistry() :
    def __init__(self,D) :
        self.recipes = D
        self.pile = defaultdict(lambda: 0,{})
        self.availableResources = defaultdict(lambda: 0,{})
        self.ore = 0

    def getFuel(self,n):
        self.pile["FUEL"] = n

    def cook1Ingredient(self) :
        pileValues = np.array(list(self.pile.values()))
        print(self.pile,"\n")
        print(pileValues)
        print(np.sum(pileValues==0))
        if all(pileValues==0) :
            return 0
        pileIngredients = list(self.pile.keys())
        firstIngredient = pileIngredients.pop()
        necessaryNumber = self.pile[firstIngredient]
        while necessaryNumber == 0 :
            firstIngredient = pileIngredients.pop()
            necessaryNumber = self.pile[firstIngredient]
        numberObtained, ingredients = self.recipes[firstIngredient]
        numberCooked = 0
        necessaryNumber-=self.availableResources[firstIngredient]
        print("selected ingredient : ",firstIngredient)
        print("necessary number : ",necessaryNumber)
        print(numberObtained,"with recipe : ",ingredients)
        while numberCooked < necessaryNumber :
            for n,ing in ingredients :
                if ing == "ORE" :
                    self.ore += n
                else :
                    self.pile[ing] += n
            numberCooked += numberObtained
        self.availableResources[firstIngredient] = numberCooked - necessaryNumber
        self.pile[firstIngredient] = 0
        return 1

    def cook1Ingredient2(self) :
        pileValues = np.array(list(self.pile.values()))
        """print("\n",self.pile,"\n")
        print(pileValues)
        print(np.sum(pileValues==0))"""
        if all(pileValues==0) :
            return 0
        pileIngredients = list(self.pile.keys())
        firstIngredient = pileIngredients.pop()
        necessaryNumber = self.pile[firstIngredient]
        while necessaryNumber == 0 :
            firstIngredient = pileIngredients.pop()
            necessaryNumber = self.pile[firstIngredient]
        numberObtained, ingredients = self.recipes[firstIngredient]
        necessaryNumber-=self.availableResources[firstIngredient]
        """print("selected ingredient : ",firstIngredient)
        print("necessary number : ",necessaryNumber)
        print(numberObtained,"with recipe : ",ingredients) """
        ratio = ceil(necessaryNumber/numberObtained)
        for n,ing in ingredients :
            if ing == "ORE" :
                self.ore += ratio*n
            else :
                self.pile[ing] += ratio*n
        numberCooked = numberObtained*ratio
        self.availableResources[firstIngredient] = numberCooked - necessaryNumber
        self.pile[firstIngredient] = 0
        return 1

    def cookFor(self,number) :
        self.getFuel(number)
        while self.cook1Ingredient2() :
            pass
        return self.ore

    def cookForOneTrillion(self) :
        fuels = 0
        while self.ore < 1e12 :
            self.cookFor(1)
            fuels+=1
            if fuels/100 == fuels//100 :
                print(fuels)
        return fuels

    def cookForOneTrillion2(self) :
        fuels = 0
        while self.ore < 1e12 :
            self.pile["FUEL"] = 1e4
            self.cookFor(1)
            fuels+=1e4
            print(fuels)
        return fuels


L = read_file("input-day14")
D = create_dict(L)

C = Chemistry(D)
print(Chemistry(D).cookFor(1))

def dichotomic_search() :
        a = 1
        b = 1e9
        while b-a > 1 :
            middle = int(a + (b-a)//2)
            v = Chemistry(D).cookFor(middle)
            if v > 1e12 :
                b = middle - 1
            elif v < 1e12 :
                a = middle + 1
            else :
                return middle
        return middle

print(dichotomic_search())