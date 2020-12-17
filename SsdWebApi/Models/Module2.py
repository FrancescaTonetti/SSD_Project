#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 11:26:39 2020

@author: francescatonetti
"""

import numpy as np
from sklearn.svm import SVR

"""
Fase di Previsione:
    
"""
def algorithmSvr(dataset_base,dataset_forecast):
   
   """Definisco X e y a partire dai miei dati del dataset_base"""
   y = dataset_base
   X = list(range(len(dataset_base)))
   X = np.array(X).astype('float32')
   
   """Definisco X2 e y2 a partire dai miei dati del dataset_forecast (finestra di previsione)"""
   #nuovo range di indici del forecast --> indici che vanno dalla len del dataset_base alla len del forecast
   y2 = dataset_forecast
   X2 = list(range(len(dataset_base), len(dataset_base)+len(dataset_forecast), 1)) #dall'ultimo indice del dataset_base all'ultimo indice del dataset_ forecast (finestra dei soli dati di forecast)
   X2 = np.array(X2).astype('float32')

   
   X = X.reshape(-1,1)
   X2 = X2.reshape(-1,1)

   """Applico l'algoritmo di regressione SVR solo sui dati del dataset_base sui quali applico la fit."""
   #regressor = SVR(kernel='rbf', C=10000, gamma=0.1, epsilon=.1) --> giocare con i numeri di C e gamma per vedere cosa succede alla curva di previsione
   regressor = SVR(kernel='rbf') #con il default ottengo una curva migliore rispetto all'uso di: C=1000, gamma=0.1, epsilon=.1
   regressor.fit(X,y.ravel()) #FITTO SU TUTTI I MIEI DATI DEL DATABASE_SET

   """Applico la predict su tutti i dati del dataset completo, per cui visualizzo come predice i dati relativamente alla finestra di forecast"""
   #Visualizzo i risultati SVR
   X_grid= np.arange(min(X), max(X2)) #mi consente di creare una curva di predizione con le linee arrotondate
   X_grid = X_grid.reshape((len(X_grid),1)) #apply a new shape into an array without changing the data
   prediction = regressor.predict(X_grid)
   prediction = prediction.astype('float32')
   #prediction = prediction.reshape(-1,1)

   
   return X, y, X2, y2, X_grid, prediction

"""Funzione che mi permette di calcolare un vettore contenente la variazione normalizzata dei valori assunti dal portafoglio"""
def computeVar(valPort):
  variazPort = []
  i = 1
  while i < len(valPort):
     variazPort.append((valPort[i]-valPort[i-1])/valPort[i-1]) 
     i = i+1
  return variazPort
   
