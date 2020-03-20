import nfa
import automateichon
from graphviz import Digraph
VALIDOS = ["A", "B", "C", "D" ,"E", "a" ,"b" ,"c" ,"d" ,"e","ε", "0","1"]
OPERADORES = ["*", "|", "?", "+", "^", ")"]
OPERADORESUNI = ["*", "?", "+"]
ABCEDARIO = ["A", "B", "C", "D" ,"E", "F","G" ,"H", "I", "J"] 
COUNT = [10]
EPSILON = "ε"
class Nodo:
    def __init__(self,data):
        self.right = None
        self.left = None
        self.data = data

def print2DUtil(root, space) : 
  
    # Base case  
    if (root == None) : 
        return
  
    # Increase distance between levels  
    space += COUNT[0] 
  
    # Process right child first  
    print2DUtil(root.right, space)  
  
    # Print current node after space  
    # count  
    print()  
    for _ in range(COUNT[0], space): 
        print(end = " ")
    print(root.data)  
  
    # Process left child  
    print2DUtil(root.left, space)  
  
# Wrapper over print2DUtil()  
def print2D(root) : 
      
    # space=[0] 
    # Pass initial space count as 0  
    print2DUtil(root, 0)

def arbolillo(expresion):
    vals = []
    ops = []
    i = 0

    while i < len(expresion):
        if expresion[i] == '(':
            ops.append(expresion[i])  
        elif expresion[i] in VALIDOS:
            val = ""
            while(i<len(expresion) and expresion[i] not in OPERADORES):
                val += expresion[i]
                i += 1
            i -= 1
            val = Nodo(val)
            vals.append(val)

        elif expresion[i] == ')':
            while len(ops) != 0 and ops[-1] != '(':
                val2 = vals.pop()
                val1 = vals.pop()
                op = ops.pop()
                nodito = Nodo(op)
                nodito.left = val1
                nodito.right = val2
                vals.append(nodito)
            ops.pop()

        else:
            if(expresion[i] in OPERADORESUNI):
                ops.append(expresion[i])
                op = ops.pop()
                val = vals.pop()
                nodito = Nodo(op)
                nodito.right = None
                nodito.left = val
                vals.append(nodito)
            else:
                while (len(ops) != 0 and ops[-1] != '('):
                    op = ops.pop()
                    val2 = vals.pop()
                    val1 = vals.pop()
                    nodito = Nodo(op)
                    nodito.left = val1
                    nodito.right = val2
                    vals.append(nodito)
                ops.append(expresion[i])

        i += 1
    while len(ops) != 0:
        val2 = vals.pop()
        val1 = vals.pop()
        op = ops.pop()
        nodito = Nodo(op)
        nodito.left = val1
        nodito.right = val2
        vals.append(nodito)
        if (len(vals) == 1):
            return vals[-1]
    return vals[-1]

def create_automataRepresentation(arbolito, expresion):
    auto = nfa.Machine(expresion)
    print2D(arbolito)
    automaton = automateichon.automataBuilder(arbolito, auto)
    auto.states[-1].accept = True
    dfatext = open("nfa.txt","w")
    for state in auto.states:
        identidad = "estado: " + str(state.id) + "\n"
        aceptacion = "Aceptacion: "+str(state.accept) + "\n" 
        dfatext.write(identidad)
        dfatext.write(aceptacion)
        for trap in state.transitions:
            if trap.simbolo == EPSILON:
                z = "E"
            else:
                z = trap.simbolo
            texto = "Transicion: " + str(trap.destino) + " " + "Con: " + z + "\n"
            dfatext.write(texto)
    dfatext.close
  
    dot = Digraph()
    for state in auto.states:
        if state.accept == True:
            dot.node(str(state.id), str(state.id), shape = "doublecircle")
        for t in state.transitions:
            dot.edge(str(state.id), str(t.destino), str(t.simbolo))
    print(dot.source)
    dot.render('test-output/round-table.pdf', view=False)
    return automaton
    
def cerraduraEpsilon(automata, current):
    for i in current:
        for j in automata.states[i].transitions:
            if j.simbolo == EPSILON and j.destino not in current:
                current.append(j.destino)
    return current

def matchingNfa(arbolito, expresion, textillo):
    auto = nfa.Machine(expresion)
    automateichon.automataBuilder(arbolito, auto)
    aceptados = []
    for r in expresion:
        if r not in OPERADORES:
            if r != '(':
                aceptados.append(r)
    for x in textillo:
        if x not in aceptados:
            print("no aceptado")
            return 0
    opciones = list(textillo)
    estaditos = [0]
    estaditos = cerraduraEpsilon(auto, estaditos)
    auto.states[-1].accept = True
    i = 0
    while True:
        tempstates = []
        for estado in estaditos:
            for trans in auto.states[estado].transitions:
                if trans.simbolo == opciones[i] and trans.destino not in tempstates:
                    tempstates.append(trans.destino)
        i += 1
        tempstates = cerraduraEpsilon(auto, tempstates)
        if not tempstates and expresion == EPSILON:
            break
        estaditos = tempstates.copy()
        if i > len(opciones)-1:
            break
    for x in estaditos:
        if auto.states[x].accept:
            return print("Aceptado")
    return print("No Aceptado")

def nfaToDfa(arbolito, expresion, textillo):
    #hacer automata
    auto = nfa.Machine(expresion)
    automata = nfa.Machine(expresion)
    nuevosEstados = []
    opciones = []
    for u in expresion:
        if u not in OPERADORES:
            if u != '(' and u not in opciones:
                opciones.append(u)
    automateichon.automataBuilder(arbolito, auto)
    primero = cerraduraEpsilon(auto, [0])
    primero = set(primero)
    auto.states[-1].accept = True
    nuevosEstados.append(primero)
    primerito = nfa.State(len(automata.states))
    primerito.vaina.append(primero)           
    automata.states.append(primerito)
    for i in automata.states:
        for opcion in opciones:
            tempstates = set()
            for state in auto.states:
                if state.id in nuevosEstados[i.id]:
                    for trans in state.transitions: 
                        if trans.simbolo == opcion:
                            tempstates.add(trans.destino)
            x = set()
            for temp in tempstates:
                x.add(temp)
                x.update(cerraduraEpsilon(auto,[temp]))
            if x not in nuevosEstados:
                if len(x) != 0:
                    nuevosEstados.append(x)
                    estadox = nfa.State(len(automata.states))
                    estadox.vaina.append(x)
                    for y in x:
                        if auto.states[y].accept == True:
                            estadox.accept = True
                    automata.states.append(estadox)
                    i.transitions.append(nfa.Transition(opcion,estadox.id))
            elif x in nuevosEstados:
                if len(x) != 0:
                    for h in automata.states:
                        if h.vaina[0] == x:
                            i.transitions.append(nfa.Transition(opcion,h.id))
    print(nuevosEstados)
    #imprimir automata
    dot = Digraph()
    for state in automata.states:
        if state.accept == True:
            dot.node(str(state.id), str(state.id), shape = "doublecircle")
        for t in state.transitions:
            dot.edge(str(state.id), str(t.destino), str(t.simbolo))
    print(dot.source)
    dot.render('test-output/dfa.pdf', view=False)

    dfatext = open("dfa.txt","w")
    for state in automata.states:
        identidad = "estado: " + str(state.id) + "\n"
        aceptacion = "Aceptacion: "+str(state.accept) + "\n" 
        dfatext.write(identidad)
        dfatext.write(aceptacion)
        for trap in state.transitions:
            if trap.simbolo == EPSILON:
                z = "E"
            else:
                z = trap.simbolo
            texto = "Transicion: " + str(trap.destino) + " " + "Con: " + z + "\n"
            dfatext.write(texto)
    dfatext.close

 #matching
    aceptados = []
    for e in expresion:
        if e not in OPERADORES:
            if e != '(':
                aceptados.append(e)
    for g in textillo:
        if g not in aceptados:
            print("no aceptado")
            return 0
    opts = list(textillo)
    est = [0]
    est = cerraduraEpsilon(automata, est)
    q = 0
    while True:
        temporales = []
        for es in est:
            for trans in automata.states[es].transitions:
                if trans.simbolo == opts[q] and trans.destino not in temporales:
                    temporales.append(trans.destino)
        q += 1
        temporales = cerraduraEpsilon(automata, temporales)
        if not temporales and opts == EPSILON:
            break
        est = temporales.copy()
        if q > len(opts)-1:
            break
    for x in est:
        if automata.states[x].accept:
            return print("Aceptado")
    return print("No Aceptado")  

if __name__ == "__main__":
    print("Ingrese la expresion Regular con el simbolo '^' para la concatenacion: ")
    exp = input()
    print("Ingrese la cadena a probar:")
    cadena = input()
    ans = arbolillo(exp)
    create_automataRepresentation(ans, exp)
    matchingNfa(ans,exp, cadena)
    nfaToDfa(ans,exp,cadena) 