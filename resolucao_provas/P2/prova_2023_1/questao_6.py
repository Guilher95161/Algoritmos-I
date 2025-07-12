def procurarPadrao(imagem,padrao)->int:
    vezes = 0
    bateu = True
    for i in range(1000-7):
        for j in range(1000-7):
            bateu=True
            for k in range(8):
                for l in range(8):
                    if imagem[i+k][j+l]!=padrao[k][l]:
                        bateu = False
                        break
                if not bateu: break
            if bateu:
                vezes+=1
    return vezes