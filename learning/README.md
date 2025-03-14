# Algoritmi di apprendimento automatico
Questa cartella contiene l'implementazione di algoritmi di apprendimento automatico, con esempi di utilizzo su problemi concreti.

## Struttura

### ```datasets```
Contiene dei dataset di esempi, da utilizzare per valutare le prestazioni di un modello di apprendimento automatico.
+ ```abalone.csv```:
   + Problema di regressione, in merito alle caratteristiche delle conchiglie di una particolare varietà di mollusco
   + 8 attributi di input
   + 4177 esempi
+ ```bodyfat.csv```:
   + Problema di regressione, in merito alle caratteristiche misurabili di una persona
   + 13 attributi di input
   + 252 esempi 
+ ```iris.csv```:
   + Problema di classificazione a 3 classi, in merito alle caratteristiche osservabili di un fiore
   + 4 attributi di input
   + 150 esempi 
+ ```restaurant.csv```:
   + Problema di classificazione binaria
   + 12 esempi 
+ ```simplefit.csv```:
   + Semplice problema di regressione
   + 1 attributo di input
   + 94 esempi 

### ```src/utils.py```
Contiene l'implementazione di funzioni di supporto per l'utilizzo di algoritmi di apprendimento automatico.
In particolare, questo script contiene i metodi necessari per la lettura da file di un dataset.

### ```src/learning.py```
Contiene l'implementazione della classe Dataset e del metodo di cross validation:
+ ```DataSet```: classe che implementa l'astrazione di un dataset per un task di machine learning. Contiene gli esempi del dataset, con gli attributi di input e di target
+ ```cross_validation```: funzione per valutare le performance del modello di machine learning, secondo uno schema di k-fold cross validation

### ```src/linear_model.py```
Contiene l'implementazione del modello lineare visto a lezione:
+ ```LinearModel```: implementazione del modello lineare. Prevede un metodo ```fit()``` per l'addestramento del modello, e un metodo ```predict()``` per calcolare l'output del modello addestrato

### ```src/decision_tree.py```
Contiene l'implementazione del modello dell'albero decisionale:
+ ```DecisionLeaf```: implementazione di una foglia in un albero decisionale. Utilizzato per contenere un possibile risultato
+ ```DecisionFork```: implementazione di una biforcazione in un albero decisionale. Esegue la scelta del ramo da prendere in base all'esempio in input
+ ```DecisionTreeLearner```: implementazione di un albero decisionale. L'oggetto costruisce l'albero addestrato e prevede un metodo ```predict()``` per calcolare l'output del modello

### ```src/knn.py```
Contiene l'implementazione dell'algoritmo *k-Nearest Neighbors*:
+ ```NearestNeighborLearner```: implementazione del modello *KNN*. Prevede un metodo ```predict()``` per determinare l'output del modello, calcolato in base ad un voto di maggioranza tra i *k* elementi più vicini  

### ```esempi_modello_lineare.ipynb```
Jupyter Notebook che contiene la definizione di alcuni dataset di esempio, e alcune dimostrazioni di utilizzo del modello lineare.
