#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 18:28:29 2020

@author: francescatonetti
"""

import numpy as np
import random as rnd
import math as mt

#Funzione chiamata dal mio Modulo1
def takeDataSet(dataset):
    num_iter = 100 #1000 o prova con 100 e 30
    pop_size = 30
    nhood_size = 10
   
    return goPSO(num_iter, pop_size, nhood_size, dataset) #chiamo la funzione goPSO
    
def goPSO(num_iter, pop_size, nhood_size, dataset):
    res = np.inf
    
    dimensioni = 7 #dimensioni --> 7 indici a disposizione
    #punti dello spazio di ricerca, ogni punto nello spazio è una possibile config del portafoglio
    xmin = 5 #5 (0.05)
    xmax = 100 #100 (1)
    
    capitale = 100000
        
    #Run PSO algorithm
    PSO = ParSwarmOpt(xmin, xmax, capitale, dataset)
    res = PSO.pso_solve(pop_size, dimensioni, num_iter, nhood_size)
    return res; #risultato di ritorno del mio PSO messo in funzione <<-- risultato di ritorno al modulo1
    


# restituisce un vettore contenente i valori di media mobile assunti dal portafoglio nel tempo
def computeMovingAverage(values,nval):
    medie = []
    i = 0
    while (i+nval) <= len(values):
        medie.append(sum(values[i:(i+nval)])/nval) 
        i = i+1
    return medie

# restituisce un vettore contenente il valore day by day del portfolio per uno specifico indice
def computeIndexPortfolioValueDayByDay(capitale, indexData):
    res = [capitale]
    for i in range(1, len(indexData)):
        res.append((1+indexData[i])*res[i-1])
    return res


#Funzione che calcola la variazione del portafoglio
def funVariazionePortafoglio(portafoglio):
    variazionePortafoglio = []
    for i in range(1, len(portafoglio)):
        variazionePortafoglio.append((portafoglio[i].sum()-portafoglio[i-1].sum())/portafoglio[i-1].sum())
    return variazionePortafoglio


#funzione che calcola il valore del portafoglio       
def funValorePortafoglio(portafoglio):
    valorePortafoglio = []
    for i in range(len(portafoglio)):
        valorePortafoglio.append(portafoglio[i].sum()) #sommo tutti gli elementi di ciascuna riga
    return valorePortafoglio


#funzione che calcola la Return del portafoglio   
def funReturn(valorePortafoglio):
    month = 20
    return sum(valorePortafoglio[-month:])/month


#Funzione che calcola il valore di rischio del portafoglio
def funRisk(valorePortafoglio):
    value = [] #colonna AB
    sqError = []
    for i in range(20, len(valorePortafoglio)+1):
        value.append(sum(valorePortafoglio[i-20 : i])/20)
    for v in range(20, len(value)+20):
        sqError.append(pow(valorePortafoglio[v-1]-value[v-20],2))
    stdev = mt.sqrt(sum(sqError)/len(sqError))
    return stdev
        
#Calcolo della funzione obiettivo    
def funObiettivo(ret, risk):
    alfa = rnd.uniform(0, 1)
    return alfa*ret - (1-alfa)*risk #alfa*ret + (1-alfa)*rischio


def compute_fitness(pop, capitale, dataset):
    #return paraboloid(pos);
    calcoloCapitali = []
    
    portafoglio = [] #lista di valori nuovi
    variazionePortafoglio = []
    valorePortafoglio = []
    
    #calcolo il valore del capitale per ciascun dataset
    for p in pop:
        calcoloCapitali.append(p * capitale)
    
    #ora mi devo calcolare il nuovo portafoglio chiamando la computeIndexPortfolioValueDayByDay
    #il mio nuovo array di array avrà come prima riga tutti i valori del calcolo del capitale
    for i in range(len(dataset)):
        portafoglio.append(computeIndexPortfolioValueDayByDay(calcoloCapitali[i], dataset[i])) #ritorno un array di array
    
    portafoglio = np.array(portafoglio)
    portafoglio = portafoglio.transpose() #ho invertito la matrice!!!
    
    #Calcolo la variazione del portafolgio(considero di essere riuscita ad ottenere una matrice capovolta nel modo giusto)
    # z = np.array(allForecastVariance)
    variazionePortafoglio = funVariazionePortafoglio(portafoglio)
    
    #Calcolo il valore del portafoglio
    valorePortafoglio = funValorePortafoglio(portafoglio)

    #Calcolo il valore di _return come la media del valore del portafoglio dell'ultimo mese ovvero ultimi 20gg.
    ret = funReturn(valorePortafoglio)
    
    #Calcolo il valore del rischio risk come deviazione standard!!!
    risk = funRisk(valorePortafoglio)
    #print("return:{0} e rischio:{1}".format(ret, risk))
    
    #Applico la funzione obiettivo i cui pesi scelgo che sia l'utente a modificarli in base a quanto rischio vogliono applicare
    return funObiettivo(ret, risk)
    
def calculatePop(pop, newPop, xmin, xmax, dimension):
    dimension = dimension-1
    size = len(newPop)
    sumPop = sum(newPop) #sommo le nuove posizioni
    newSumPop = (xmax/100) - sumPop - ((dimension-size)* (xmin/100)) #sottraggo al mio valore massimo
    pop = rnd.uniform((xmin/100), newSumPop)
    newPop.append(pop)
    return pop  


"""Ha la propria posizione, il personal best (pbest), e una velocità"""
class Particle:
    def __init__(self, _ndim, _nhood_size):
        self.fit = self.fitnbest = self.gbest = 0
        self.v = np.zeros(_ndim, dtype=np.float)
        self.x = np.zeros(_ndim, dtype=np.float)
        self.pbest = np.zeros(_ndim, dtype=np.float)
        self.lbest = np.zeros(_ndim, dtype=np.float) #npbest è il localBest dei neighborhood
        self.nset = np.zeros(_nhood_size, dtype=np.int)
        
class ParSwarmOpt:
    
    """PSO"""
    def __init__(self, _xmin, _xmax, capitale, dataset):
        self.c0 = 0.25 #coefficiente di velocità
        self.c1 = 1.5
        self.c2 = 2.0
        self.gbest = -(np.inf)
        self.xmin = _xmin
        self.xmax = _xmax
        self.capitale = capitale
        self.dataset = dataset
        self.xsolbest = np.zeros(7, dtype=np.float) #passare alla init la dimensione
    
    def pso_solve(self, pop_size, dimension, num_iter, nhood_size):
        rnd.seed(550)
        
        #inizializzo 
        pop = []
        newPop = []
        
        for i in range(pop_size):
            p = Particle(dimension, nhood_size) #genero la popolazione iniziale
            pop.append(p)
            
        for i in range(pop_size):
            #inizializzo posizione e velocità (casuale)
            for j in range(dimension):
                pop[i].x[j] = calculatePop(pop[i].x[j], newPop, self.xmin, self.xmax, dimension)
                pop[i].v[j] = (rnd.random()-rnd.random()) * 0.5 * ((self.xmax/100)-(self.xmin/100))-(self.xmin/100)     
            
            #posizione delle particelle, configurazione inizale del portafoglio
            #pop[i].x = np.array([0.05, 0.05, 0.2, 0.1, 0.05, 0.3, 0.25]) #Da cancellare!!!!!!!!!!!!!!!!!!! perchè inizialmente ho posizioni randomiche ma la cui somma è 1
            
            #pop[i].x /= pop[i].x.sum() #faccio in modo che il risultato delle posizioni ovvero del portafoglio sia 1 al massimo.
            pop[i].pbest = pop[i].x
            pop[i].lbest = pop[i].x
            
            #inizializzo le fitness
            pop[i].fit = compute_fitness(pop[i].x, self.capitale, self.dataset)
            pop[i].gbest = pop[i].fit
            
            #inizializzo i figli(neighbothood) inserendo casualmente gli altri elementi
            for j in range(nhood_size):
                id=rnd.randrange(pop_size)
                while(id in pop[i].nset):
                    id = rnd.randrange(pop_size)
                else:
                    pop[i].nset[j] = id;
            newPop = []        
                    
        #mando il ciclo ripetuto num_iter volte
        for iter in range(num_iter):
            #print("iter{0} zub {1}".format(iter, self.gbest))
            #Aggiorno le particelle
            for i in range(pop_size):
                #per ciascuna dimensione
                for d in range(dimension):
                    #coefficienti stocastici
                    rho1 = self.c1 * rnd.random()
                    rho2 = self.c2 * rnd.random()
                    #aggiorno le velocità
                    pop[i].v[d] = self.c0 * pop[i].v[d] +\
                      rho1 * (pop[i].pbest[d] - pop[i].x[d]) +\
                      rho2 * (pop[i].lbest[d] - pop[i].x[d])
                    #aggiorno le posizioni
                    pop[i].x[d] += pop[i].v[d]
                    
                    #chiamo la funzione
                    pop[i].x[d] = calculatePop(pop[i].x[d], newPop, self.xmin, self.xmax, dimension)
                    #pop[i].v[d] += pop[i].v[d]; --> += o = - ? come cambia la sua velocità?
                    
                
                #Aggiorno la fitness delle particelle
                pop[i].fit = compute_fitness(pop[i].x, self.capitale, self.dataset)
                
                #Aggiorno la personal best posizion, min
                if (pop[i].fit < pop[i].gbest):
                    pop[i].gbest = pop[i].fit
                    for j in range(dimension):
                        pop[i].pbest[j] = pop[i].x[j]
                         
                #Aggiorno la best dei neighborhood
                pop[i].fitnbest = np.inf
                for j in range(nhood_size):
                    if(pop[pop[i].nset[j]].fit < pop[i].fitnbest):
                        pop[i].fitnbest = pop[pop[i].nset[j]].fit
                        #copio le particelle pos sul vettore gbest
                        for k in range(dimension):
                            pop[i].lbest[k] = pop[pop[i].nset[j]].x[k]
                           
                #Aggiorno il gbest
                if(pop[i].fit > self.gbest):
                    #aggiorno la best fitness
                    self.gbest = pop[i].fit
                    #copio la posizione della particelle al vettore gbest
                    for j in range(dimension):
                        self.xsolbest[j] = pop[i].x[j]
            newPop = [] 
                        
        #Ritorno il risultato
        return self.xsolbest;
            
            
            
            
            
            
            
            
            
            
            
            
            
            