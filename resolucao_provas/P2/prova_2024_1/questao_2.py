'''
Crie uma função moveZeroes, que move os zeros de um
vetor para o final do mesmo, mantendo a ordem relativa
dos outros valores diferentes de zero. 
'''
def moveZeroes(nums):
    diferente = 0
    for i in range(len(nums)):
        if nums[i]!=0:
            nums[i],nums[diferente]=nums[diferente],nums[i]
            diferente+=1
    return nums
print(moveZeroes([0,1,0,3,12]))
print(moveZeroes([0,0]))
print(moveZeroes([10,20,30]))