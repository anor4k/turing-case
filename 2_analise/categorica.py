#%% Change working directory from the workspace root to the ipynb file location.
import os
try:
	os.chdir(os.path.join(os.getcwd(), '2_analise'))
except:
	pass
#%% [markdown]
# # Análise de Dados
# ## Projetos do Kickstarter
# ### Noel Viscome Eliezer
# 
# Dataset: https://www.kaggle.com/kemical/kickstarter-projects
# 
#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

#%%
kickst = pd.read_csv('ks-projects-201801.csv', parse_dates=['deadline', 'launched'])
kickst = kickst[(kickst.pledged > 0) & (kickst.backers > 0)]
kickst['pledged_ratio'] = kickst['pledged'] / kickst['goal']
#%% [markdown]
# Utilizaremos a escala logarítmica para analisar os dados de maneira mais compreensiva, visto que temos projetos desde a casa das dezenas até milhares de dólares.
#%%
kickst['log_pledged_ratio'] = np.log10(kickst['pledged_ratio'])
kickst['log_usd_pledged_real'] = np.log10(kickst['usd_pledged_real'])
kickst['log_usd_goal_real'] = np.log10(kickst['usd_goal_real'])
kickst['log_backers'] = np.log10(kickst['backers'])
kickst = kickst.sample(10000)
#%%
kickst.info()
#%%
kickst.describe()
#%%
kickst.head()
#%% [markdown]
# A primeira feature categórica que é interessante de ser analisada é a divisão por categorias. Primeiro vamos observar a quantidade de projetos por categoria principal:
#%%
sns.countplot(y = 'main_category', order = kickst['main_category'].value_counts().index, data = kickst)
#%% [markdown]
# O gráfico abaixo, por outro lado, estima o valor médio de cada projeto por categoria (em escala logarítmica), e percebemos que é majoritariamente uniforme. 
#%%
sns.barplot(x = 'log_usd_pledged_real', y = 'main_category', data = kickst, order = kickst['main_category'].value_counts().index)
#%% [markdown]
# Já no gráfico abaixo comparamos a quantidade de projetos bem sucedidos e cancelados ou que falharam. Há também projetos em andamento, suspensos ou sem categoria, mas não foram inclusos devido à pouca representatividade.
#%%
plt.figure(figsize= (10, 8))
sns.countplot(y = 'state', hue = kickst['main_category'], hue_order = kickst['main_category'].value_counts().index, data = kickst[(kickst.state == 'successful') | (kickst.state == 'failed') | (kickst.state == 'canceled')])
plt.show()

#%% [markdown]
# Os gráficos abaixo mostram a média de arrecadação em relação à meta para cada categoria quando todos os projetos são inclusos, e apenas quando incluímos os projetos bem-sucedidos.
#%%
sns.barplot(x = 'log_pledged_ratio', y = 'main_category', data = kickst, order = kickst['main_category'].value_counts().index)
#%%
sns.barplot(x = 'log_pledged_ratio', y = 'main_category', data = kickst[kickst.state == "successful"], order = kickst['main_category'].value_counts().index)
#%%