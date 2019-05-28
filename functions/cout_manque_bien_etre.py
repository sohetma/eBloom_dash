# -*- coding: utf-8 -*-
"""
Created on Sun May 19 11:39:03 2019

@author: Sohet Maxime
"""

import pandas
from statistics import mean 

def cout_manque_bien_etre(data , taille_entreprise, priority=0, pourcentage=0.1, salaire_moyen = 45000):
  names = list(data.columns.values)
  sorted_data = data.sort_values(by = names[priority])
  l,c = sorted_data.shape
  dim_flop = int(pourcentage*l)
  dim2 = l - dim_flop
  
  mean_flop = mean(sorted_data.iloc[0:dim_flop,c-1].values)
  mean_top = mean(sorted_data.iloc[dim2:l,c-1].values)
  
  perc_absenteisme = mean_top - mean_flop
  cout = perc_absenteisme*salaire_moyen*taille_entreprise
  cout = round(cout,2)
  
  text = '{}{}{}'.format('Le cout du manque en Bien-être est estimé en coût direct à ', cout, ' €.')
  #print(text)
  
  return cout