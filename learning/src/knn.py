import heapq

from utils import mode

class NearestNeighborLearner:
    '''
    Implementazione dell'algoritmo k-NearestNeighbor.
    In input richiede:
    dataset: oggetto della classe DataSet
             contiene gli esempi per il training e le funzioni per la gestione del data set
    k: numero di vicini da considerare
    '''

    def __init__(self, dataset, k=1):
        self.dataset = dataset
        self.k = k

    def predict(self, example):
        '''
        Cerca i k elementi più vicini all'esempio in input.
        Utilizza un voto di maggioranza sull'output.
        '''

        # heapq.nsmallest restituisce una lista degli n elementi più vicini all'esempio in input.
        # viene utilizzata una funzione di distanza, che di default è la distanza euclidea.
        best = heapq.nsmallest(self.k, ((self.dataset.distance(e, example), e) for e in self.dataset.examples))

        # mode restituisce il valore di target maggiormente presente tra i vicini
        return mode(e[self.dataset.target] for (d, e) in best)