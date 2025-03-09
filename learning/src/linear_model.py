import random

class LinearModel:
    def __init__(self, dataset, learning_rate=0.01, epochs=100):
        '''
        Modello lineare con algoritmo di addestramento.
        Richiede in input:
          dataset: oggetto della classe DataSet che contiene gli esempi
                   per il training e le funzioni per la gestione del dataset
          learning rate: 'eta' a lezione -- default 0.01
          epochs: numero massimo di epoche per il training -- default 100
        '''

        self.dataset = dataset
        self.learning_rate = learning_rate
        self.epochs = epochs

        # idx_i è una lista degli indici nei dati di ogni esempio
        # come [0,1,2,3] o [2,5,7]
        self.idx_i = dataset.inputs # indici delle variabili di input

        # indici della variabile usata per target
        # la variabile target è chiamata 'y' a lezione
        self.idx_t = dataset.target

        # ogni esempio corrisponde a una lista contenente sia le variabili
        # di input sia il target
        self.examples = dataset.examples # lista di tutti gli esempi
        
        # numero di esempi nel dataset
        # l a lezione
        self.num_examples = len(self.examples)
        self.input_dim = len(self.idx_i) # dimensione dell'input (n a lezione)

        # inizializzazione dei pesi del modello in modo casuale
        # da una distribuzione uniforme tra -0.5 e 0.5
        self.w = [random.uniform(-0.5, 0.5) for _ in range(len(self.idx_i) + 1)]

    def fit(self, examples=None):
        '''
        Funzione utilizzata per addestrare il modello lineare.
        Restituisce l'errore quadratico medio (MSE) di training al variare delle epoche.
        '''

        examples = examples or self.dataset.examples
        training_error = []

        for epoch in range(self.epochs):
            err = []
            inputs = []

            # considera tutti gli esempi 
            for example in examples:
                # lista locali dei valori delle variabili in input
                # viene aggiunto l'input bias unitario
                x = [1] + [example[i] for i in self.idx_i]
                inputs.append(x) # aggiunge l'esempio attuale alla lista

                y_pred = self.dot_product(self.w, x) # calcola l'output del modello
                y = example[self.idx_t] # il valore target
                err.append(y - y_pred) # calcola l'errore e lo salva in una lista

            # calcolo il DeltaW (passo 2 alg. a lezione)
            for i in range(len(self.w)):
                delta_w_i = 0

                # calcolo iterativo di delta_w_i
                for p in range(self.num_examples):
                    x_p_i = inputs[p][i] # componente i del pattern p
                    delta_w_i += err[p] * x_p_i

                # si tiene in conto la costante '2', come a lezione
                # dividiamo per il numero di esempi --> LMS
                delta_w_i = 2 * (delta_w_i / self.num_examples)
                self.w[i] = self.w[i] + self.learning_rate * delta_w_i # aggiornamento del peso w_i (passo 3 alg. a lezione)

            # calcolo l'MSE per l'epoca corrente e lo salvo in una lista
            epoch_mse = sum(e**2 for e in err) / len(err)
            training_error.append(epoch_mse)

        return training_error

    def predict(self, x):
        '''
        Funzione utilizzata per calcolare l'output del modello addestrato
        per l'esempio specificato in input.
        '''

        return self.dot_product(self.w, x)
    
    def dot_product(self, A, B):
        '''
        Calcola il prodotto scalare tra il vettore 'A' e il vettore 'B'.
        '''

        # zip() è un metodo standard di python
        # permette di iterare su più oggetti contemporaneamente
        return sum(a * b for a, b in zip(A, B))