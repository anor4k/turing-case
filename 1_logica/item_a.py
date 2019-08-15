#Noel Viscome Eliezer – noel.eliezer@icloud.com

# recebe entradas no formato 4 2 0
input_list = input("Input: ").split()
# converte entradas para lista de int
input_list = [int(i) for i in input_list]

# normaliza o vetor de entrada para média 0
def Normalize(input:list):
    avg = sum(input)/len(input)
    return [(i - avg) for i in input]

# algoritmo de kadane
# complexidade O(n), faz todas as somas temporárias em um loop e preserva a maior
in_array = Normalize(input_list)
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
print (str(start) + ", " + str(end - start + 1))