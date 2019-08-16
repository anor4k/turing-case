#%% Change working directory from the workspace root to the ipynb file location.
import os
try:
	os.chdir(os.path.join(os.getcwd(), '3_ia'))
except:
	pass
#%% [markdown]
# # Algoritmo de IA – Regressão Linear
# ### Noel Viscome Eliezer
#%%
import pandas as pd
import numpy as np
#%% [markdown]
# O dataset é um conjunto imenso de dados oceanográficos coletados ao redor do mundo e ao longo do tempo.
# Nessa análise, iremos apenas buscar uma relação entre a temperatura da água e a salinidade.
# Como o dataset inteiro consiste de mais de 800.000 entradas, iremos usar uma amostra de 20.000 entradas para facilitar o processamento e a visualização.
#%%
full_bottle = pd.read_csv('bottle.csv')
bottle = full_bottle.sample(20000)
#%% [markdown]
# Primeiramente, separamos as colunas que interessam para a análise, que são a temperatura e a salinidade. A temperatura será tratada como _feature_, e a salinidade como _target_.
#%%
temp = bottle.loc[:, ['T_degC']]
salt = bottle.loc[:, ['Salnty']] 
#%% [markdown]
# Precisamos lidar com os dados faltantes para realizar a regressão. Neste caso, vamos preencher os dados faltantes com a média da amostra.
#%%
temp = temp.fillna(temp.mean())
salt = salt.fillna(salt.mean())
#%% [markdown]
# Dividimos a amostra entre um grupo de treino (70% da amostra), que será usado para o treino (_fitting_) do algoritmo, e um grupo de teste (30% da amostra), que será usado para fins de análise do erro do modelo.
#%%
from sklearn.model_selection import train_test_split
temp_train, temp_test, salt_train, salt_test = train_test_split(temp, salt, test_size = 0.3)
#%% [markdown]
# Agora efetivamente criamos e treinamos o regressor com as amostras de treino.
# %%
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(temp_train, salt_train)
#%% [markdown]
# Agora que temos nosso regressor treinado, vamos visualizar os dados em um _scatter plot_:
# Os pontos em azul são os pontos reais, usados pra treinar o regressor; os pontos em verde representam os pontos estimados pelo regressor já treinado.
# Um detalhe a ser percebido é que os pontos em azul que formam uma reta horizontal perfeita logo abaixo de 34 representam (geralmente) os pontos que foram preenchidos com a média anteriormente.
#%%
import matplotlib.pyplot as plt
plt.figure(figsize=(12,10))
plt.scatter(x = temp_train, y = salt_train, c = 'b', s=40, alpha = 0.5)
plt.scatter(x = temp_test, y = regressor.predict(temp_test), c = 'g', s = 40)
plt.ylabel("Salinity")
plt.xlabel("Temperature (°C)")
plt.show()
#%% [markdown]
# Calculamos também o score r<sup>2</sup> para analisar a variância do modelo em relação ao dataset.
#%%
regressor.score(temp_test, salt_test)
#%% [markdown]
# O valor de cerca de aproximadamente 25% (sendo 100% o melhor valor possível, indicando perfeita paridade entre o modelo e os dados) de r<sup>2</sup> é um indicador da grande variância dos dados utilizados para a definição do regressor.
# 
#%% [markdown]
# Finalmente, utilizamos validação cruzada para determinar o erro quadrado médio negativo entre uma série de 5 validações com a amostra original.
#%%
from sklearn.model_selection import cross_val_score
scores = cross_val_score(regressor, temp, salt, cv=5, scoring='neg_mean_squared_error')
print(scores)

#%% [markdown]
# A partir das informações obtidas, obtemos também o coeficiente angular da reta e seu ponto de intersecção:
print(f'Coeficiente angular = {float(regressor.coef_):.2f}')
print(f'Intersecção = {float(regressor.intercept_):.2f}')

#%% [markdown]
# Finalmente, a conclusão principal da análise é: embora estejam relacionados, a salinidade da água e a temperatura da água são significativamente afetadas também por outros fatores. A enorme variância observada é o principal indicador disso.

#%%
