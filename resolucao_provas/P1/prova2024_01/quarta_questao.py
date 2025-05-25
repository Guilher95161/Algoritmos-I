def ataque(atq1,atq2,atq3,def1,def2,def3):
    maior= max(atq1,atq2,atq3)
    menor = min(atq1,atq2,atq3)
    meio = atq1+atq2+atq3-maior-menor
    atq1=maior
    atq2=meio
    atq3=menor
    maior=meio=menor=0
    maior=max(def1,def2,def3)
    menor = min(def1,def2,def3)
    meio = def1+def2+def3-maior-menor
    def1=maior
    def2=meio
    def3=menor
    contador_acertos=0
    if atq1>def1:
        contador_acertos+=1
    if atq2>def2:
        contador_acertos+=1
    if atq3>def3:
        contador_acertos+=1
    return contador_acertos

print(ataque(3,3,3,1,2,3))