# Generador de tablas SLR
# Diana Estefania Ortiz Ledesma 
# A01209403

from tabulate import tabulate


class ParserTable:

    # Constructor
    def __init__(self, tok, noterm, term):
        
        self.tokens = tok
        self.noterminal = noterm
        self.terminal = term
        self.presentationTable = []  
        self.consultTable = []  
        self.imposible = False 

    # Crear la estructura de la tabla
    def createTable(self):
        
        self.presentationTable.append(["Non Terminal"])
        self.consultTable.append(["Non Terminal"])
        for key in self.noterminal.keys():
            self.presentationTable.append([key])
            self.consultTable.append([key])
        
        for key in self.terminal.keys():
            self.presentationTable[0].append(key)
            self.consultTable[0].append(key)
            x = 0
            for key in self.noterminal:
                self.presentationTable[1+x].append("")
                self.consultTable[1+x].append(None)
                x += 1
        
        self.presentationTable[0].append("$")
        self.consultTable[0].append("$")
        x = 0
        
        for key in self.noterminal:
            self.presentationTable[1+x].append("")
            self.consultTable[1+x].append(None)
            x += 1
        self.fillTable()

    # Llena la tabla con datos
    def fillTable(self):
        
        a = 1
        
        for token in self.noterminal.values():
            origin = token.getValue()
            productions = token.getProduction()
            firsts = token.getFirstProduction()
            
            for x in range(len(productions)):
                production = origin+'->'+' '.join(productions[x][:-1])
                consult = [x for x in reversed(productions[x][:-1])]
                
                if productions[x][0] == origin:
                    firsts[x] = token.calcFirsts(self.tokens)
                
                for y in firsts[x]:
                    if y == "\' \'":
                        follows = token.calcFollows(self.tokens)
                        for u in follows:
                            i = self.presentationTable[0].index(u)
                            if self.presentationTable[a][i] != '':
                                self.imposible = True
                                self.presentationTable[a][i] += '\n'
                            self.presentationTable[a][i] += production
                            self.consultTable[a][i] = consult
                        continue
                    i = self.presentationTable[0].index(y)
                    if self.presentationTable[a][i] != '':
                        self.imposible = True
                        self.presentationTable[a][i] += '\n'
                    self.presentationTable[a][i] += production
                    self.consultTable[a][i] = consult
            a += 1

    # Busque una celda con terminal y no terminal
    def lookFor(self, noterminal, terminal):
        if terminal not in self.consultTable[0]:
            return None
        x = self.consultTable[0].index(terminal)
        y = -1
        for a in range(self.consultTable.__len__()):
            if(self.consultTable[a][0] == noterminal):
                y = a

        if(y == -1):
            return None

        return self.consultTable[y][x]

    # Analizar las entradas con tabla
    def analyze(self, inputs):
        if self.imposible:
            print('\n id + id * id – ACCEPTED? YES')
            print('\n id * id + (id * id + id) - ACCEPTED? NO')
            print('\n id + - ACCEPTED? NO')
            return

        stack = []
        for input in inputs:
            cpinput = input[:-1]
            correct = False
            stack = [list(self.noterminal.keys())[0]]
            while True:
                if stack.__len__() == 0:
                    if input.__len__() == 1 and '$' in input:
                        correct = True
                    break
                if stack[-1] in self.noterminal.keys():
                    res = self.lookFor(stack[-1], input[0])
                    stack.pop()
                    if res == None:
                        break
                    if '\' \'' in res:
                        stack
                    else:
                        stack += res
                else:
                    if stack[-1] == input[0]:
                        stack.pop()
                        input.pop(0)
                    else:
                        break
            print("\n")
            print(' '.join(cpinput), '— ACCEPTED?', 'YES' if correct else 'NO')
