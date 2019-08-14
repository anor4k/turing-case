# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), '2_analise'))
	print(os.getcwd())
except:
	pass
#%% [markdown]
# # Grupo Turing - Processo Seletivo 2019.2
# ## Exemplo de Análise de Dados - Red Wine Quality
# Dataset: https://www.kaggle.com/uciml/red-wine-quality-cortez-et-al-2009
# 
# Descrição do dataset (retirada do link acima):
# 
# > - **fixed acidity:**
#     most acids involved with wine or fixed or nonvolatile (do not evaporate readily)
# >
# > - **volatile acidity:**
#     the amount of acetic acid in wine, which at too high of levels can
#     lead to an unpleasant, vinegar taste
# >
# > - **citric acid:**
#     found in small quantities, citric acid can add 'freshness' and flavor to wines
# >
# > - **residual sugar:**
#     the amount of sugar remaining after fermentation stops, it's rare to find
#     wines with less than 1 gram/liter and wines with greater than 45 grams/liter
#     are considered sweet
# >
# > - **chlorides:**
#     the amount of salt in the wine
# >
# > - **free sulfur dioxide:**
#     the free form of SO2 exists in equilibrium between molecular SO2
#     (as a dissolved gas) and bisulfite ion; it prevents microbial growth and
#     the oxidation of wine
# >
# > - **total sulfur dioxide:**
#     amount of free and bound forms of S02; in low concentrations, SO2 is mostly
#     undetectable in wine, but at free SO2 concentrations over 50 ppm, SO2 becomes
#     evident in the nose and taste of wine
# >
# > - **density:**
#     the density of water is close to that of water depending on the percent alcohol
#     and sugar content
# >
# > - **pH:**
#     describes how acidic or basic a wine is on a scale from 0 (very acidic) to
#     14 (very basic); most wines are between 3-4 on the pH scale
# >
# > - **sulphates:**
#     a wine additive which can contribute to sulfur dioxide gas (S02) levels,
#     which acts as an antimicrobial and antioxidant
# >
# > - **alcohol:**
#     the percent alcohol content of the wine
# >
# > - **quality:**
#     output variable (based on sensory data, score between 0 and 10)
#%% [markdown]
# ## Setup
# Os pacotes de python que usaremos para essa análise de dados são:

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#%%
wine = pd.read_csv('winequality-red.csv')  # Leitura do dataset

#%% [markdown]
# ## Observações iniciais
# Usaremos os métodos `.head()`, `.info()` e `.describe()` para ter uma noção geral de como o dataset está estruturado.

#%%
wine.head()  # Mostra as 5 primeiras linhas do dataset

#%% [markdown]
# Pela tabela acima, temos uma ideia geral da organização do dataset. Em geral, dizemos que cada linha é uma **observação** e que as colunas de *fixed acidity* a *alcohol* são as **features**. A coluna *quality* é a **target**. O nosso objetivo é identificar como as features afetam a target, ou seja, como as características do vinho afetam a sua qualidade.

#%%
wine.info()  # Mostra quais são as colunas (ou features) do dataset

#%% [markdown]
# A saída de `wine.info()` acima nos diz que o dataset tem 12 colunas. A coluna quality é de tipo inteiro e as outras são floats. A anotação `non-null` nos diz que não há dados faltantes (na prática, é comum que alguns dos dados não estejam disponíveis).

#%%
wine.describe()  # Mostra algumas estatísticas sobre as features

#%% [markdown]
# Com `wine.describe()`, podemos ver algumas estatísticas sobre o dataset. Por exemplo, de acordo com a descrição do dataset, a qualidade pode variar entre 0 e 10. No entanto, as observações que nós temos só têm qualidades entre 3 e 8, com uma média de 5,63.
# Além disso, olhando o desvio padrão ($\mathrm{std}$), que indica o quanto os valores de alguma coluna variam, observamos que:
# 
# - os valores de *total sulfur dioxide* variam muito ($\mathrm{std} = 32.9$, $\dfrac{\mathrm{std}}{\mathrm{mean}} = 0.71$)
# - os valores de *density* variam pouco ($\mathrm{std} = 0.001887$, $\dfrac{\mathrm{std}}{\mathrm{mean}} = 0.001893$)
# 
# O próximo passo é identificar melhor as características de cada feature (nesse exemplo só analisaremos algumas das features). Para isso usaremos *histogramas*.
# 
# ## quality

#%%
wine['quality'].hist()
plt.show()

#%% [markdown]
# No histograma acima, vemos que a maioria das observações tem uma qualidade intermediária (5 ou 6) e poucas tem os valores mais extremos. Em torno de 680 observações tem qualidade 5 (a qualidade mais comum).
# 
# ## residual sugar

#%%
wine['residual sugar'].hist()
plt.show()

#%% [markdown]
# Observamos que os valores de *residual sugar* são, em geral, pequenos (o gráfico é mais alto na esquerda e tem uma cauda direita). No entanto, existem outliers (observações com valores que distoam da maioria), como as poucas observações com valores próximos de 14. Além disso, a maioria dos valores dessa feature estão entre 1 e 4.
# 
# ## chlorides

#%%
wine['chlorides'].hist()
plt.show()

#%% [markdown]
# Observamos que *chlorides* também tem uma cauda direta e outliers. Pelo gráfico acima, quase todos os valores de *chlorides* estão entre 0 e 0,15. Pelo saída de `wine.describe()` (visto no início do notebook), a média dessa feature é 0,087.
# 
# ## Relação entre as features e a qualidade
# 
# Até aqui observamos as características de cada feature. A partir de agora precisamos entender como essas features se correlacionam e, especificamente, se há alguma relação entre as features e a qualidade do vinho. O primeiro passo é identificar a correlação $\rho$ entre as features e a qualidade. $\rho$ admite valores entre $-1$ e $1$ e indica o grau de correlação linear entre duas variáveis:
# 
# - se $\operatorname{\rho}(x,y) = 1$, então $y = ax+b \quad (a>0)$
# - se $\operatorname{\rho}(x,y) = -1$, então $y = -ax+b \quad (a>0)$
# 
# Por exemplo:
# 
# ![Exemplos de correlação positiva, negativa e nula](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABA8AAAECCAIAAAAehGn1AAAgAElEQVR4Ae2de7xWRbnH2W6wyDS0Nhc3hhAkBCQKiB39cAQOmmmQqIRpUWKU2cnLydycPF4+WWwtTc+pUx+LirQ0Mz5QYnQB7UIqaWiY6cGCjuw4hALeAt0g59eeXK7WvPvd633fdZlZ67v+2HvWrFkzz/Od9c6aZ+aZWU179+7txQEBCEAAAhCAAAQgAAEIQMAisI8VQwQEIAABCEAAAhCAAAQgAIG/EcBa4DmAAAQgAAEIQAACEIAABCoTwFqozIVYCEAAAhCAAAQgAAEIQABrgWcAAhCAAAQgAAEIQAACEKhMAGuhMpcyxG7fvv29733v67oOBXbs2FFR6y1btrz//e8/+OCDX/Oa17z97W9fv369SbZx48Ym6/jsZz9rrn7wgx9805ve1Ldv35aWlpkzZ/7+97+vmDmREICAFwT+93//953vfOd+++33hje84WMf+9iLL75YUew//OEPp5xyin71BxxwwOzZs9V6mGRqLubNmzds2DC1Cfq7YMGCnTt3RnJ48sknW1tb1agoELnEKQQg4DKBmN0JbatzxRVXqDuhduC444773e9+Fyj1P//zP+9617vUvOy///5HH330ihUrzKVvfOMbVkej6de//nVwI4FsCGAtZMPZxVLe8573/OY3v9FvUocCMhhsKfXb1g9YFsLSpUvXrl07ZMiQf/mXf3n++eeV8pBDDtkcOv77v/9bP+nTTjvNZDJhwgT9yGUk/OhHP1Imuquzs9POnxgIQMB9Anv27DnppJOeffbZX/ziF7fccsvtt9/+b//2b7bYahmOP/54/d5XrVq1evVqWRQyMF566SWlfPTRR5XJl770JfUP/uu//uub3/zm+eefH8nhAx/4wLhx4yKRnEIAAu4TiNOdkBbXXHPNtddeqxZA3f3+/ftPnz5drYrR7uSTT961a9fKlSvV0zj22GM1yKihB11697vfHepobD7rrLM03KAOhvtMiiahWnYOxwn89re/lan9qle96qCDDvrEJz6hl27jAj/yyCN6lH/5y1+arNQJ0Kne6JGcH3vsMcU/+OCDJl5Fa9TwK1/5SiSZTmUP6JdvxyvmoYceqph5xcREQgACNRFIo32ICHDnnXdqLEDTCyb+pptuUnP09NNPR5JpaEDJtm3bZuI1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)
#%% [markdown]
# Os scatter plots (gráficos de dispersão) acima representam cada observação por meio de um ponto. Usaremos eles novamente mais a frente.
# 
# A correlação entre as features pode ser mostrada em uma matriz de correlação:

#%%
plt.figure(figsize=(9, 6))  # Aumenta o tamanho da figura
sns.heatmap(wine.corr(), vmin=-1, vmax=1, annot=True, fmt='.2f')
plt.show()

#%% [markdown]
# A partir da matriz acima, podemos identificar que as features que têm maior correlação com a qualidade são: *volatile acidity*, *sulphates* e *alcohol*. Portanto, analisaremos as relações entre essas features por meio de scatter plots. Nos gráficos abaixo, deixaremos os pontos transparentes por meio do parâmetro `alpha`, para que fique claro onde há maior concentração de pontos (caso contrário, alguns pontos seriam "escondidos" por outros pontos).

#%%
wine.plot(x='volatile acidity', y='quality', alpha=.05, kind='scatter')
plt.show()


#%%
wine.plot(x='sulphates', y='quality', alpha=.05, kind='scatter')
plt.show()


#%%
wine.plot(x='alcohol', y='quality', alpha=.05, kind='scatter')
plt.show()

#%% [markdown]
# Nos gráficos acima, podemos observar que há, de fato, correlação entre a qualidade e *volatile acidity*, *sulphates* e *alcohol*.
# 
# Podemos ainda analisar como duas features juntas afetam a qualidade. Nos gráficos abaixo, a cor de cada ponto indica a qualidade.

#%%
wine.plot(x='volatile acidity', y='sulphates', c='quality',
          cmap='Reds', kind='scatter', sharex=False)
plt.show()


#%%
wine.plot(x='alcohol', y='sulphates', c='quality',
          cmap='Reds', kind='scatter', sharex=False)
plt.show()

#%% [markdown]
# Nos gráficos acima, vemos novamente que valores menores de *volatile acidity* e maiores de *sulphates* e *alcohol* correspondem a maiores qualidades.

#%%



#%%



#%%



#%%



#%%



#%%



#%%


