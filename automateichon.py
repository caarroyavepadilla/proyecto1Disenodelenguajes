import nfa
import arbolitos
OPERADORES = ['|', '*', '+', '?', '^', ')', '(']
EPSILON = "ε"

global_counter = 0

def automataBuilder(arbolillo,automata):
    inicio = 0
    final = 0
    if arbolillo.data == '^':
        inicio, final = concatAutomata(arbolillo, automata)
    elif arbolillo.data == '|':
        inicio, final = orAutomata(arbolillo, automata)
    elif arbolillo.data == '*':
        inicio, final = limpioAutomata(arbolillo, automata)
    elif arbolillo.data == '?':
        inicio, final = questionAutomata(arbolillo, automata)
    elif arbolillo.data == '+':
        inicio, final = limpioplusAutomata(arbolillo, automata)
    else:
        inicio, final = automata1(arbolillo, automata)
    return inicio, final

def concatAutomata(arbolillo,automata):
    if arbolillo.left.data in OPERADORES:
        estado1, final1 = automataBuilder(arbolillo.left, automata)
    else:
        estado1, final1 = automata1(arbolillo.left, automata)
    
    if arbolillo.right.data in OPERADORES:
        estado2, final2 = automataBuilder(arbolillo.right, automata)
    else:
        estado2, final2 = automata1(arbolillo.right, automata)
    
    final1.transitions.append(nfa.Transition(EPSILON, estado2.id))
    return estado1, final2

def orAutomata(arbolillo, automata):

    inicio = nfa.State(len(automata.states))
    automata.states.append(inicio)
    if arbolillo.left.data in OPERADORES:
        estado1, final1 = automataBuilder(arbolillo.left, automata)
    else:
        estado1, final1 = automata1(arbolillo.left, automata)
    
    if arbolillo.right.data in OPERADORES:
        estado2, final2 = automataBuilder(arbolillo.right, automata)
    else:
        estado2, final2 = automata1(arbolillo.right, automata)
    final = nfa.State(len(automata.states))
    automata.states.append(final)

    inicio.transitions.append(nfa.Transition(EPSILON, estado1.id))
    inicio.transitions.append(nfa.Transition(EPSILON, estado2.id))
    final1.transitions.append(nfa.Transition(EPSILON, final.id))
    final2.transitions.append(nfa.Transition(EPSILON, final.id))

    return inicio, final
    
def limpioAutomata(arbolillo, automata):
    inicio = nfa.State(len(automata.states))
    automata.states.append(inicio)
    if arbolillo.left.data in OPERADORES:
        estado1, final1 = automataBuilder(arbolillo.left, automata)
    else:
        estado1, final1 = automata1(arbolillo.left, automata)

    final = nfa.State(len(automata.states))
    automata.states.append(final)
    inicio.transitions.append(nfa.Transition(EPSILON, estado1.id))
    inicio.transitions.append(nfa.Transition(EPSILON, final.id))
    final1.transitions.append(nfa.Transition(EPSILON, estado1.id))
    final1.transitions.append(nfa.Transition(EPSILON,final.id))
    return inicio, final

def questionAutomata(arbolillo, automata):
    inicio = nfa.State(len(automata.states))
    automata.states.append(inicio)
    temp = arbolitos.arbolillo(EPSILON)
    if arbolillo.left.data in OPERADORES:
        estado1, final1 = automataBuilder(arbolillo.left, automata)
    else:
        estado1, final1 = automata1(arbolillo.left, automata)
    if temp.data in OPERADORES:
        estado2, final2 = automataBuilder(temp, automata)
    else:
        estado2, final2 = automata1(temp, automata)
    final = nfa.State(len(automata.states))
    automata.states.append(final)

    inicio.transitions.append(nfa.Transition(EPSILON, estado1.id))
    inicio.transitions.append(nfa.Transition(EPSILON, estado2.id))
    final1.transitions.append(nfa.Transition(EPSILON, final.id))
    final2.transitions.append(nfa.Transition(EPSILON,final.id))

    return inicio, final

def limpioplusAutomata(arbolillo, automata):
    inicio = nfa.State(len(automata.states))
    automata.states.append(inicio)
    if arbolillo.left.data in OPERADORES:
        estado1, final1 = automataBuilder(arbolillo.left, automata)
    else:
        estado1, final1 = automata1(arbolillo.left, automata)
    final = nfa.State(len(automata.states))
    automata.states.append(final)
    inicio.transitions.append(nfa.Transition(EPSILON, estado1.id))
    final1.transitions.append(nfa.Transition(EPSILON, estado1.id))
    final1.transitions.append(nfa.Transition(EPSILON,final.id))
    return inicio, final


def automata1(arbolillo, automata):
    signo = arbolillo.data
    primero = nfa.State(len(automata.states))
    automata.states.append(primero)
    segundo = nfa.State(len(automata.states))
    automata.states.append(segundo)
    primero.transitions.append(nfa.Transition(signo, segundo.id))
    return primero, segundo