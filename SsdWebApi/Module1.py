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


if __name__ == "__main__":
    
   files = ["All_Bonds.csv", "FTSE_MIB.csv", "GOLD_SPOT.csv", "MSCI_EM.csv", "MSCI_EURO.csv", "SP_500.csv", "US_Treasury.csv"]
   allForecastPrediction = []
   allForecastVariance = []
   
   """cambia working directory to script path"""
   abspath = os.path.abspath(__file__)
   dname = os.path.dirname(abspath)
   os.chdir(dname)
   
   
   """!! QUI rimettere il codice !!! + elimina riga 37"""
   variaz = pd.read_csv("./variations.csv") 
       
   
   #codice da togliere
   allForecastVariance = []
   variaz = variaz.to_numpy()
   variaz = variaz.transpose()
   for v in variaz:
       allForecastVariance.append(v) 
       
       
   #Al PSO passerò una lista che costituisce per ogni indice la lista di valori del forecast ai quali ho applicato il calcolo della variazione
   res_xsolbest = PSO.takeDataSet(allForecastVariance)


   import json
   data = {}
   data['horizont'] = 6
   for f in range(len(files)):
       data[files[f][:-4]] = res_xsolbest[f]
   with open("data_file.json", "w") as write_file:
    json.dump(data, write_file)
   r = open("data_file.json")
   print(r.readlines())

   
   
   
   
   
   
   
   
   
   