def notaReposicao(nota1,nota2,nota3):
    soma = nota1+nota2+nota3
    if soma>=210:
        return 0
    maior = max(nota1,nota2,nota3)
    menor = min(nota1,nota2,nota3)
    meio = soma -maior-menor
    reposicao = 210 - maior-meio
    if reposicao > 100:
        return "Não é possível com a quarta prova, pois precisa tirar mais que 100"
    else:
        return reposicao
    
nota1,nota2,nota3 = map(float,input().split())
print(notaReposicao(nota1,nota2,nota3))