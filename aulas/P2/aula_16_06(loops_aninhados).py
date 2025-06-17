##Imprimir os divisores dos valores de 1 a 10
for i in range(1,11):
    linha = f"{i} = "
    for j in range(1,i+1):
        if i%j==0:
            linha += f"{j} "
    print(linha)
    
## Tabuada de 1 a 10
for i in range(1,11):
    print(f"\nTabuada do {i}:\n")
    for j in range(1,11):
        print(f"{i} * {j} = {i*j}")

## Faz o quadrado da multiplicação, fds
i = int(input("\nDigite o l do quadrado: "))
for _ in range(1,i+1):
    for _ in range(1,i+1):
        print(f"{i}", end=" ")
    print()