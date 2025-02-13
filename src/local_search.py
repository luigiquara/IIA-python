import random
import sys

def hill_climbing(problem):
    # Ricerca locale hill climbing
    current = problem.initial_state

    while True:
        # Il metodo expand restituisce tutti i vicini di un nodo, uno alla volta
        # In questo modo, si ottengono tutti i nodi vicini
        neighbors = list(current.expand(problem))
        if not neighbors: # se il nodo corrente non ha vicini interrompi e restituisci current
            break

        # Seleziona il vicino con il valore più alto
        highest_neighbor = sorted(neighbors, key=lambda x: x.state, reverse=True)[0]
        # Se il vicino maggiore ha comunque un valore minore del nodo corrente, interrompe l'esecuzione
        if highest_neighbor.state <= current.state:
            break
        else:
            current = highest_neighbor
    return current

def exp_schedule(k=100, lam=0.5, limit=100):
    # Una possibile funzione di scheduling per simulated annealing.
    # In questo caso, la temperatura decresce seguendo una legge esponenziale
    # k indica la temperatura iniziale
    return lambda t: (k * math.exp(-lam * t) if t < limit else 0)

def simulated_annealing(problem, schedule=exp_schedule()):
    # Ricerca locale simulated annealing
    # L'algoritmo richiede una funzione di scheduling
    # per determinare l'andamento della temperatura
    current = problem.initial_state

    for t in range(sys.maxsize): #sys.maxsize è il massimo numero intero
        temp = schedule(t)
        if temp == 0: return current

        neighbors = list(current.expand(problem))
        if not neighbors: # se il nodo corrente non ha vicini interrompi e restituisci current
            break

        # il nodo successivo è scelto casualmente tra i vicini di quello corrente
        next = random.choice(neighbors)
        delta_e = next.state - current.state
        if delta_e > 0 or random.random()<(math.exp(delta_e / temp)):
            current = next