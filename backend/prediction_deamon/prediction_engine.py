import keras
from os import listdir
from os.path import isfile, join
from keras.models import load_model
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
import pandas as pd
import numpy as np


class Prediction_Engine:
  
  
  def __init__(self, nb_models_to_loads):
    self.path_to_models = './prediction_deamon/ML_models/'
    self.files_list = self.get_files_list()
    self.model_list = self.get_model_list()
    self.files_of_models = self.get_files_of_model()
    self.genes_of_models = self.get_gen_list_per_model()
    
    df = pd.read_csv('./prediction_deamon/X_columns.csv')
    self.genes_index = df['x'].tolist()
  
    self.loaded_models = self.load_models(nb_models_to_loads)

    
    
  def load_models(self, nb_models_to_loads):
    #nb_models = len(self.files_of_models)
    loaded_models = {}
    for m in self.model_list:
      if len(loaded_models) == nb_models_to_loads:
        break
      if m in self.files_of_models.keys():
        print('Loading model...' + str(len(loaded_models) + 1) + '/' + str(nb_models_to_loads), '(' + m + ')', flush=True)
        model = load_model(self.path_to_models + self.files_of_models[m])
        loaded_models[m] = model
    print('Model loading done!', flush=True)
    return loaded_models


  def get_files_list(self):
    model_list = [f for f in listdir(self.path_to_models) if isfile(join(self.path_to_models, f))]
    clean_model_list = []
    for m in model_list:
      if 'ALL' not in m:
        clean_model_list.append(m)
    return clean_model_list
  
  
  def get_model_list(self):  
    unique_model_list = []
    for m in self.files_list:
      model_name = m.split('_')[0]
      if model_name not in unique_model_list:
        unique_model_list.append(model_name)
    return unique_model_list
  
  
  def get_files_of_model(self):
    file_of_model = {}
    for m in self.model_list:
      mfl = []
      for f in self.files_list:
        if f.split('_')[0] == m and '.h5' in f and 'Survival' in f and '_Transfer_':
          mfl.append(f)
      if len(mfl) > 0:
        f = mfl[-1]
        file_of_model[m] = f
    return file_of_model


  def get_gen_list_per_model(self):
    gen_of_model = {}
    for m in self.model_list:
      if m in self.files_of_models.keys():
        f = self.files_of_models[m]
        fdata = f[0:-3] + '.Rdata'
        pandas2ri.activate()
        base = importr('base')
        base.load(self.path_to_models + fdata)
        rdf = base.mget(base.ls())
        gen_list = rdf[0][-1]
        gen_of_model[m] = gen_list
    return gen_of_model         
  
  
  def predict_all_models(self, X):
    all_pred = []
    
    model_id = 0
    for m in self.loaded_models.keys():
      
      if type(X) is pd.core.frame.DataFrame: # if Salmon input
        selected_TPM = []
        for g in self.genes_of_models[m]:
          selected_TPM.append(X[g]['TPM'])
        selected_TPM = np.array(selected_TPM).reshape((1, len(selected_TPM)))
        all_pred.append(self.loaded_models[m].predict(selected_TPM))
        
    
      elif type(X) is np.ndarray:  # if numpy input
        index_of_genes_in_X = []
        for g in self.genes_of_models[m]:
          i = self.genes_index.index(g)
          index_of_genes_in_X.append(i)
        sub_X = X[:, index_of_genes_in_X]
        all_pred.append(self.loaded_models[m].predict(sub_X))
    
    all_pred = np.array(all_pred)
      
    return all_pred


  def predict_with_mean(self, X):
    return np.mean(self.predict_all_models(X), axis=0)
  
  
  def predict_with_median(self, X):
    return np.median(self.predict_all_models(X), axis=0)
  
  
  def predict(self, X):
    #return self.predict_with_mean(X)
    return self.predict_with_median(X)

    

