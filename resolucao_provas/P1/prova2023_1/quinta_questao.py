int1,int2,int3,int4 = map(int,input("Digite quatros inteiros,separados por espaço: ").split())
maior = max(int1,int2,int3,int4)
menor = min(int1,int2,int3,int4)
soma_outros = int1+int2+int3+int4-maior-menor
if maior+menor>soma_outros:
    print("A soma do maior e o menor valor é maior que a soma dos inteiros restantes")
elif maior+menor == soma_outros:
    print("A soma do maior e menor valor é igual a soma dos inteiros restantes")
else:
    print("A soma do maior e menor valor é menor que a soma dos inteiros restantes")
 