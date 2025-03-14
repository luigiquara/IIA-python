from utils import argmax_random_tie

class DecisionTreeLearner():
    '''
    Addestra un albero di decisione.
       In input richiede:
        dataset: oggetto della classe DataSet.
            contiene gli esempi per il training e le funzioni per la gestione del data set
    
    Crea l'albero decisionale tramite la funzione decision_tree_learning() chiamata nel costruttore.
    Dopo l'addestramento, si utilizza la funzione predict() in fase di inferenza.
    '''

    def __init__(self, dataset):
        self.dataset = dataset
        self.tree = self.decision_tree_learning(dataset.examples, dataset.inputs)

    def decision_tree_learning(self, examples, attrs, parent_examples=()):
        if len(examples) == 0:
            return self.plurality_value(parent_examples)
        if self.all_same_class(examples):
            return DecisionLeaf(examples[0][self.dataset.target])
        if len(attrs) == 0:
            return self.plurality_value(examples)
        A = self.choose_attribute(attrs, examples)
        tree = DecisionFork(A, self.dataset.attr_names[A], self.plurality_value(examples))
        for (v_k, exs) in self.split_by(A, examples):
            subtree = self.decision_tree_learning(exs, remove_all(A, attrs), examples)
            tree.add(v_k, subtree)
        return tree


    def plurality_value(self, examples):
        '''
        Restituisce il valore di target più comune per l'insieme di esempi in input.
        '''

        popular = argmax_random_tie(self.dataset.values[self.dataset.target],
                                    key=lambda v: self.count(self.dataset.target, v, examples))
        return DecisionLeaf(popular)

    def count(self, attr, val, examples):
        '''Conta il numero di esempi che hanno l'attributo "attr" in input pari al valore "val"'''

        return sum(e[attr] == val for e in examples)

    def all_same_class(self, examples):
        '''Indica se tutti gli esempi in input hanno la stesso valore di target'''

        class0 = examples[0][self.dataset.target]
        return all(e[self.dataset.target] == class0 for e in examples)

    def choose_attribute(self, attrs, examples):
        '''Restituisce l'attributo con il più alto information gain'''

        return argmax_random_tie(attrs,
                                 key=lambda a: self.information_gain(a, examples))

    def information_gain(self, attr, examples):
        '''Restituisce la riduzione dell'entropia attesa effettuando lo split sull'attributo "attr"'''

        def I(examples):
            return information_content([self.count(self.dataset.target, v, examples)
                                        for v in self.dataset.values[self.dataset.target]])
        n = len(examples)
        remainder = sum((len(examples_i) / n) * I(examples_i)
                        for (v, examples_i) in self.split_by(attr, examples))
        return I(examples) - remainder

    def split_by(self, attr, examples):
        '''Restituisce una lista composta da coppie (val, examples), per ogni valore di "attr"'''

        return [(v, [e for e in examples if e[attr] == v])
                for v in self.dataset.values[attr]]

    def predict(self, x):
        return self.tree(x)

def information_content(values):
    '''Numero di bits necessari per rappresentare la distribuzione di probabilità di "values"'''

    probabilities = normalize(remove_all(0, values))
    return sum(-p * np.log2(p) for p in probabilities)

class DecisionLeaf:
    '''
    Una foglia di un albero decisione.
    Utilizzata per salvare un risultato.
    '''

    def __init__(self, result):
        self.result = result

    def __call__(self, example):
        return self.result

    def display(self, indent=0):
        print('RESULT =', self.result)

    def __repr__(self):
        return repr(self.result)

class DecisionFork:
    '''
    Una biforcazione in un albero decisionale.
    Contiene l'attributo da testare e un dizionario di rami,
    uno per ognuno dei valori dell'attributo
    '''

    def __init__(self, attr, attr_name=None, default_child=None, branches=None):
        '''Inizializzazione, che specifica l'attributo che viene testato in questa biforcazione'''

        self.attr = attr
        self.attr_name = attr_name or attr
        self.default_child = default_child
        self.branches = branches or {}

    def __call__(self, example):
        '''
        Dato un esempio in input, viene classificato in base all'attributo da testare.
        Restituisce il ramo selezionato.
        '''

        attr_val = example[self.attr]
        if attr_val in self.branches:
            return self.branches[attr_val](example)
        else:
            # restituisce la classe di default quando l'attributo è sconosciuto
            return self.default_child(example)

    def add(self, val, subtree):
        '''Metodo per aggiungere un ramo'''
        self.branches[val] = subtree

    def display(self, indent=0):
        name = self.attr_name
        print('Test', name)
        for (val, subtree) in self.branches.items():
            print(' ' * 4 * indent, name, '=', val, '==>', end=' ')
            subtree.display(indent + 1)

    def __repr__(self):
        return 'DecisionFork({0!r}, {1!r}, {2!r})'.format(self.attr, self.attr_name, self.branches)