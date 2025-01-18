from utils import Node, Problem, PriorityQueue

LIFOQueue = list

# best_first_search è l'algoritmo di ricerca più generale,
# viene scelto il nodo con il valore minimo di una funzione di valutazione f.
# Variando la funzione di valutazione si ottengono diversi algoritmi di ricerca.
def best_first_search(problem, f):
    # ricerca best_first su grafo
    # la ricerca best_first utilizza una coda con priorità come frontiera
    # la coda viene inizializzata inserendo il primo nodo del problema
    node = Node(problem.initial_state)
    frontier = PriorityQueue(f=f)
    frontier.insert(node)
    explored = {problem.initial_state: node} # insieme degli stati già visitati

    while frontier: # finchè ci sono nodi nella frontiera
        # seleziona il nodo per l'espansione
        node = frontier.pop()
        # controlla se il nodo è uno stato obiettivo
        if problem.is_goal(node.state): return node

        # se non è uno stato obiettivo, il nodo viene espanso per aggiornare la frontiera
        for child in node.expand(problem):
            s = child.state
            # lo stato s viene aggiunto alla frontiera se:
            # 1. non fa parte dell'insieme dei nodi esplorati
            # 2. fa parte dei nodi già esplorati, ma ora è stato raggiunto seguendo un cammino di costo minore
            if s not in explored or child.path_cost < explored[s].path_cost:
                explored[s] = child
                frontier.insert(child)
    return None # in questo caso ritorna fallimento

# Restituisce True se il nodo 'node' forma un cammino ciclico di lunghezza 'k' o minore
def is_cycle(node, k=30):
    # implementazione ricorsiva
    def find_cycle(ancestor, k):
        return (ancestor is not None and k > 0 and
                (ancestor.state == node.state or find_cycle(ancestor.parent, k - 1)))
    return find_cycle(node.parent, k)

def best_first_search_tree(problem, f):
    # ricerca best-first su albero - non mantiene la collezione 'explored'
    # la ricerca best_first utilizza una coda con priorità come frontiera
    # la coda viene inizializzata inserendo il primo nodo del problema
    node = Node(problem.initial_state)
    frontier = PriorityQueue(f=f)
    frontier.insert(node)

    while frontier: # finchè ci sono nodi nella frontiera
        # seleziona il nodo per l'espansione
        node = frontier.pop()
        # controlla se il nodo è uno stato obiettivo
        if problem.is_goal(node.state): return node

        # se non è uno stato obiettivo, il nodo viene espando per aggiornare la frontiera
        for child in node.expand(problem):
            # non vengono aggiunti alla frontiera i nodi che formano cammini ciclici
            if not is_cycle(child):
                frontier.insert(child)
    return None # in questo caso ritorna fallimento

def breadth_first_search(problem):
    # Ricerca-grafo in ampiezza
    # La funzione di valutazione è la lunghezza -> vengono esaminati prima i nodi a profondità minore
    return best_first_search(problem, f=len)

def depth_first_search(problem):
    # Ricerca-grafo in profondità
    # La funzione di valutazione è l'opposto della lunghezza -> vengono esaminati prima i nodi a profondità maggiore
    return best_first_search(problem, f=lambda n: -len(n))

def depth_first_recursive_search(problem, node):
    # Ricerca in profondità ricorsiva
    if node is None:
        node = Node(problem.initial_state)

    # controlla se lo stato del nodo è uno stato obiettivo
    if problem.is_goal(node.state):
        return node
    # controlla se si è in un cammino ciclico
    elif is_cycle(node):
        return None
    
    # se il nodo obiettivo non è stato trovato
    # ripeti la ricerca espandendo l'albero di ricerca
    else:
        for child_node in node.expand(problem):
            result = depth_first_recursive_search(problem, child_node)
            if result:
                return result

def depth_limited_search(problem, depth_limit):
    """Ricerca in profondità con depth_limit"""
    frontier = LIFOQueue([Node(problem.initial_state)])

    # finchè la frontiera non è vuota
    while frontier:
        node = frontier.pop() # estrae un nodo dalla frontiera
        # controlla se lo stato del nodo è uno stato obiettivo
        if problem.is_goal(node.state):
            return node
        # controlla se si è superato il limite di profondità
        elif len(node) >= depth_limit:
            return None
        # controlla se si è in un cammino ciclico
        elif is_cycle(node):
            return None

        # altrimenti, espandi la frontiera
        else:
            for child in node.expand(problem):
                frontier.append(child)

def depth_recursive_limited_search(problem, node, depth_limit):
    """Ricerca in profondità ricorsiva con depth_limit"""

    if node is None:
        node = Node(problem.initial_state)
    # controllo per fermare la ricorsione
    if depth_limit < 0:
        return None
    # controlla se lo stato del nodo è uno stato obiettivo
    if problem.is_goal(node.state):
        return node
    # controlla se si è in cammino ciclico
    if is_cycle(node):
        return None

    # altrimenti, continua la ricerca
    for child_node in node.expand(problem):
        result = depth_recursive_limited_search(problem, child_node, depth_limit-1)
        if result:
            return result

# funzione di valutazione per la ricerca uniform_cost
def g(n): return n.path_cost

def uniform_cost_search(problem):
    # Ricerca-grafo uniform_cost
    # La funzione di valutazione dipende dal path_cost -> vengono esaminati prima i nodi a costo minore
    return best_first_search(problem, f=g)

def astar_search(problem, h=None):
    # Ricerca A*
    # È possibile definire una funzione euristica custom,
    # altrimenti viene utilizzata l'euristica indicata nella definizione del problema
    h = h or problem.h
    # vengono esaminati prima i nodi a costo stimato minore, seguendo la funzione di valutazione di A*
    return best_first_search(problem, f=lambda n: g(n) + h(n))