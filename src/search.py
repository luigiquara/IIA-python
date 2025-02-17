from utils import Node, Problem, PriorityQueue

LIFOQueue = list

# best_first_search è l'algoritmo di ricerca più generale,
# viene scelto il nodo con il valore minimo di una funzione di valutazione f.
# Variando la funzione di valutazione si ottengono diversi algoritmi di ricerca.
def best_first_search(problema, f):
    # ricerca best_first su grafo
    # la ricerca best_first utilizza una coda con priorità come frontiera
    # la coda viene inizializzata inserendo il primo nodo del problema
    nodo = Node(problem.initial_state)
    frontiera = PriorityQueue(f=f)
    frontiera.insert(nodo)
    raggiunti = {problem.initial_state: nodo} # insieme degli stati già visitati

    while frontiera: # finchè ci sono nodi nella frontiera
        # seleziona il nodo per l'espansione
        nodo = frontiera.pop()
        # controlla se il nodo è uno stato obiettivo
        if problema.is_goal(nodo.state): return nodo

        # se non è uno stato obiettivo, il nodo viene espanso per aggiornare la frontiera
        for nodo_figlio in nodo.expand(problema):
            s = nodo_figlio.state
            # lo stato s viene aggiunto alla frontiera se:
            # 1. non fa parte dell'insieme dei nodi esplorati
            # 2. fa parte dei nodi già esplorati, ma ora è stato raggiunto seguendo un cammino di costo minore
            if s not in raggiunti or nodo_figlio.path_cost < raggiunti[s].path_cost:
                raggiunti[s] = nodo_figlio
                frontiera.insert(nodo_figlio)
    return None # in questo caso ritorna fallimento

# Restituisce True se il nodo 'node' forma un cammino ciclico di lunghezza k o minore
def is_cycle(nodo, k=30):
    nodo_padre = node.parent
    steps = 0

    while nodo_padre is not None and steps < k:
        if nodo_padre.state == nodo.state:
            return True  # Abbiamo trovato un ciclo
        nodo_padre = nodo_padre.parent
        steps += 1

    return False

def best_first_search_tree(problema, f):
    # ricerca best-first su albero - non mantiene la collezione 'explored'
    # la ricerca best_first utilizza una coda con priorità come frontiera
    # la coda viene inizializzata inserendo il primo nodo del problema
    nodo = Node(problema.initial_state)
    frontiera = PriorityQueue(f=f)
    frontiera.insert(node)

    while frontiera: # finchè ci sono nodi nella frontiera
        # seleziona il nodo per l'espansione
        nodo = frontiera.pop()
        # controlla se il nodo è uno stato obiettivo
        if problema.is_goal(node.state):
            return nodo

        # se non è uno stato obiettivo, il nodo viene espando per aggiornare la frontiera
        for nodo_figlio in nodo.expand(problema):
            # non vengono aggiunti alla frontiera i nodi che formano cammini ciclici
            #if not is_cycle(child):
                #frontier.insert(child)
            frontiera.insert(nodo_figlio)
    return None # in questo caso ritorna fallimento

def breadth_first_search(problema):
    # Ricerca-grafo in ampiezza
    # La funzione di valutazione è la lunghezza -> vengono esaminati prima i nodi a profondità minore
    return best_first_search(problema, f=len)

def depth_first_search(problema):
    # Ricerca-grafo in profondità
    # La funzione di valutazione è l'opposto della lunghezza -> vengono esaminati prima i nodi a profondità maggiore
    return best_first_search(problema, f=lambda n: -len(n))

def depth_first_search_tree(problema):
    return best_first_search_tree(problema, f=lambda n: -len(n))

def depth_first_recursive_search(problema, nodo=None):
    # Ricerca in profondità ricorsiva
    if nodo is None:
        nodo = Node(problema.initial_state)

    # controlla se lo stato del nodo è uno stato obiettivo
    if problema.is_goal(nodo.state):
        return nodo
    # controlla se si è in un cammino ciclico
    elif is_cycle(nodo):
        return None
    
    # se il nodo obiettivo non è stato trovato
    # ripeti la ricerca espandendo l'albero di ricerca
    else:
        for nodo_figlio in nodo.expand(problema):
            result = depth_first_recursive_search(problema, nodo_figlio)
            if result:
                return result

def depth_limited_search(problema, depth_limit):
    """Ricerca a profondità limitata"""
    frontiera = LIFOQueue([Node(problem.initial_state)])

    # finchè la frontiera non è vuota
    while frontiera:
        nodo = frontiera.pop() # estrae un nodo dalla frontiera
        # controlla se lo stato del nodo è uno stato obiettivo
        if problema.is_goal(nodo.state):
            return nodo
        # controlla se si è superato il limite di profondità
        elif len(nodo) > depth_limit:
            continue
            #return None
        # controlla se si è in un cammino ciclico
        elif is_cycle(nodo):
            continue

        # altrimenti, espandi la frontiera
        else:
            for nodo_figlio in nodo.expand(problema):
                frontiera.append(nodo_figlio)

    return None # in questo caso ritorna con fallimento

def depth_recursive_limited_search(problema, nodo=None, depth_limit=100):
    """Ricerca a profondità limitata ricorsiva"""

    if nodo is None:
        nodo = Node(problem.initial_state)
    # controllo per fermare la ricorsione
    if depth_limit < 0:
        return None
    # controlla se lo stato del nodo è uno stato obiettivo
    if problema.is_goal(nodo.state):
        return nodo
    # controlla se si è in cammino ciclico
    if is_cycle(nodo):
        return None

    # altrimenti, continua la ricerca
    for nodo_figlio in nodo.expand(problema):
        result = depth_recursive_limited_search(problema, nodo_figlio, depth_limit-1)
        if result:
            return result

# funzione di valutazione per la ricerca uniform_cost
def g(n): return n.path_cost

def uniform_cost_search(problema):
    # Ricerca-grafo a costo uniforme
    # La funzione di valutazione dipende dal path_cost -> vengono esaminati prima i nodi a costo minore
    return best_first_search(problema, f=g)

def astar_search(problema, h=None):
    # Ricerca A*
    # È possibile definire una funzione euristica custom,
    # altrimenti viene utilizzata l'euristica indicata nella definizione del problema
    h = h or problema.h
    # vengono esaminati prima i nodi a costo stimato minore, seguendo la funzione di valutazione di A*
    return best_first_search(problema, f=lambda n: g(n) + h(n))
