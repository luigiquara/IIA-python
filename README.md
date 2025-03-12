# IIA-python
Algoritmi e applicazioni di IA relative al corso "Introduzione all'Intelligenza Artificiale", Corso di Laurea in Informatica, Università di Pisa.

Contiene due sezioni principali: 
* Implementazione di algoritmi di ricerca globale e locale, aggiornata alla quarta edizione dell'AIMA, con esempi di utilizzo su problemi concreti;
* Implementazione di algoritmi di apprendimento automatico, con esempi di utilizzo su problemi concreti

## Struttura

Il repository è strutturato come segue:

```
.
├── search/  
│   ├── src/  
│   │   ├── utils.py                  # Classi di supporto per nodi e problemi
│   │   ├── search.py                 # Implementazione degli algoritmi di ricerca
│   │   ├── local_search.py           # Implementazione degli algoritmi di ricerca locale
│   ├── esempi_ricerca.ipynb          # Notebook con esempi di utilizzo degli algoritmi di ricerca
|   ├── esempi_ricerca_locale.ipynb   # Notebook con esempi di utilizzo degli algoritmi di ricerca locale
│  
├── learning/  
│   ├── datasets/                     # Dataset per l'addestramento e la valutazione dei modelli  
│   ├── src/  
│   │   ├── utils.py                  # Funzioni di supporto
│   │   ├── learning.py               # Implementazione di dataset, cross-validation e funzioni di valutazione
│   │   ├── linear_model.py           # Implementazione del modello lineare
│   ├── esempi_modello_lineare.ipynb  # Notebook con esempi di utilizzo del modello lineare
│  
├── README.md                         # Questo file

```

Per informazioni aggiuntive riguardo al contenuto delle singole sezioni, fare riferimento ai file README.md presenti in ```search``` e ```learning```.
