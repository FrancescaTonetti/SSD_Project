#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 09:49:25 2020

@author: francescatonetti
"""

import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import os, math, sys, io, base64

from keras.models import Sequential
from keras.layers import Dense

def compute_windows(nparray, npast=1):
    dataX, dataY = [], [] # window and value
    for i in range(len(nparray)-npast-1):
        a = nparray[i:(i+npast), 0]
        dataX.append(a)
        dataY.append(nparray[i + npast, 0])
    return np.array(dataX), np.array(dataY)

def predict_func(model, nparray, npred):
    nparray_resh = nparray.reshape((1, len(nparray)))
    forecast_elem = model.predict(nparray_resh, verbose=0)
    nparray = nparray [1:]
    new_nparray = np.append(nparray, [forecast_elem])
    if npred >1:
        return np.append([forecast_elem], [predict_func(model, new_nparray, npred-1)])
    else:
        return forecast_elem


if __name__ == "__main__":
   # cambia working directory to script path
   
   #os.chdir('/Users/francescatonetti/Desktop/Università/2°Anno Magistrale/Sistemi Supporto Decisioni/SSDProject/ProgettoFinanziario/SsdWebApi')
   abspath = os.path.abspath(__file__)
   dname = os.path.dirname(abspath)
   os.chdir(dname)
   
   # stampo info sugli argomenti passati da chi chiama lo script
   print('Arg number:', len(sys.argv)) # Scrive la lunghezza del vettore degli argomenti (argv).
   print('Arg list:', str(sys.argv), ' first arg:',sys.argv[1]) # Scrive la lista degli argomenti seguito dal secondo argomento di argv che sarebbe il file csv (il primo è il file pythos stesso).
   
   dffile = sys.argv[1] # recupero il file che voglio andare a leggere
   df = pd.read_csv("./"+dffile) # leggo il contenuto del file
   dataset = df.values.astype('float32') #estraggo i dati, e indico il tipo: necessario per tensorflow
   
   plt.plot(dataset)
   plt.show()
   
   #print(os.path.splitext("/path/to/some/file.txt")[0])
   
   forecast_size = 240*2 #considero come finestra temporale 2 Anni, composta solo dai giorni lavorativi. <-- finestra di previsione(come se fossero dati che non conosco)
   dataset_base, dataset_forecast = dataset[:-forecast_size], dataset[-forecast_size:]
   log_dataset_base = np.log(dataset_base)
   log_dataset_forecast = np.log(dataset_forecast)
   
   plt.plot(log_dataset_base)
   plt.plot(np.concatenate((np.full(len(log_dataset_base),np.nan), log_dataset_forecast[:,0])))
   plt.show()
   
   """
   Continuo la parte di pre-processing splittando tra train e test set (70%-30%).
   Chiamo la compute window sia sulla parte di training che su quella di test.
   """
   # train - test sets
   cutpoint = int(len(log_dataset_base) * 0.7) # 70% train, 30% test
   train, test = log_dataset_base[:cutpoint], log_dataset_base[cutpoint:]
   print("Len train={0}, len test={1}".format(len(train), len(test)))
   
   """ Chiamo la compute window sia sulla parte di training che su quella di test. """
   # sliding window matrices (npast = window width); dim = n - npast - 1
   npast = 22*2 #considero solo i giorni lavorativi per due mesi consecutivi
   trainX, trainY = compute_windows(train, npast)
   testX, testY = compute_windows(test, npast) # should get also the last npred of train
   
   """
   Successivamente all'apprendimento del modello, ho i miei dati e posso definire il modello neurale che dovrà apprendere sui dati stessi.
   Dico che voglio usare il Precettone Multilivello (MLP).
    
   Con l'struzione add aggiungo un livello al modello, è denso e conterà N hidden neuroni,
   l'ingresso fornirà npast dati.
    
   Ho il livello di ingresso e nascosto, ora aggiugo il livello di uscita ovvero n-output, tutti collegati allo stesso output.
   Ho costruito quindi una rete 3-8-1.
    
   Dovrà apprendere andando a ottimizzare una funzione di LOSS, che è l'errore quadratico medio, ovvero per ciascun esempio calcola l'ouput una volta fornito l'input.
   Azione propagata 
   """
   
   # Multilayer Perceptron model (MLP)
   model = Sequential() #modello di precettore multilivello di Keras - istanzia una rete neurale MLP
   n_hidden = 10
   n_output = 1
   #aggiungo i layer nella mia rete con i valori di input e hidden, mentre relu è la funzione di attivazione lineare
   model.add(Dense(n_hidden, input_dim=npast, activation='relu')) # hidden neurons, 1 layer - Livello denso ovvero completamente connesso
   model.add(Dense(n_output)) # output neurons
   #funzione di attivazione non specificata quindi quella di base ovvero logaritmica
   model.compile(loss='mean_squared_error', optimizer='adam') #funzione da minimizzare + variante back propagation ovvero per minimizzare il valore di min_square_error
   
   #Faccio apprendimento!!!!
   model.fit(trainX, trainY, epochs=200, batch_size=128, verbose=2) # batch_size len(trainX)
   
   model.save('/Users/francescatonetti/Desktop/Università/2°Anno Magistrale/Sistemi Supporto Decisioni/SSDProject/ProgettoFinanziario/SsdWebApi')
   
   from tensorflow import keras
   model = keras.models.load_model('/Users/francescatonetti/Desktop/Università/2°Anno Magistrale/Sistemi Supporto Decisioni/SSDProject/ProgettoFinanziario/SsdWebApi')


   """
   Vediamo quanto ha appreso bene il modello.
   """
   # Model performance: valuta quanto è andato bene il train
   trainScore = model.evaluate(trainX, trainY, verbose=0) #funzione che restituisce train score (MSE) sia sul train che sul test.
   print('Score on train: MSE = {0:0.2f} '.format(trainScore))
   testScore = model.evaluate(testX, testY, verbose=0)
   print('Score on test: MSE = {0:0.2f} '.format(testScore))
    
   #Calcolo sia sui dati di train che test. -> predizione sui dati
   trainPredict = model.predict(trainX) # predictions
   testForecast = model.predict(testX) # forecast(dati che non avevo nei set dei dati di training)
    
   #Visualizzo il grafo conclusivo del modello.
   plt.rcParams["figure.figsize"] = (10,8) # redefines figure size
   plt.plot(np.log(dataset_base))
   plt.plot(np.concatenate((np.full(1,np.nan),trainPredict[:,0])))
   plt.plot(np.concatenate((np.full(len(train)+1,np.nan), testForecast[:,0])))
   plt.show()
   
   #predizione sui dati futuri(che non conosco)
   last_elements = testX[len(testX)-1] #parto dall'ultima finestra/sliding-window del test
   forecast_elements = predict_func(model, last_elements, forecast_size)
   
   plt.plot(np.log(dataset))
   plt.plot(trainPredict)
   plt.plot(np.concatenate((np.full(len(train), np.nan), testForecast[:,0])))
   plt.plot(np.concatenate((np.full(len(dataset_base), np.nan), forecast_elements)))
   plt.show()
   
   #Ricostruzione del dataset a cui ho applicato il preprocessing - procedura inversa, applico exp
   """
   plt.plot(dataset)
   plt.plot(np.exp(trainPredict))
   plt.plot(np.concatenate((np.full(len(train), np.nan), np.exp(testForecast[:,0]))))
   plt.plot(np.concatenate((np.full(len(dataset_base), np.nan), np.exp(forecast_elements[:,0]))))
   plt.show()
   
   plt.plot(np.exp(log_dataset_forecast))
   plt.plot(np.exp(forecast_elements))
   plt.show()
   """

   
   #Applico la funzione di variazioni ai dati che ho previsto (forecast-element)
   
   
   #Applico la funzione del portafoglio al datset
   
   
   
   
   

   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   