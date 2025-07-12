'''
4. uma matnz mat possui 4x5 cadeias de caracteres
A funcção colunasComUFMA(mat) deve retornar quantas das cinco colunas
dessa matriz possuem a string"UFMA"
'''
def colunasComUFMA(mat):
    cont_ufma = 0
    for j in range(5):
        for i in range(4):
            if mat[i][j] == "UFMA":
                cont_ufma+=1
                break
    return cont_ufma
