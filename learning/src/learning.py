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