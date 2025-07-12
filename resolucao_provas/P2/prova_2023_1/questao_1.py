#1. Faça um programa de computador que imprime todos os números
#que iniciam pelo dígito 3 ou terminam pelo digito 3, de I a 1000. 
# Você vai imprimir, portanto: 3,13,23,30,301 até 993.
for i in range(1,1001):
    if "3" in str(i)[0]:
        print(i)
    elif "3" in str(i)[-1]:
        print(i)