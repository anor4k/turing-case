#%% Change working directory from the workspace root to the ipynb file location.
import os
try:
	os.chdir(os.path.join(os.getcwd(), '3_ia'))
except:
	pass
#%% [markdown]
# # Algoritmo de IA – KNN
# ### Noel Viscome Eliezer
#%%
import pandas as pd
import numpy as np
#%% [markdown]
# Vamos importar e tratar os dados do dataset para a análise. Como a quantidade de amostras é pequena (< 600), iremos usar todas as entradas.
#%%
cancer_data = pd.read_csv('data.csv')
cancer_data = cancer_data.dropna(how='all', axis='columns') #coluna Unnamed com NaN criada por algum motivo? dropamos para garantir a consistência dos dados
#%%
cancer_data.info()
#%%
cancer_data.head()
#%% [markdown]
# Para essa análise, utilizaremos todas as features numéricas do dataset. Queremos prever o diagnóstico (*M*aligno, *B*enigno) através das diversas características descritas.
#%%
X = cancer_data.drop(['id', 'diagnosis'], axis=1) 
y = cancer_data['diagnosis']
#%% [markdown]
# Agora criamos um modelo simples de classificação usando os 5 pontos mais próximos, e usaremos validação cruzada para analisar sua precisão (0.000 a 1.000).
#%%
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors = 5)
from sklearn.model_selection import cross_val_score
scores = cross_val_score(knn, X, y, scoring = 'accuracy', cv = 10)
print("Precisão para cada iteração: ", scores)
print("Média: ", scores.mean())
#%% [markdown]
# Para melhorar o processo anterior, usaremos GridSearch para fazer a validação cruzada com diferentes valores para K. Com isso, podemos escolher o valor ideal de K para obter a melhor precisão para análise.
#%%
from sklearn.model_selection import GridSearchCV
k_range = list(range(1,31))
param_grid = dict(n_neighbors = k_range)
grid = GridSearchCV(knn, param_grid, scoring ='accuracy', cv = 10, return_train_score = False, iid = True)
grid.fit(X, y)
#%% [markdown]
# Vamos plotar em um gráfico os diferentes valores para a média da precisão para cada valor de K.
#%%
import matplotlib.pyplot as plt
grid_mean_scores = grid.cv_results_.get('mean_test_score')
plt.plot(k_range, grid_mean_scores)
plt.xlabel('Número de vizinhos')
plt.ylabel('Cross Validated Accuracy')
#%% [markdown]
# Finalmente, podemos ver abaixo o parâmetro com melhor precisão.
#%%
print(grid.best_params_)
#%%
