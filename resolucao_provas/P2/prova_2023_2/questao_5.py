''' 
5 Duas matrizes matl e mat2 possuem 4x4 inteiros e estão ordenadas 
de
forma crescente linha a linha (não há inteiros repetidos em uma 
mesma matriz), mas o primeiro elemento da segunda linha é maior que o
último da primeira linha e assim por diante até a última linha. 
Crie uma função intersecaoMatrizes(mat1,mat2), que retoma uma lista 
com todos os elementos em comum em ambas matrizes.
'''

def incrementa(i,j):
    if j ==3:
        i+=1
        j=0
    else:
        j+=1
    return i,j

def intersecaoMatrizes(mat1,mat2):
    intersecao = []
    i,j,k,l = 0,0,0,0
    while i<4 and k<4:
        if mat1[i][j] == mat2[k][l]:
            intersecao.append(mat1[i][j])
            i,j=incrementa(i,j)
            k,l=incrementa(k,l)
        elif mat1[i][j] > mat2[k][l]:
            k,l = incrementa(k,l)
        else:
            i,j = incrementa(i,j)
    return intersecao
