# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location.
import os
try:
	os.chdir(os.path.join(os.getcwd(), '2_analise'))
	print(os.getcwd())
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
kickst = kickst[kickst.pledged > 0]
kickst['pledged_ratio'] = kickst['pledged'] / kickst['goal']
#%% [markdown]
# Usar escala logarítmica torna a visualização dos dados mais simples, e coloca acima de 0 os projetos que atingiram a meta, e abaixo de 0 os que não atingiram
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
#%% [markdown]
# Analisando a distribuição, podemos perceber que há uma concentração inicial de projetos com backing de apenas US$1. 
# Após isso, gradualmente cresce e se concentra principalmente entre projetos com aproximadamente US$900 e US$20,000. 
#%%
plt.hist(kickst.log_usd_pledged_real, bins = 12)
#%% [markdown]
# Abaixo 
#%%
plt.hist([kickst[kickst.state == "failed"].log_usd_pledged_real, kickst[kickst.state == "successful"].log_usd_pledged_real], stacked=True, bins = 12)
#%% [markdown]
# No gráfico abaixo, analisamos agora o ratio, vendo a relação entre a meta e o valor arrecadado, e vemos que a distribuição é semelhante ao longo de todo o espectro a partir de US$100.
#%%
plt.scatter(y = 'log_pledged_ratio', x = 'log_usd_goal_real', data=kickst[kickst.state == "successful"], alpha= 0.5)
#%%
