def sumCount(value:int,d1:int,d2:int,d3:int,d4:int,d5:int) -> int:
    conta_values = 0
    if d1==value:
        conta_values+=1
    if d2 == value:
        conta_values+=1
    if d3 == value:
        conta_values+=1
    if d4 == value:
        conta_values+=1
    if d5 == value:
        conta_values+=1
    return value*conta_values