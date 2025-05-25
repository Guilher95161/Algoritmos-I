def fullhouse (d1:int, d2:int, d3:int, d4:int, d5:int) -> bool:
    conta_d1 = 1 + (d2==d1)+(d3==d1)+(d4==d1)+(d5==d1)
    if d1 != d2:
        diferente =d2
    elif d1!=d3:
        diferente =d3
    elif d1!= d4:
        diferente = d4
    elif d1!=d5:
        diferente = d5
    else:
        return False
    conta_diferente = (d2==diferente) + (d3==diferente) +(d4==diferente)+(d5==diferente)
    if (conta_d1==2 and conta_diferente==3) or (conta_d1==3 and conta_diferente==2):
        return True
    else:
        return False
    
print(fullhouse(1,2,1,2,1))  # True
print(fullhouse(4,4,4,4,4))  # False
print(fullhouse(3,3,5,5,5))  # True
print(fullhouse(1,2,3,4,5))  # False
print(fullhouse(2,2,2,3,3))  # True