#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 10:49:52 2020

@author: francescatonetti
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 09:49:25 2020

@author: francescatonetti
"""

import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import os, sys

import Module2
import PSO

"""
Introduciamo i passi relativi alla previsione della mia serie storica.

Procedo attraverso una Previsione UNIVARIATA ovvero usufruisco dei dati passati della stessa serie storica per predire quelli futuri. 
(NON uso variabili esterne/esogene)
Nello specifico, partendo dalle serie storiche degli indici di borsa, voglio visualizzare dei pattern (o comportamenti) 
sui dati del passato, per prevedere il futuro.

Obiettivo: Voglio ottenere un portafoglio azionario in modo da massimizzare nel futuro il redimento del capitale investito,
conoscendo il comportamento degli indici di borsa nel passato.
"""


if __name__ == "__main__":
   
   files = ["All_Bonds.csv", "FTSE_MIB.csv", "GOLD_SPOT.csv", "MSCI_EM.csv", "MSCI_EURO.csv", "SP_500.csv", "US_Treasury.csv"]
   
   """Inizializzo due liste vuote che userò al termine della previsione"""
   allForecastPrediction = []
   allForecastVariance = []
   
   """Cambio la directory di lavoro (script path)"""
   abspath = os.path.abspath(__file__)
   dname = os.path.dirname(abspath)
   os.chdir(dname)
   
   """Ciclicamente estraggo un file csv, relativo ad un indice specifico di borsa, e inserisco i valori in un array"""
   for dffile in files:
       df = pd.read_csv("../"+dffile) # leggo il contenuto del file
       dataset = df.values.astype('float32') #estraggo i dati, e indico il tipo (necessario per tensorflow) -- array
       
       
       """Uso la funzione plot() per visualizzare in un grafo bidimensionale (x: tempo, y:valori) la serie storica di interesse"""
       #plt.plot(dataset) #visualizzo tutto il mio dataset (intera serie storica di dati)
       #plt.show()
       
       """
       Fase di pre-processing:
       Standardizzo il set di dati affiché l'algoritmo di apprendimento ne tragga massimo vantaggio.
       Porto la mia distribuzione di dati ad avere media zero e varianza unitaria --> chiamando il modulo StandardScaler()
       """
       from sklearn.preprocessing import StandardScaler
       sc_dataset = StandardScaler() #applico la standardizzazione dei dati su tutto il dataset
       #fit: calcolo la media e l'std da utilizzare per il ridimensionamento e nello stesso momento applico latrasformazione sui dati.
       dataset = sc_dataset.fit_transform(dataset.reshape(-1,1)) #fornisco all'array una nuova forma ovvero 2 dimensioni senza modificare i dati.
       
       """Scelgo il valore migliore per la mia finestra di forecast e, 
       a partire dal dataset di base tolgo l'ultima parte di dati che vorrò prevedere
       """
       forecast_size = 120 #6mesi(120), composto solo dai giorni lavorativi
       dataset_base, dataset_forecast = dataset[:-forecast_size], dataset[-forecast_size:]
       
       """Visualizzo la nuova serie storica distinguendo tra i dati del dataset di base e quelli di forecast"""
       #plt.plot(dataset_base)
       #plt.plot(np.concatenate((np.full(len(dataset_base),np.nan), dataset_forecast[:,0])))
       #plt.show()
   
       """
       Fase di previsione del dataset:
       Chiamo il Modulo2 python per fare l'addestramento e previsione sui dati con algoritmo SVR"""
       X, y, X2, y2, X_grid, prediction = Module2.algorithmSvr(dataset_base, dataset_forecast)
   
       """Visualizzo l'intera serie storica distinguendo i dati di base rispetto quelli di forecast
       Questa volta utilizzando il modulo scatter che, a differenza del plot, 
       disegna la serie attraverso dei puntini nel grafo bidimensionale, senza linee che li colleghino
       """
       #plt.scatter(X, y, s=1, color='blue')
       #plt.scatter(X2, y2, s=1, color='red')
       #plt.show()
   
       """Visualizzo il grafo precedente al quale aggiungo il valore di predizione resitutito dall'algoritmo SVR, 
       come linea continua su tutto il dataset
       """
       #plt.scatter(X, y, s=1, color='blue')
       #plt.scatter(X2, y2, s=1, color='red')
       #plt.plot(X_grid, prediction, color='orange')
       #plt.show()
    
       dataset = sc_dataset.inverse_transform(dataset) #Annullo il ridimensionamento del mio dataset.
       prediction = sc_dataset.inverse_transform(prediction) #Annullo il ridimensionamento sui dati predetti.
       #plt.plot(dataset)
       #plt.plot(prediction)
       #plt.show()
       
       """Calcolo i soli valori predetti relativi ai dati di forecast (finestra di previsione)"""
       predictForecast = prediction[-forecast_size:]

       """Creo una lista che contenta per ciascun indice di borsa i soli valori di previsione"""
       allForecastPrediction.append(predictForecast)
    
       
   """Al termine del processo di previsione, a partire dalla mia lista di valori di previsione (per ciascun indice di borsa),
   applico il calcolo per la variazione del valore del portafoglio.
   """
   for forecast in allForecastPrediction:
       predictForecastVariance = Module2.computeVar(forecast) #applico la varianza su ogni dataset della mia lista, uno alla volta
       allForecastVariance.append(predictForecastVariance)  
       
   """Fase di ottimizzazione: chiamo il modulo PSO"""    
   #Al PSO passerò una lista che costituisce per ogni indice la lista di valori del forecast ai quali ho applicato il calcolo della variazione
   res_xsolbest = PSO.takeDataSet(allForecastVariance)

   """Restituisco un file json contenente il portafoglio ottimo calcolato"""
   import json
   data = {}
   data['horizont'] = 6
   for f in range(len(files)):
       data[files[f][:-4]] = res_xsolbest[f]
   with open("bestPortafoglio.json", "w") as write_file:
    json.dump(data, write_file)
   print(data)

   
   
   
   
   
   
   
   
   
   