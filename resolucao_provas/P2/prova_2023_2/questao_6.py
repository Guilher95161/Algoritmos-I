'''
E. uma mãriz mat tem 8x8 números reais e possui quatro quadrantes,
que são matrizes 4x4. conforme cada cor da figura ao lado. Crie uma
função quartoQuadrante(mat) que retoma uma matriz 4x4 com os reais no
quarto quadrante
'''
def quartoQuadrante(mat):
    quarto_quadrante = [[None for _ in range(4)] for _ in range(4)]
    for i in range(4,8):
        for j in range(4,8):
            quarto_quadrante[i-4][j-4] = mat[i][j]
    return quarto_quadrante