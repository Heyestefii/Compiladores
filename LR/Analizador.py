# Generador de tablas SLR
# Diana Estefania Ortiz Ledesma 
# A01209403

from Token import Token
from ParserTable import ParserTable


class Lexer:
    def __init__(self):

        self.terminal = {}  
        self.noterminal = {}   
        self.reserved = {}  

        self.arrow = False 
        self.firstL = True  
        self.origin = None 
        self.production = []  
        self.setReserved()

    # Definir las palabras reservadas que tiene el lexer
    def setReserved(self):
        self.reserved['->'] = 0
        self.reserved['\' \''] = 1

    # Escanea la línea para todas los tokens
    def scan(self, entrada):
        self.arrow = False
        token = None
        epsilon = 0  
        self.production = []

        for c in entrada:
            if 0 < epsilon:
                if epsilon == 1:
                    if c.isspace():
                        epsilon = 2
                        token += ' '
                        continue
                    else:
                        epsilon = 0
                elif epsilon == 2:
                    if c == '\'':
                        epsilon = 3
                        token += '\''
                        continue
                    else:
                        epsilon = 0
                        self.saveToken('\'')
                        token = None
                elif epsilon == 3:
                    if c.isspace():
                        epsilon = 0
                        self.saveToken(token)
                        token = None
                        continue
                    else:
                        epsilon = 0
                        self.saveToken('\'')
                        token = '\''

            if c.isspace():
                self.saveToken(token)
                token = None
                continue

            if c.isnumeric():
                if token == None:
                    token = 0
                elif isinstance(token, str):
                    token += c
                    continue
                token = (token*10)+int(c)

            elif c.isalpha():
                if token == None:
                    token = ''
                elif isinstance(token, int):
                    token = str(token)
                token += c

            elif c.isascii():
                if token == None:
                    if c == '\'':
                        epsilon = 1
                        token = '\''
                        continue
                    token = ''
                elif isinstance(token, int):
                    token = str(token)
                token += c
        self.saveToken(token)
        self.production.append(None)
        self.setOriginProductions()

    # Guarda el token en terminal o no terminal
    def saveToken(self, token):
        if token == None:
            return

        t = self.reserved.get(token)
        if t != None:
            if t == 0:
                self.arrow = True
                self.firstL = False  
            if t == 1:
                self.production.append('\' \'')
            return

        t = self.terminal.get(token)
        n = self.noterminal.get(token)

        if self.arrow == True:
            self.production.append(token)
            if n == None and t == None:
                self.terminal[token] = Token(token, True, self.firstL)
            return

        if t == None:
            t = Token(token, False, self.firstL)
        else:
            self.terminal.pop(token)
        if n == None:
            self.noterminal[token] = t
            self.noterminal[token].setTerminal(False)
        self.origin = token

    # Guarda el token en terminal o no terminal
    def setOriginProductions(self):
        self.noterminal[self.origin].addProduction(self.production)

        for token in self.production:
            if token in self.terminal.keys():
                self.terminal[token].addOrigin(self.origin)
                self.terminal[token].addOriginProduction(self.production)
            elif token in self.noterminal.keys():
                self.noterminal[token].addOrigin(self.origin)
                self.noterminal[token].addOriginProduction(self.production)

    # Imprime el primero y sigue del no terminal
    def printFirstsFollows(self):
        tokens = {**self.noterminal, **self.terminal, **self.reserved}
        for token in self.noterminal.values():
            print(token.getValue(),
                  " => FIRST ={",
                  token.getFirsts(tokens),
                  "}, FOLLOW = {",
                  token.getFollows(tokens), "}", sep='')
        print("LL(1)? ", end='')
        for token in self.noterminal.values():
            if token.isLL(tokens) == False:
                print('No')
                return
        print('Yes')

    # Imprimir todos los terminales y no terminales que tiene el lexer
    def toString(self):
        print('Terminal:', end='')
        tokens = list(self.terminal.values())
        for i in range(tokens.__len__()):
            if i != 0:
                print(',', end='')
            print(' '+str(tokens[i].getValue()), end='')

        print('\nNon terminal:', end='')
        tokens = list(self.noterminal.values())
        for i in range(tokens.__len__()):
            if i != 0:
                print(',', end='')
            print(' '+str(tokens[i].getValue()), end='')
        print('\n')

    # Imprimir la tabla y evaluar
    def evaluate(self, inputs):
        tokens = {**self.noterminal, **self.terminal, **self.reserved}
        for token in self.noterminal.values():
            token.getFirsts(tokens)
            token.getFollows(tokens)
        analyzer = ParserTable(tokens, self.noterminal, self.terminal)
        analyzer.createTable()
        analyzer.analyze(inputs)


num, eval = [int(x) for x in input().split()]  
lexer = Lexer()  
cadena = []
for n in range(num):  
    lexer.scan(input())  

for n in range(eval):
    l = list(input().split(' '))
    l.append('$')
    cadena.append(l)

lexer.evaluate(cadena)
