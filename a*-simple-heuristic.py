from copy import deepcopy
FINAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, None]
START_STATE = [None, 7, 8, 6, 5, 4, 2, 3, 1]

class Node:
    def __init__(self, list, parentCost, parentId):
        self.lines = []
        self.lines.append(list[0:3])
        self.lines.append(list[3:6])
        self.lines.append(list[6:9])
        self.id = ''.join(str(x) for x in list)
        self.cost = parentCost+1
        self.heuristic = self.calcHeuristic()
        self.parentId = parentId
        self.noneLocation = self.getLocation()

    def calcHeuristic(self):
        global FINAL_STATE
        heuristicValue = 0
        flatLines = []
        # converts lines to one dimension list
        for sublist in self.lines:
            for item in sublist:
                flatLines.append(item)
        
        for i in range(len(flatLines)):
            if(flatLines[i] != FINAL_STATE[i]):
                heuristicValue+=1
        return heuristicValue

    def getLocation(self):
        for i in range(len(self.lines)):
            if None in self.lines[i]:
                return i, self.lines[i].index(None)
        return False

    def getParentId(self):
        return self.parentId

    def getId(self):
        return self.id

    def getCost(self):
        return self.cost
    
    def getHeuristic(self):
        return self.heuristic

    def getLines(self):
        return self.lines

def isTarget(S0,Sf):
    if (S0.getId() == Sf.getId()):
        return True
    else:
        return False

def swap (x, i_start, j_start, i_end, j_end):
    aux = x[i_start][j_start]
    x[i_start][j_start] = x[i_end][j_end]
    x[i_end][j_end] = aux

    flatS = []
    for sublist in x:
        for item in sublist:
            flatS.append(item)
    return flatS

def createNodes(S, i, j):
    # it can go +-1 in i and j directions (4 possibilities)
    newNodes = []
    dir = [-1,1]
    for a in range(2):
        if(i+dir[a] <= 2 and i+dir[a] >= 0):
            parentLines = deepcopy(S.getLines())
            newList = swap(parentLines, i, j, i+dir[a], j)
            newNode = Node(newList , S.getCost(), S.getId())
            newNodes.append(newNode)
    for b in range(2):
        if(j+dir[b] <= 2 and j+dir[b] >= 0):
            parentLines = deepcopy(S.getLines())
            newList = swap(parentLines, i, j, i, j+dir[b])
            newNode = Node(newList, S.getCost(), S.getId())
            newNodes.append(newNode)
    return newNodes

def openNodes(S0):
    i,j = S0.getLocation()
    return createNodes(S0, i, j)

def deleteClosedNodes (A, F):
    def filterClosedNodes(node):
        for j in range(len(F)):
            if isTarget(node, F[j]):
                return False
        return True

    return list(filter(filterClosedNodes,A))

def mergeLists(A, newA):
    for nodeNewA in newA:
        for nodeA in A:
            if (isTarget(nodeNewA, nodeA)):
                if (nodeNewA.getCost() >= nodeA.getCost()):
                    newA.remove(nodeNewA)
                else:
                    A.remove(nodeA)
    return A+newA

def leastCost(elem):
    return elem.getCost()+elem.getHeuristic()

def getPath(S0, F):
    path = []
    parent = S0.getParentId()
    path.append(S0.getId())
    ### sugestao pro adas: 
        # varrer F criando uma estrutura com fácil acesso ao id e indice do elemento em F, dessa forma fica melhor.
        # Quem mandou ir no jogo do avai?
    while (parent != 'mirandao'):
        for node in F:
            if (node.getId() == parent):
                parent = node.getParentId()
                path.append(node.getId())
                print(path)
                F.remove(node)
    path.append(parent)
    return list(reversed(path))

    

def uniformCost(S0, Sf):
    F = []
    A = []
    while (not(isTarget(S0,Sf))):
        F.append(S0)
        print(S0.getId())
        # print('inicio\n')
        # for i in A:
        #     print('A antes de open nodes ' + i.getId() + '\n')
        newA = openNodes(S0)
        # for i in newA:
        #     print('newA ' + i.getId() + '\n')
        A = mergeLists(A, newA)
        # for i in A:
        #     print('A mergeado com newA ' + i.getId() + '\n')
        A = deleteClosedNodes(A, F)
        # for i in A:
        #     print('A com F removido ' + i.getId() + '\n')
        A.sort(key=leastCost)
        S0 = A[0]
        A.remove(S0)
    F.append(S0)
    return getPath(S0, F)


## implementar classe com id pra nao ficar iterando na merda toda

Sf = Node(FINAL_STATE, 9999999, '')
S0 = Node(START_STATE, -1, 'mirandao')
a = 'aaaaaaa'
uniformCost(S0, Sf)