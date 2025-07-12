'''
Crie a função encontrarProduto, que tem como parâmetro um
vetor v, com 100 inteiros e um inteiro alvo. 
A função deve retornar um valor lógico. Para retornar verdadeiro 
(True), o inteiro alvo deve serencontrado como o produto_de 
dois inteiros do vetor v. Caso contrário, a função deve retornar 
falso (False).
'''
def encontrarProduto(v,alvo):
    for i in range(100):
        for j in range(i+1,100):
            if v[i]*v[j]==alvo: return True
    return False