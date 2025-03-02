from utils import Problem

class Labirinto_Teseo(Problem):

    # Definizione di un costruttore custom
    # Oltre allo stato iniziale e l'obiettivo, vengono definite le possibili azioni
    # È possibile indicare l'ordine con il quale vengono prese in considerazione le azioni
    def __init__(self, initial_state='(2,1)', goal_state='(2,4)', possible_actions=['UP', 'DOWN', 'LEFT', 'RIGHT']):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.possible_actions = possible_actions

    # per ogni casella, restituisce l'insieme delle possibili azioni
    # in base alla conformazione del labirinto
    def actions(self, state):
        # initializza la lista delle possibili azioni
        # e rimuove le azioni che non possono essere eseguite
        possible_actions = self.possible_actions[:]

        if (state == '(2,1)') or (state == '(3,2)') or (state == '(1,2)') or (state == '(1,3)') \
            or (state == '(4,1)') or (state == '(4,2)') or (state == '(4,3)') or (state == '(4,4)'):
            possible_actions.remove('DOWN')

        if (state == '(3,1)') or (state == '(2,2)') or (state == '(2,3)') or (state == '(4,2)') \
           or (state == '(1,1)') or (state == '(1,2)') or (state == '(1,3)') or (state == '(1,4)'):
            possible_actions.remove('UP')

        if (state == '(3,2)') or (state == '(2,3)') or (state == '(3,3)') or \
        (state == '(1,4)') or (state == '(2,4)') or (state == '(3,4)') or (state == '(4,4)'):
            possible_actions.remove('RIGHT')

        if (state == '(4,2)') or (state == '(3,4)') or (state == '(3,3)') or \
        (state == '(1,1)') or (state == '(2,1)') or (state == '(3,1)') or (state == '(4,1)'):
            possible_actions.remove('LEFT')
        return possible_actions

    # Restituisce lo stato che si ottiene una volta eseguita l'azione indicata
    # mentre si è nella casella 'state'
    def result(self, state, action):

        # ottiene le coordinate RIGA - COLONNA corrispondenti a state
        row = int(state[1:2])
        col = int(state[-2:-1])

        if action == 'UP':
            row = row - 1
        elif action == 'DOWN':
            row = row + 1
        elif action == 'RIGHT':
            col = col + 1
        elif action == 'LEFT':
            col = col - 1

        # costruisci la nuova stringa di stato e restituiscila
        new_state = '('+str(row)+','+str(col)+')'
        return new_state

    # Funzione euristica
    # Restituisce l'opposto della profondità del nodo
    # Viene sottratto il costo del cammino, affinchè f = g + h sia uguale a -node.depth
    def h(self, node):
        return -len(node) - node.path_cost


class Labirinto_Teseo_Local(Labirinto_Teseo):
    """Versione del problema del labirinto di Teseo
        in cui e' definita una funzione value da usare
        per algoritmi di ricerca locale."""

    def value(self, node):
        # questa funzione calcola il valore della funzione da massimizzare
        # nel nostro caso e' basata sul numero minimo di mosse da compiere
        # per arrivare alla soluzione

        # calcola row e col dello stato corrispondente al nodo
        row = int(node.state[1:2])
        col = int(node.state[-2:-1])
        # calcola row e col dello stato goal
        row_goal = int(self.goal_state[1:2])
        col_goal = int(self.goal_state[-2:-1])

        return - (abs(row-row_goal) + abs(col-col_goal))

from local_search import hill_climbing, simulated_annealing

teseo_local = Labirinto_Teseo_Local()

teseo1_local = Labirinto_Teseo_Local(possible_actions=['UP','RIGHT','DOWN','LEFT'])
teseo2_local = Labirinto_Teseo_Local(possible_actions=['LEFT','DOWN','RIGHT','UP'])

print('Ricerca hill climbing')
solution = hill_climbing(teseo1_local)
print(solution)
print(solution.path_actions())

print('\nSimulated annealing')
solution = simulated_annealing(teseo1_local)
print(solution)
print(solution.path_actions())
