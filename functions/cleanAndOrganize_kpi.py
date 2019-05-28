import pandas as pd
import numpy as np


# Function : cleaning and organizing score's data
# Output : - average     : moyenne des 8 features
#          - dataset1    : score of questions
#          - reference   : reference entreprise + TOP/FLOP 10 
#          - dataset2    : Information on teams
#          - dataset     : dataset1 + dataset2
#          - features    : names of features
def cleaningAndOrganise_scores(dataset):

  ''' Read the file csv '''
  #path = '/Users/user/Desktop/Memoire/Partie technique/Data and Code/Data/usefull/'
  #image = '/Users/user/Desktop/Memoire/Partie technique/Data and Code/Plots/'
  
  ''' Organisation of data '''
  features = list(dataset.columns.values)
  
  #newCol = ['charges et équilibre','developement personel','relation dans équipe', 'avis sur l employeur']
  
  ref = dataset.iloc[0:4,:].values
  dataset = dataset.iloc[4:558,:].values
  
  data1 = dataset[:,5:9]/10000 # Average score : Stress, Engagement, Satisfaction, Loyauté
  data2 = dataset[:,:5]        # Information on Team
  data  = dataset[:,9:108]     # Score by question
  
  
  
  ''' Cleaning Data '''
  taille_tab_to_clean = 99
  for i in range(0,taille_tab_to_clean) : 
    data[:,i] = zeroToAverage(data,i,0)   #Replace value 0.0 by average of column
  #score_moyen = data[:,0:4]
  
  
  
  ''' Creation of new average '''
  l,c = data.shape
  length = l*4
  new_average = np.arange(length).reshape(l,4)
  for j in range(0,l):
    new_average[j,0] = meandata(data[j,31:43])
    new_average[j,1] = meandata(data[j,43:50])
    new_average[j,2] = meandata(data[j,50:65])
    new_average[j,3] = meandata(data[j,65:99]) #34 variables
  new_average = new_average/10000
  
  
  
  ''' Creation of DataFrames '''
  new_moyenne = pd.DataFrame(new_average)
  dataset1 = pd.DataFrame(data=data)         # Score by question
  dataset2 = pd.DataFrame(data=data2)        # Information on Team
  score_average = pd.DataFrame(data=data1)   # Average score : Stress, Engagement, Satisfaction, Loyauté
  reference = pd.DataFrame(data=ref)         # Reference Bpost and TOP/FLOP 10
  
  frames = [dataset2, dataset1]
  dataset = pd.concat(frames, axis = 1)
   
  # Average score : Stress, Engagement, Satisfaction, Loyauté, Charges, dev perso, équipe, avis
  average = pd.concat([score_average, new_moyenne], axis=1)
  average = average.astype('float')
  average = round(average,2)
  average.columns =  ['Index stress moyen','Index engagement moyen',' Index loyauté moyen', ' Index statifaction moyen','charges et équilibre','developement personel','relation dans équipe', 'avis sur l employeur']
  

  return average, dataset1, reference, dataset2, dataset, features



# Function : Raplace value = 'crit' by average of column 
# Input : - data 
#         - indice of column to clean (m)
# Output : Column cleaned
def zeroToAverage(data,m,crit):
  #Initialisation
  T = 0
  Sum = 0
  x = []
  l,c = data.shape

  for i in range(0,l) :
    if data[i,m] != crit :
      Sum += data[1,m] 
      T += 1
    elif data[i,m] == crit :
      x.append(i)
    
  Average = Sum/T
 
  #if len(x)==0: print('Aucune valeur à cleaner')
  for j in range(0,len(x)) :
    #print('indice : (', x[j], ',', m, ') a comme valeur : ', data[x[j],m], '. Cette valeur est remplacé par ', Average)
    data[x[j],m] = Average

  return data[:,m]



# Function : average  
# Input :  - data (list)
# Output : - average of a list
def meandata(X):
  somme = 0
  count = 0
  for i in range(0,len(X)):
    somme = somme + X[i]
    count = count+1
  return somme/count



# Function : Clean Data file 
# Input :  - dataset kpi
# Output : - X : data
#          - Y : absenteisme
#          - features 
#          - locations : adresse GPS
def cleanAndOrganize_kpi(kpi):
  
  ''' Organisation of data '''
  features = list(kpi.columns.values)
  locations = list(kpi.iloc[:,0].values)
  
  Y = kpi.iloc[:,1:16].values
  #X[:,1] = X[:,1]/10000 
  Y = pd.DataFrame(data=Y)
  Y = Y.fillna(0)
  Y.columns = features[1:16]

  X = kpi.iloc[:,16:24].values
  X = pd.DataFrame(data=X)
  X.columns = features[16:24]
  
  return X,Y,features,locations



# Function : divide score by 100 
# Input :  - dataset 
# Output : - new dataset with correct scores
def orgadata(dataset7):
  features = list(dataset7.columns.values)
  var = pd.DataFrame(dataset7.iloc[:,0].values)
  data = dataset7.iloc[:,1:].values /100
  data = pd.DataFrame(data)
  dataset = pd.concat([var, data], axis=1)
  dataset.columns = features
  
  return dataset

