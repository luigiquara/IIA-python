import numpy as np
import random

from utils import open_data, mean_boolean_error, parse_csv, unique

class DataSet:
    """ Questa classe implementa l'astrazione di un dataset per un ML task
        Ha i seguenti campi:
        
    d.examples   Una lista di esempi. Ogni esempio e' una lista di valori di attributi.
    d.attrs      Una lista di indici interi all'interno delle posizioni di ciascun esempio.
                 Ogni posizione indicata in d.attrs si riferisce ad un attributo all'interno di ciascun esempio.
    d.attrnames  Lista opzionale di nomi mnemonici per gli attributi corrispondenti.
    d.target     L'indice corrispondente alla variabile che rappresenta il target in ciascun esempio.
                 Per default e' uguale all'attributo finale.
    d.inputs     Lista contenente gli indici corrispondenti alla variabili di input in ciascun esempio.
    d.values     Una lista di liste: ogni sottolista rappresenta l'insieme di possibili valori per l'atributo corrispondente.
                 Se inizialmente None, viene calcolato dagli esempi noti da self.set_problem.
                 Se diverso da None, un valore errato genera un ValueError.
    d.distance   Una funzione (distanza) da una coppia di esempi ad un valore non-negativo.
    d.name       Nome del dataset (solo a fini di visualizzazione).
    d.source     Sorgente del dataset (ad esempio URL)
    d.exclude    Una lista di indici di attributi da escludere da d.inputs.
                 Gli elementi di questa lista devono essere interi (indici) o nomi di attributi.

    Solitamente, per costruire il dataset e' sufficiente invocare il costruttore passando gli opportuni argomenti;
    per usare il dataset e' sufficiente accedere alle variabili d.examples, d.inputs e d.target."""

    def __init__(self, examples=None, attrs=None, attr_names=None, target=-1, inputs=None,
                 values=None, distance=mean_boolean_error, name='', source='', exclude=()):
        """
        Costruttore. Accetta come argomenti tutti i campi del dataset.
        Gli esempi possono anche essere una stringa o un file .csv da cui parsare gli esempi
        (automaticamente) usando la funzione parse_csv.
        """
        self.name = name
        self.source = source
        self.values = values
        self.distance = distance
        self.got_values_flag = bool(values)

        # Inizializza examples da una stringa, da una lista o da un file
        if isinstance(examples, str):
            # in questo caso parsa la stringa
            self.examples = parse_csv(examples)
        elif examples is None:
            # in questo caso parsa il file .csv
            self.examples = parse_csv(open_data(name + '.csv').read())
        else:
            # altrimenti gli esempi vengono presi dall'agomento
            self.examples = examples

        # attrs sono gli indici degli esempi
        if self.examples is not None and attrs is None:
            attrs = list(range(len(self.examples[0])))
        self.attrs = attrs

        # inizializza attr_names da una stringa, una lista o con valori di default
        if isinstance(attr_names, str):
            self.attr_names = attr_names.split()
        else:
            self.attr_names = attr_names or attrs
        self.set_problem(target, inputs=inputs, exclude=exclude)

    def set_problem(self, target, inputs=None, exclude=()):
        '''
        Metodo per impostare o modificare il target e/o gli inputs, in modo da poter usare un DataSet in diversi modi.
        Questo metodo calcola anche la lista dei possibili valori, se non specificata in precedenza.

        Se specificato, inputs è una lista di attributi. Altrimenti, con exclude è possibile indicare la lista degli attributi da ignorare in inputs.
        Gli attributi possono essere -n..n, oppure un attr_name.
        '''

        self.target = self.attr_num(target)
        exclude = list(map(self.attr_num, exclude))
        if inputs:
            self.inputs = remove_all(self.target, inputs)
        else:
            self.inputs = [a for a in self.attrs if a != self.target and a not in exclude]
        if not self.values:
            self.update_values()
        self.check_me()

    def check_me(self):
        '''
        Controllo sulle variabili della classe, per verificare che non ci siano errori.
        '''

        assert len(self.attr_names) == len(self.attrs)
        assert self.target in self.attrs
        assert self.target not in self.inputs
        assert set(self.inputs).issubset(set(self.attrs))
        if self.got_values_flag:
            list(map(self.check_example, self.examples))

    def add_example(self, example):
        '''
        Aggiungere un nuovo esempio alla lista di esempi.
        Controllo l'esempio prima di inserirlo
        '''

        self.check_example(example)
        self.examples.append(example)

    def check_example(self, example):
        '''
        Se example ha dei valori invalidi, genera ValueError
        '''

        if self.values:
            for a in self.attrs:
                if example[a] not in self.values[a]:
                    raise ValueError("Valore errato {} per l'attributo {} in {}"
                                     .format(example[a], self.attr_names[a], example))

    def attr_num(self, attr):
        '''
        Restituisce l'indice utilizzato per attr.
        Attr può essere un nome, oppure in intero in -n .. n-1.
        '''
        
        if isinstance(attr, str):
            return self.attr_names.index(attr)
        elif attr < 0:
            return len(self.attrs) + attr
        else:
            return attr

    def update_values(self):
        self.values = list(map(unique, zip(*self.examples)))

    def sanitize(self, example):
        '''
        Restituisce una copia di example, sostituendo con None il valore degli attributi non usati in input
        '''

        return [attr_i if i in self.inputs else None for i, attr_i in enumerate(example)][:-1]

    def classes_to_numbers(self, classes=None):
        '''
        Converte i nomi delle classi in numeri.
        '''

        if not classes:
            # se classes = None, estraile da values
            classes = sorted(self.values[self.target])
        for item in self.examples:
            item[self.target] = classes.index(item[self.target])

    def remove_examples(self, value=''):
        '''
        Rimuove gli esempi che contengono un determinato valore
        '''

        self.examples = [x for x in self.examples if value not in x]
        self.update_values()

    def split_values_by_classes(self):
        '''
        Separa i valori in base alla loro classe.
        '''

        buckets = defaultdict(lambda: [])
        target_names = self.values[self.target]

        for v in self.examples:
            item = [a for a in v if a not in target_names]  # rimuovi il target da item
            buckets[v[self.target]].append(item)  # aggiungi item al bucket (contenitore) corrispondente alla sua classe

        return buckets

    def find_means_and_deviations(self):
        '''
        Calcola la media e la deviazione standard di self.dataset.

        means: dizionario per ogni classe/target. Contiene la lista delle medie
        deviations: dizionario per ogni classe/target. Contiene la lista delle deviazioni standard
        '''

        target_names = self.values[self.target]
        feature_numbers = len(self.inputs)

        item_buckets = self.split_values_by_classes()

        means = defaultdict(lambda: [0] * feature_numbers)
        deviations = defaultdict(lambda: [0] * feature_numbers)

        for t in target_names:
            # find all the item feature values for item in class t
            features = [[] for _ in range(feature_numbers)]
            for item in item_buckets[t]:
                for i in range(feature_numbers):
                    features[i].append(item[i])

            # calcola medie e deviazioni stardard per la classe
            for i in range(feature_numbers):
                means[t][i] = mean(features[i])
                deviations[t][i] = stdev(features[i])

        return means, deviations

    def __repr__(self):
        return '<DataSet({}): {:d} esempi, {:d} attributi>'.format(self.name, len(self.examples), len(self.attrs))



def cross_validation(learner, dataset, loss, k=10, learning_rate = None, epochs = None, K = None, trials=1):
    '''
    Funzione usata per valutare la performance del modello di apprendimento secondo uno schema di k-fold cross validation.
    Restituisce in output la performance del learner in training e validation, mediata sulle k-fold

    'learning_rate' and 'epochs' are parameters for the LinearModel.
    K is a parameter for the k-NN model.
    '''

    if trials > 1:
        trial_errs = 0
        for t in range(trials):
            # implementazione ricorsiva
            errs = cross_validation(learner, dataset, size, k, trials)
            trial_errs += errs
        return trial_errs / trials

    # caso base della ricorsione
    else:
        train_fold_err = 0
        val_fold_err = 0
        n = len(dataset.examples)
        examples = dataset.examples
        random.shuffle(dataset.examples)

        for fold in range(k):
            # crea training e validation set, in base al fold corrente
            train_data, val_data = train_test_split(dataset, fold * (n // k), (fold + 1) * (n // k))
            dataset.examples = train_data

            # definizione del modello
            # se 'learning_rate' e 'epochs' sono definite
            # allora viene utilizzato il LinearModel
            if learning_rate and epochs:
                model = learner(dataset, learning_rate, epochs)

            # se 'K' è definito
            # allora viene utilizzato il modello k-NN
            elif K:
                model = learner(dataset, K)

            # altri casi 
            else:
                model = learner(dataset)

            #train_fold_err += model.fit(train_data)
            train_fold_err += loss(model, dataset, train_data)
            val_fold_err += loss(model, dataset, val_data)

            # gli esempi del dataset vengono ripristinati a quelli originali
            # una volta terminato il test
            dataset.examples = examples

        return train_fold_err/k, val_fold_err/k

def train_test_split(dataset, start=None, end=None):
    '''
    Funzione usata per separare gli esempi nel dataset in training e test set.
    I parametri start ed end identificano la porzione del dataset da usare in test set. Il resto viene usato per il training set.
    '''

    examples = dataset.examples
    train = examples[:start] + examples[end:]
    val = examples[start:end]

    return train, val

def mse_loss(model, dataset, examples=None): 
    """ Restituisce l'errore quadratico medio per un problema di regressione."""

    examples = examples or dataset.examples

    if len(examples) == 0:
        return float("inf")

    err = 0
    for example in examples:
        desired = example[dataset.target]

        #remove nones
        ex = dataset.sanitize(example)
        ex_c = [x for x in ex if x is not None]

        output = model.predict(ex_c)
        err = err + (desired-output)**2
        
    return (err / len(examples))

def accuracy_binary(model, dataset, examples=None, verbose=0):
    """Calcola l'accuratezza di un predittore per un problema di classificazione binaria
       (cioe' la proporzione degli esempi correttamente classificati).
       Nota: questa funzione assume che
        - il target e' un numero in {0,1}, dove
          0 corrisponde alla classe negativa
          1 corrisponde alla classe positiva
        - l'output e' un numero reale, che viene discretizzato in {0,1}
          usando 0.5 come valore soglia.

       Il parametro verbose in input e' usato per visualizzare gli output corretti
       e quelli errati, secondo il seguente schema:
       verbose - 0: No output; 1: Output wrong; 2 (or greater): Output correct"""

    if examples is None:
        examples = dataset.examples
    if len(examples) == 0:
        return 0.0
    right = 0.0
    for example in examples:
        desired = example[dataset.target]
        output = model.predict(dataset.sanitize(example))
        if output > 0.5:
            output = 1
        else:
            output = 0
                
        if output == desired:
            right += 1
            if verbose >= 2:
                print('   OK: got {} for {}'.format(desired, example))
        elif verbose:
            print('WRONG: got {}, expected {} for {}'.format(
                output, desired, example))
    return (right / len(examples))

def err_ratio(learner, dataset, examples=None):
    '''
    Calcola la proporzione di esempi che non sono correttamente predetti.
    '''

    examples = examples or dataset.examples
    if len(examples) == 0:
        return 0.0

    right = 0
    for example in examples:
        desired = example[dataset.target]
        output = learner.predict(dataset.sanitize(example))

        # np.allclose restituisce True se ogni elemento dei due array coincide, con una certa tolleranza
        if np.allclose(output, desired):
            right += 1

    return 1 - (right / len(examples))