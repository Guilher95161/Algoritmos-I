'''
3. Função emOrdem,que verifica se um vetor está em ordem crescente.
Para estar em estritamente crescente, cada elemento do vetor precisa
ser maior que o anterior
'''
def emOrdem(nums):
    for i in range(len(nums)-1):
        if not nums[i]<nums[i+1]: return False
    return True
