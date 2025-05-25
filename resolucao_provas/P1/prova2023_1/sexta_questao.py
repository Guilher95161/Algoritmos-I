# def party(name1,name2,name3):
#     if name1=="Maria":
#         return name2=="João" or name3=="João":
#     elif name2 == "Maria":
#         return name1 or name3=="João"
#     else:
#         return name1=="João" or name2=="João"
'''O Certo'''
def party(name1,name2,name3):
    if name1=="Maria":
        return name2=="João" or name3=="João"
    elif name2 == "Maria":
        return name1=="João" or name3=="João"
    elif name3=="Maria":
        return name1=="João" or name2=="João"
    else:
        return False