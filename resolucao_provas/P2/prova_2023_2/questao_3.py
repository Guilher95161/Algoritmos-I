'''
3. A de inteiros grmdes ern fatores prirnos é algo utilizado na 
cnptografia.
Coe uma que reWna todos os intetros que podem ser Obbdos
exatarnente trés fatores de um vetor primos dado como entrada. 
que possu apenas
interos pnrnos sem repetjçóes. A assinatura da 
funçSo deve ser: def
'''
def chaves(primos):
    v_chaves=[]
    for i in range(len(primos)-2):
        for j in range(i+1,len(primos)-1):
            for k in range(i+2,len(primos)):
                v_chaves.append(primos[i]*primos[j]*primos[k])
    return v_chaves
