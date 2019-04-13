class Node:
    def __init__(self, list, parentCost, parentId):
        self.lines = []
        self.lines.append(list[0:3])
        self.lines.append(list[3:6])
        self.lines.append(list[6:9])
        self.id = ''.join(str(x) for x in list)
        self.cost = parentCost+1
        self.parentId = parentId
        self.noneLocation = self.getLocation()

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

    def getLines(self):
        return self.lines

def isTarget(S0,Sf):
    if (S0.getId() == Sf.getId()):
        return True
    else:
        return False

def swap (S, i_start, j_start, i_end, j_end):
    S = S.getLines()
    aux = S[i_start][j_start]
    S[i_start][j_start] = S[i_end][j_end]
    S[i_end][j_end] = aux

    flatS = []
    for sublist in S:
        for item in sublist:
            flatS.append(item)
    return flatS

def createNodes(S, i, j):
    # it can go +-1 in i and j directions (4 possibilities)
    newNodes = []
    dir = [-1,1]
    for a in range(2):
        if(i+dir[a] <= 2 and i+dir[a] > 0):
            newNode = Node(swap(S, i, j, i+dir[a], j), S.getCost(), S.getId())
            newNodes.append(newNode)
    for b in range(2):
        if(j+dir[b] <= 2 and j+dir[b] >= 0):
            newNode = Node(swap(S, i, j, i, j+dir[b]), S.getCost(), S.getId())
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

    return list(filter(filterClosedNodes,A)

def mergeLists(A, newA):
    compensateA = 0
    compensateNewA = 0
    for i in range(len(newA)):
        for j in range(len(A)):
            if (isTarget(newA[i], A[j])):
                if (newA[i].getCost >= A[j].getCost()):
                    del newA[i + compensateNewA]
                    compensateNewA = compensateNewA - 1
                else:
                    del A[j + compensateA]
                    compensateA = compensateA - 1
    return A+newA

def leastCost(elem):
    return elem.getCost()

def getPath(S0, F):
    path = []
    parent = S0.getParentId()
    path.append(S0.getId())
    ### sugestao pro adas: 
        # varrer F criando uma estrutura com fácil acesso ao id e indice do elemento em F, dessa forma fica melhor.
        # Quem mandou ir no jogo do avai?
    while (parent != 'mirandao'):
        if (F[i].getId() == parent):
            parent = F[i].getId()
            path.append(parent)
            del F[i]
    path.append(parent)
    return path

    

def uniformCost(S0, Sf):
    F = []
    A = []
    while (not(isTarget(S0,Sf))):
        F.append(S0)
        newA = openNodes(S0)
        A = mergeLists(A, newA)
        A = deleteClosedNodes(A, F)
        for a in A:
            print(a.getId())
        A.sort(key=leastCost)
        S0 = A[0]
    F.append(S0)
    return getPath(S0, F)


## implementar classe com id pra nao ficar iterando na merda toda

Sf = Node([1, 2, 3, 4, 5, 6, 7, 8, None], 9999999, '')
S0 = Node([5, 1, None, 4, 7, 8, 3, 2, 6], -1, 'mirandao')

uniformCost(S0, Sf)