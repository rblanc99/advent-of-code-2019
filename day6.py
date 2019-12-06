from typing import List

def read_file(input) :
    data = open(input,"r")
    res = data.readlines()
    res = list(map(lambda x: x[:-1].split(')'),res))
    data.close()
    return res

dictNodes = {}

class Node:
    def __init__(self, name: str, parent) :
        self.name = name
        self.parent = parent
        self.children = []
        self.value = 0
        dictNodes[name] = self

    def addChildren(self, child) :
        self.children.append(child)

    def setParent(self, parentNode) :
        self.parent = parentNode

noeudVide: Node = Node("vide", None)

def constructTree(L) :
    for x in L :
        parent, child = x
        if parent in dictNodes :
            parentNode = dictNodes[parent]
            if child in dictNodes :
                childNode = dictNodes[child]
                childNode.setParent(parentNode)
            else :
                childNode = Node(child,parentNode)
            parentNode.addChildren(childNode)
        else :
            parentNode = Node(parent, noeudVide)
            if child in dictNodes :
                childNode = dictNodes[child]
                childNode.setParent(parentNode)
            else :
                childNode = Node(child, parentNode)
            parentNode.addChildren(childNode)
    return dictNodes["COM"]

def depthFirstSearch(node: Node) :
#    print("on regarde le noeud", node.name)
    if node.children == [] :
#        print("il n'a pas d'enfants, sa value est ",node.value)
        return 
    for x in node.children :
#        print("ses enfants sont : ",list(map(lambda x:x.name,node.children)))
        x.value = node.value+1
        depthFirstSearch(x)
    return 

data = read_file("input-day6")
root = constructTree(data)
root.value = 0
depthFirstSearch(root)

total = 0
for x in dictNodes :
    total+=dictNodes[x].value
    #print(x,"enfants : ",dictNodes[x].children, "parent : ",dictNodes[x].parent)

print(total)

def path(a: Node, b: Node, root: Node) :
    current = a
    distanceToA = 1
    parentsOfA = {'a': 0}
    while root.name not in parentsOfA :
        parentsOfA[current.parent.name] = distanceToA
        current = current.parent
        distanceToA +=1
    current = b
    distanceToB = 1
    while 1 :
        if current.parent.name in parentsOfA :
            return parentsOfA[current.parent.name] + distanceToB - 2
        else : 
            distanceToB+=1
            current = current.parent

print(path(dictNodes["YOU"],dictNodes["SAN"],root))




