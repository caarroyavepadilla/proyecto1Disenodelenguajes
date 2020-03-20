import arbolitos

EPSILON = "ε"
class Machine:
    def __init__(self, expresion):
        self.id = expresion
        self.states = []

class State:
    def __init__(self, identificacion):
        self.id = identificacion
        self.transitions = []
        self.accept = False
        self.vaina = []
        self.transitions.append(Transition(EPSILON, self.id))
class Transition:
    def __init__(self, char, destino):
        self.id = ""
        self.simbolo = char
        self.destino = destino
        

def ordenar_arbol(arbol):
    nodos = []
    if arbol.left != None:
        s = ordenar_arbol(arbol.left)
        for symb in s:
            nodos.append(symb)
    if arbol.right != None:
        s = ordenar_arbol(arbol.right)
        for symb in s:
            nodos.append(symb)
    nodos.append(arbol.data)
    return nodos