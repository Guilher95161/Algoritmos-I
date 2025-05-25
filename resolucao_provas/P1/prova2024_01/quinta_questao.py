def animaisScanner(vida1,vida2,vida3,vida4,vida5):
    # Se for os tipos vistos de animais é isso
    contador_animais=0
    if vida1==123 or vida2==123 or vida3==123 or vida4==123 or vida5==123:
        contador_animais+=1
    if vida1==234 or vida2==234 or vida3==234 or vida4==234 or vida5==234:
        contador_animais+=1
    if vida1==345 or vida2==345 or vida3==345 or vida4==345 or vida5==345:
        contador_animais+=1
    if vida1==456 or vida2==456 or vida3==456 or vida4==456 or vida5==456:
        contador_animais+=1
    return contador_animais
    # Se for a quantidade de animais vistos é isso:
    '''
    qtd_animais=0
    vidas = [vida1,vida2,vida3,vida4,vida5]
    animais = [123,234,345,456]
    if vida1 in animais:
        qtd_animais+=1
    if vida2 in animais:
        qtd_animais+=1
    if vida3 in animais:
        qtd_animais+=1
    if vida4 in animais:
        qtd_animais+=1
    if vida5 in animais:
        qtd_animais+=1
    return qtd_animais
    for vida in vidas:
        if vida in animais:
            qtd_animais+=1
    return qtd_animais
    '''