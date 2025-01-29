from collections import deque
import heapq

#La classe Problem è il "building block" utilizzato per rappresentare un problema
# Si tratta di una classe astratta - ogni problema specifico dovrà estendere questa classe
class Problem:
    # Costrutture. Specifica lo stato iniziale e lo stato (o la lista di stati) obiettivo
    def __init__(self, initial_state=None, goal_state=None):
        self.initial_state = initial_state
        self.goal_state = goal_state

    # Metodo astratto, deve essere implementato in ogni sottoclasse che specializza Problem
    # Dato lo stato 'state', restituisce la lista di azioni che possono essere eseguite
    def actions(self, state):
        raise NotImplementedError

    # Metodo astratto, deve essere implementato in ogni sottoclasse che specializza Problem
    # Dato lo stato 'state' e l'azione 'action', restituisce lo stato risultante in base al modello di transizione del problema
    def result(self, state, action):
        raise NotImplementedError

    # Dato lo stato 'state', restituisce True se è lo stato obiettivo, False altrimenti
    def is_goal(self, state):
        # controllo se self.goal_state è una lista, quindi esistono molteplici stati obiettivi
        if isinstance(self.goal_state, list):
            return state in self.goal_state
        # altrimenti, self.goal_state è un solo elemento, quindi esiste un solo stato obiettivo
        else: return state == self.goal_state

    # Restituisce il costo dell'esecuzione dell'azione 'action' che porti dallo 'stateA' allo 'stateB'
    # Questa implementazione di default prevede costo unitario per ogni azione
    def action_cost(self, action, stateA, stateB):
        return 1

    # Funzione euristica di default, che restituisce 0 per ogni nodo
    # Ogni problema specifico, sottoclasse della classe Problem, può specificare la propria funzione euristica
    def h(self, node):
        return 0


# La classe Node è il "building block" utilizzato per rappresentare un nodo nell'albero di ricerca
# Si tratta di una classe astratta - ogni nodo 
class Node:
    # Costruttore. Specifica lo stato associato al nodo, il nodo padre,
    # l'azione che ha generato il nodo, il costo del cammino dalla radice al nodo
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    # Specifica la stringa da stampare per rappresentare il nodo
    def __repr__(self):
        description = f'state: {self.state} - path cost: {self.path_cost}'
        return description

    # Restituisce la profondità del nodo
    # Se il nodo corrente non ha nodo padre, i.e. self.parent is None, la profondità è 0
    # Altrimenti, la profondità è quella del nodo padre più 1
    def __len__(self):
        if self.parent is None:
            return 0
        else:
            return 1 + len(self.parent)

    # Restituisce la lista delle azioni compiute per arrivare al nodo corrente
    # Se il nodo corrente non ha nodo padre, i.e. self.parent is None, nessuna azione è stata ancora eseguita
    def path_actions(self):
        if self.parent is None: actions = []
        else: return self.parent.path_actions().append(self.action)

    # Restituisce la lista degli stati attraversati per arrivare al nodo corrente
    # Se il node corrente non ha nodo padre, i.e. self.parent is None, la lista degli stati corrisponde allo stato attuale
    def path_states(self):
        if self.parent is None: states = self.state
        else: return self.parent.path_states().append(self.state)

    # Funzione che espande un nodo, generando tutti i nodi figli
    # La keyword "yield" permette di creare un generatore, che restituisce un nodo figlio alla volta
    def expand(self, problem):
        s = self.state
        # per ogni possibile azione nello stato corrente
        for action in problem.actions(s):
            s1 = problem.result(s, action)
            cost = self.path_cost + problem.action_cost(action, s, s1)
            yield Node(s1, self, action, cost)


class PriorityQueue:
    # Costruttore. L'argomento f specifica la funzione
    # da usare per calcolare la priorità di ciascun elemento della coda.
    def __init__(self, f=lambda x: x):
        self.elements = [] # la collezione elements è una coda di coppie (elemento, priorità)
        self.f = f

    # Restituisce la lunghezza della coda
    def __len__(self):
        return len(self.elements)

    # Inserisce l'elemento item in ordine nella coda
    # utilizzando la funzione di libreria heappush
    def insert(self, item):
        pair = (item, self.f(item))
        heapq.heappush(self.elements, pair)

    # Estrae l'elemento con il valore f(e) minore
    # utilizzando la funzione di libreria heappop
    def pop(self):
        return heapq.heappop(self.elements)[0] # restituisce solo l'elemento, non la priorità