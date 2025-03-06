import os

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