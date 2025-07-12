'''
Faça um programa de computador que imprime todos os divisores 
de 4 até todos os divisores de 44. Em outros termos, você deve 
imprimir divisores de 4 (l, 2, 4), depois os divisores de 5 (1, 5), 
depois os divisores de 6 (I, 2, 3, 6), e assim por diante até 
imprimir os divisores de 44
'''
for i in range(4,45):
    linha = f"{i:02d}->( "
    for j in range(1,i+1):
        if i%j==0:
            if j==i: linha+=f"{j} "
            else: linha+=f"{j}, "
    print(f"{linha})")