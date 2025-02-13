import math
import random
import sys

from utils import Node

def hill_climbing(problema):
    # Ricerca locale hill climbing
    nodo_corrente = Node(problema.initial_state)

    while True:
        # Il metodo expand restituisce tutti i vicini di un nodo, uno alla volta
        # In questo modo, si ottengono tutti i nodi vicini
        vicini = list(nodo_corrente.expand(problema))
        if not vicini: # se il nodo corrente non ha vicini interrompi e restituisci current
            break

        # Seleziona il vicino con il valore più alto
        vicino_maggiore = sorted(vicini, key=lambda x: problema.value(x), reverse=True)[0]
        # Se il vicino maggiore ha comunque un valore minore del nodo corrente, interrompe l'esecuzione
        if problema.value(vicino_maggiore) <= problema.value(nodo_corrente):
            break
        else:
            nodo_corrente = vicino_maggiore
    return nodo_corrente

def exp_schedule(k=100, lam=0.5, limit=100):
    # Una possibile funzione di scheduling per simulated annealing.
    # In questo caso, la temperatura decresce seguendo una legge esponenziale
    # k indica la temperatura iniziale
    return lambda t: (k * math.exp(-lam * t) if t < limit else 0)

def simulated_annealing(problema, schedule=exp_schedule()):
    # Ricerca locale simulated annealing
    # L'algoritmo richiede una funzione di scheduling
    # per determinare l'andamento della temperatura
    nodo_corrente = Node(problema.initial_state)

    for t in range(sys.maxsize): #sys.maxsize è il massimo numero intero
        temp = schedule(t)
        if temp == 0: return nodo_corrente

        vicini = list(nodo_corrente.expand(problema))
        if not vicini: # se il nodo corrente non ha vicini interrompi e restituisci current
            break

        # il nodo successivo è scelto casualmente tra i vicini di quello corrente
        prossimo_nodo = random.choice(vicini)
        delta_e = problema.value(prossimo_nodo) - problema.value(nodo_corrente)
        if delta_e > 0 or random.random()<(math.exp(delta_e / temp)):
            nodo_corrente = prossimo_nodo