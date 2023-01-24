# Generador de tablas SLR
# Diana Estefania Ortiz Ledesma 
# A01209403

class Token:

    # Constructor
    def __init__(self, value, terminal, first):
        
        self.value = value
        self.origin = [] 
        self.originProd = [] 
        self.productions = []  
        self.terminal = terminal  
        self.first = first  

        self.firstCalc = False 
        self.firstList = []  
        self.firstS = "" 
        self.firstProductions = []  

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

    # Agregar el origen de una producción
    def addOriginProduction(self, production):
        self.originProd.append(production)

    # Agrega un token a la producción temporal actual
    def addProduction(self, production):
        self.productions.append(production)

    # Devolver todas las producciones
    def getProduction(self):
        return self.productions[:]

    # Devuelve todas las producciones de los firsts
    def getFirstProduction(self):
       return self.firstProductions[:]

    # Gira la bandera si el token es una terminal
    def setTerminal(self, terminal):
        self.terminal = terminal

    # Calcular el first de una producción
    def calcFirst(self, tokens, production):
        
        if self.value == production[0]:
            self.duped = True
            return []

        productionFirsts = []
        numepsilon = 0
        for token in production:
            if token == None:
                continue

            if tokens[token] == 1:
                self.timesepsilon += 1
                return ['\' \'']

            arr = tokens[token].calcFirsts(tokens)
            if "\' \'" in arr:
                arr.remove("\' \'")
                numepsilon += 1
                productionFirsts += arr
                continue

            productionFirsts += arr
            break

        if numepsilon == len(production)-1:
            self.timesepsilon += 1
            productionFirsts.append('\' \'')

        return list(set(productionFirsts))

    # Calcular el first de todas las producciones de un token
    def calcFirsts(self, tokens):
        
        if self.firstCalc:
            return self.firstList[:]

        if self.terminal:
            self.firstList.append(self.value)
            self.firstCalc = True
            return self.firstList[:]

        for production in self.productions:
            arr = self.calcFirst(tokens, production)
            self.firstList += arr
            self.firstProductions.append(arr)

        self.firstList = list(set(self.firstList))
        self.firstCalc = True
        self.firstS = ", ".join(self.firstList)
        return self.firstList[:]

    # Consigue el first del token en la gramática
    def getFirsts(self, tokens):
        
        if self.firstCalc:
            return self.firstS

        self.calcFirsts(tokens)
        return self.firstS

    # Calcular el follow del token
    def calcFollows(self, tokens):
        
        if self.followCalc:
            return self.followList[:]

        if self.first:
            self.followList.append('$')

        for x in range(len(self.origin)):
            production = self.originProd[x]
            found = False
            for y in range(len(production)):
                token = production[y]

                if token == self.value:
                    found = True

                if (not found and token != self.value) or token == None:
                    continue

                if production[y+1] == None:
                    if self.origin[x] != self.value:
                        arr = tokens[self.origin[x]].calcFollows(tokens)
                        self.followList += arr
                    continue

                arr = tokens[production[y+1]].calcFirsts(tokens)
                if "\' \'" in arr:
                    arr.remove("\' \'")
                    self.followList += arr
                    continue

                self.followList += arr
                break

        self.followList = list(set(self.followList))

        self.followCalc = True

        self.followS = ", ".join(self.followList)
        return self.followList[:]

    # Obtener el follow del token
    def getFollows(self, tokens):
        
        if self.followCalc:
            return self.followS

        self.calcFollows(tokens)
        return self.followS

    # Calcular si el no terminal en la gramática es válido 
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
