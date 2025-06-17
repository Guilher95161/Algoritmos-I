#2° Para cada posição do vetor, retorne o produto de todos os elemento, exceto ele mesmo. Não use divisão 😊😊
def produto_vetor_exceto_indice(num):
    valor_indice=1
    novo_vetor=[]
    for i in num:#1
        for j in num:#1,2,3,4
            if j!=i:
                valor_indice*=j
        novo_vetor.append(valor_indice)
        valor_indice=1
    return novo_vetor

print(produto_vetor_exceto_indice([1,2,3,4]))

#3° Receba um vetor de inteiros e diga quantas vezes aparece cada número
def diz_qtd_valores_vetor(vetor):
    vezes_aparece=0
    mensagem=""
    vetor_valores_já_vistos=[]
    for i in vetor:
        if not i in vetor_valores_já_vistos:
            for j in vetor:
                if i==j:
                    vezes_aparece+=1
            vetor_valores_já_vistos.append(i)
            mensagem+=f"{i} - {vezes_aparece} vez(es)\n"
            vezes_aparece=0
    return mensagem
print(diz_qtd_valores_vetor([1,2,2,3,4,1,7]))

#4° Dado um vetor de inteiros, conte quantos pares de índices (i,j) existem tal que:
    #i<j & nums[i]==nums[j]
def contar_pares_iguais(nums):
    contador=0
    for i in range(len(nums)):
        for j in range(len(nums)):
            if i<j and nums[i] ==nums[j]:
                contador+=1
    return contador