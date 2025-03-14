import os
import random
from statistics import mean

def open_data(name, mode='r'):
    aima_root = os.path.join(os.path.dirname(__file__), '..')
    aima_file = os.path.join(aima_root, *['datasets', name])

    return open(aima_file, mode=mode)

def parse_csv(input, delim=','):
    '''
    Esegue il parsing di una stringa in formato 'comma-separated values' (csv),
    in cui ogni riga ha campi separati da virgole.
    Questi dati vengono convertiti in una lista di liste, saltando le righe vuote.
    Converte le stringhe che sembrano numeri in effettivo formato numerico.
    'delim' indica il carattere che delimita i campi del csv - ',' è il valore di default, ma '\t' e None sono possibili valori.

    Esempio di funzionamento:
    >>> parse_csv('1, 2, 3 \n 0, 2, na')
        [[1, 2, 3], [0, 2, 'na']]
    '''
    lines = [line for line in input.splitlines() if line.strip()]
    return [list(map(num_or_str, line.split(delim))) for line in lines]

def num_or_str(x):
    '''
    L'argomento in input è una stringa.
    Questo metodo la converte in un numero (int o float) se possibile, altrimenti ritorna la stringa con strip().
    Il metodo 'strip()' rimuove tutti gli spazi bianchi all'inizio e alla fine della stringa.
    '''

    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return str(x).strip()

def unique(seq):
    '''
    Rimuove elementi duplicati dalla sequenza in input.
    '''
    return list(set(seq))

def mean_boolean_error(X, Y):
    return mean(x != y for x, y in zip(X, Y))


identity = lambda x: x

def shuffled(iterable):
    '''Permutazione casuale di una copia dell'oggetto in input'''

    items = list(iterable)
    random.shuffle(items)
    return items

def argmax_random_tie(seq, key=identity):
    '''
    Restituisce un elemento con il valore più alto della funzione specificata.
    Risolve le parità in modo casuale
    '''

    return max(shuffled(seq), key=key)

def mode(data):
    """Return the most common data item. If there are ties, return any one of them."""
    '''
    Restituisce l'elemento più comune tra i dati in input.
    In caso di parità, restituisce uno qualsiasi degli elementi più comuni.
    '''

    [(item, count)] = collections.Counter(data).most_common(1)
    return item

def normalize(dist):
    '''Ogni numero viene moltiplicato per una costante, così che la somma sia 1.0'''

    if isinstance(dist, dict):
        total = sum(dist.values())
        for key in dist:
            dist[key] = dist[key] / total
            assert 0 <= dist[key] <= 1  # le probabilità devono essere tra 0 e 1 
        return dist
    total = sum(dist)
    return [(n / total) for n in dist]

def remove_all(item, seq):
    '''Restituisce una copia della sequenza in input, dopo aver rimosso tutte le occorrenze di item'''

    if isinstance(seq, str):
        return seq.replace(item, '')
    elif isinstance(seq, set):
        rest = seq.copy()
        rest.remove(item)
        return rest
    else:
        return [x for x in seq if x != item]