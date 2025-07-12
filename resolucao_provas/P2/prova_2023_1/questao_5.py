'''
Uma matriz booleana 19X19 representa o tabuleiro do Jogo Go. Cada
posição da matriz está preenchida com uma peça branca ou preta. A
matriz possui True para representar uma  preta ou False para
representar uma branca. Vence o jogo a peça que houver em
ero na matriz Sabendo disso, crie uma função maior
vencedorD0Go, que recebe como parâmetro uma matriz booleana
19x19 chamada PPyleiro e deve retornar True se a majoria—das
peças for preta ou False se a maioria das peças for branca
vencedorDoGo (tabuleiro) :
'''
def vencedorDoGo(tabuleiro):
    cont_pretas=0
    cont_brancas=0
    for i in range(19):
        for j in range(19):
            if tabuleiro[i][j]==False:
                cont_brancas+=1
            else:
                cont_pretas+=1
    return cont_pretas>cont_brancas