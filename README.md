# IIA-python
Algoritmi e applicazioni di IA relative al corso "Introduzione all'Intelligenza Artificiale", Corso di Laurea in Informatica, Università di Pisa.

Contiene l'implementazione di algoritmi di ricerca globale e locale, aggiornata alla quarta edizione dell'AIMA, con esempi di utilizzo su problemi concreti.

## Struttura

Il repository è strutturato come segue:

```
├── src/
│   ├── utils.py                 # Classi di supporto per nodi e problemi
│   ├── search.py                # Implementazione degli algoritmi di ricerca
│   └── local_search.py          # Implementazione degli algoritmi di ricerca locale
├── esempi_ricerca.ipynb         # Notebook con esempi di utilizzo degli algoritmi di ricerca
├── esempi_ricerca_locale.ipynb  # Notebook con esempi di utilizzo degli algoritmi di ricerca locale
└── README.md                    # Questo file
```

### ```src/utils.py```
Contiene le classi fondamentali per rappresentare un problema di ricerca:
+ ```Problem```: classe astratta per la definizione di un problema di ricerca
+ ```Node```: classe astratta per la definizione di un nodo nell'albero di ricerca
+ ```PriorityQueue```: implementa una coda con priorità, necessaria per mantenere in memoria i nodi durante l'esecuzione di un algoritmo di ricerca

### ```src/serch.py```
Contiene l'implementazione degli algoritmi di ricerca visti a lezione:
+ ```Ricerca best-first```: algoritmo di ricerca generico, che utilizza una funzione di valutazione per l'espansione dei nodi. Viene utilizzato da tutti gli altri algoritmi, ognuno con una diversa funzione di valutazione
+ ```Ricerca in ampiezza```: utilizza la profondità dei nodi come funzione di valutazione
+ ```Ricerca in profondità```: utilizza l'opposto della profondità dei nodi come funzione di valutazione. Viene implementata anche la versione ricorsiva dell'algoritmo
+ ```Ricerca a profondità limitata```: come la ricerca in profondità ma con un limite, per evitare cicli infiniti. Viene implementata anche la versione ricorsiva dell'algoritmo
+ ```Ricerca a costo uniforme```: utilizza il costo del cammino come funzione di valutazione
+ ```Ricerca A*```: utilizza il costo del cammino e una funzione euristica come funzione di valutazione

### ```src/local_search.py```
Contiene l'implementazione degli algoritmi di ricerca locale visti a lezione:
+ ```Ricerca hill climbing```
+ ```Simulated annealing```

### ```esempi_ricerca.ipynb```
Jupyter Notebook che contiene la definizione di alcuni problemi concreti, *i.e.* ToyProblem, Labirinto di Teseo e Viaggio in Romania, e alcuni esempi di applicazione degli algoritmi di ricerca.

### ```esempi_ricerca_locale.ipynb```
Jupyter Notebook che contiene la definizinoe di problemi di ricerca locali, *i.e* Labirinto di Teseo locale, e alcuni esempi di applicazione degli algoritmi di ricerca locale.
