
# Calculando First's y Follow's 
# Diana Estefania Ortiz Ledesma 
# A01209403

class Token:

    # Constructor
    def __init__(self, value, terminal, first):
        
        self.value = value
        self.origin = [] 
        self.production = []  
        self.productions = []  
        self.follow = []  
        self.terminal = terminal  
        self.first = first  

        self.firstCalc = False  
        self.firstList = []  
        self.firstS = ""  

        self.followCalc = False  
        self.followList = []  
        self.followS = "" 

        self.timesepsilon = 0  
        self.duped = False  

    # Devuelve el valor del token
    def getValue(self):
        return self.value

    # Obtener el tipo de variable del token
    def getType(self):
        return type(self.value)

    # Agregar el origen del token
    def addOrigin(self, token):
        self.origin.append(token)

    # Agrega un token a la producción temporal actual
    def addProduction(self, token):
        self.production.append(token)

    # Terminar producción
    def endProduction(self):
        self.productions.append(self.production)
        self.production = []

    # Agrega el siguiente token en producción
    def addFollow(self, token):
        self.follow.append(token)

    # Cambia la bandera si el token es un terminal
    def setTerminal(self, terminal):
        self.terminal = terminal

    # Calcula el first del token
    def calcFirsts(self, tokens):
        if self.firstCalc:
            return self.firstList
        
        if self.terminal:
            self.firstList.append(self.value)
            self.firstCalc = True
            return self.firstList

        for x in self.productions:
            numepsilon = 0  

            if self.value == x[0]:
                self.duped = True
                continue

            for token in x:
                t = tokens[token]
                if t == 1:
                    if token not in self.firstList:
                        self.firstList.append(token)
                        self.timesepsilon += 1
                    break

                arr = tokens[token].calcFirsts(tokens)
                if "\' \'" in arr:
                    numepsilon += 1
                    arr.remove("\' \'")
                    self.firstList = list(set(self.firstList+arr))
                    continue

                self.firstList = list(set(self.firstList+arr))
                break

            if numepsilon == len(x):
                self.timesepsilon += 1
                self.firstList.append("\' \'")

        self.firstList = list(set(self.firstList))
        self.firstCalc = True
        self.firstS = ", ".join(self.firstList)
        return self.firstList

    # Consigue el first del token en la gramatica
    def getFirsts(self, tokens):
        if self.firstCalc:
            return self.firstS
        self.calcFirsts(tokens)
        return self.firstS

    # Calcula el follow del token
    def calcFollows(self, tokens):
        if self.followCalc:
            return self.followList

        if self.first:
            self.followList.append('$')

        for n in range(len(self.origin)):
            if self.follow[n] == None:
                if self.origin[n] != self.value:
                    arr = tokens[self.origin[n]].calcFollows(tokens)
                    self.followList = list(set(self.followList+arr))
                continue

            arr = tokens[self.follow[n]].calcFirsts(tokens)
            if "\' \'" in arr:
                arr.remove("\' \'")
                self.followList = list(
                    set(self.followList+arr+tokens[self.origin[n]].calcFollows(tokens)))
                continue

            self.followList = list(set(self.followList+arr))

        self.followList = list(set(self.followList))
        self.followCalc = True
        self.followS = ", ".join(self.followList)
        return self.followList

    # Obtenga lo siguiente del token
    def getFollows(self, tokens):
        if self.followCalc:
            return self.followS
        self.calcFollows(tokens)
        return self.followS

    # Calcular si el no terminal en la gramática es válido para ser LL(1)
    def isLL(self, tokens):
        if self.duped:
            return False

        if 1 < self.timesepsilon:
            return False

        arr = []
        for p in self.productions:
            arr.append(p[0])
        unique = list(set(arr))
        if len(unique) != len(arr):
            return False

        unique = list(set(self.firstList+self.followList))
        if len(unique) != (len(self.firstList)+len(self.followList)):
            return False

        return True
