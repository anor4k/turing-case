#Noel Viscome Eliezer – noel.eliezer@icloud.com

import numpy as np
# recebe o tamanho da matriz 3 2, em seguida toda a matriz em uma linha
matrix_shape = input("Input size: ").split()
nrows, ncols = int(matrix_shape[0]), int(matrix_shape[1])
input_matrix = input("Matrix values: ").split()
input_matrix = [int(i) for i in input_matrix] # converte entrada para int

# normaliza a matriz ainda como lista
def Normalize(arr:list):
    avg = sum(arr)/len(arr)
    return [(i - avg) for i in arr]

input_matrix = Normalize(input_matrix)
# transforma a lista em matriz usando um array numpy
matrix = np.array(input_matrix, np.int32).reshape((nrows, ncols))
print(matrix)

# mesmo algoritmo do item A, retorna (soma, início, final)
def kadane(in_array):
    max_global = max_here = tempstart = start = end = 0

    for i in range(0, len(in_array)):
        # adiciona o próximo elemento do array à soma temporária
        max_here += in_array[i]
        # caso seja negativo, reseta a soma temporária
        if max_here < 0:
            max_here = 0
            tempstart = i + 1
        # atualiza a soma global caso seja maior
        elif max_here >= max_global:
            max_global = max_here
            start = tempstart
            end = i
    return (max_global, start, end)
'''
O algoritmo abaixo combina o método de força bruta (iterar sobre todas as combinações de submatrizes)
com o algoritmo de kadane para tornar o último loop linear
Itera sobre a soma de cada linha com algoritmo de kadane entre todas as combinações de coluna inicial e final;
tempo em ordem O(n^3); baseado em: https://prismoskills.appspot.com/lessons/Dynamic_Programming/Chapter_19_-_Largest_sum_contiguous_subarray.jsp
'''
max_global = max_now = start_col = end_col = start_row = end_row = 0
for left in range(0, ncols):
    # inicializa array temporário para a soma das linhas
    temp = [0 for i in range(nrows)]
    start_row_temp = end_row_temp = 0
    for right in range(left, ncols):
        # armazena a soma de cada linha no array temporário
        for i in range(0, nrows):
            temp[i] += matrix[i, right]
        # itera sobre a linha usando o algoritmo de kadane
        (max_now, start_row_temp, end_row_temp) = kadane(temp)
        # atualiza o máximo global e o início e final
        if max_now > max_global:
            start_col = left
            end_col = right
            start_row = start_row_temp
            end_row = end_row_temp
            max_global = max_now

print("(" + str(start_row) + ", " + str(start_col) + ")" + ", i = " + str(end_row - start_row + 1) + ", j = " + str(end_col - start_col + 1))
