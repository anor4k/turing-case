import numpy as np
# recebe o tamanho da matriz 3 2, em seguida toda a matriz em uma linha
matrix_shape = input("Input size: ").split()
matrix_shape = (int(matrix_shape[0]), int(matrix_shape[1]))
input_matrix = input("Matrix values: ").split()
input_matrix = [int(i) for i in input_matrix] #converte entrada para int

# normaliza a matriz ainda como lista
def Normalize(arr:list):
    avg = sum(arr)/len(arr)
    return [(i - avg) for i in arr]

input_matrix = Normalize(input_matrix)
print(input_matrix)
# transforma a lista em matriz usando um array numpy
matrix = np.array(input_matrix, np.int32).reshape(matrix_shape)

start_line = start_column = end_line = end_column = max_global = max_now = 0

for line in range(0, matrix_shape[0]):
    max_now = 0
    for column in range(0, matrix_shape[1]):
        max_now += matrix[line, column]
        if max_now > max_global:
            max_global = max_now
        if max_now < 0:
            max_now = 0
        else:
            for other_lines in matrix[line + 1:,:]:
                max_now += other_lines[column]
                if max_now < 0:
                    max_now = 0
                    break
                elif max_now > max_global:
                    max_global = max_now
                break

print(max_global)
