# document=[]
# with open('1e puzzle input.txt.txt', 'r') as f: 
#     for ligne in f: 
#         document.append(ligne.strip())
# # print(document) 

# # som=50 
# # counter=0
# # for element in document:
# #     nb=int(element[1:]) 
# #     som = (som+nb)%100 if element.startswith('R') else (som-nb)%100
# #     if som==0:
# #         counter+=1
# # print(som)
# # print(counter)

# som=50 
# counter=0
# for element in document:
#     nb=int(element[1:]) 
#     som = (som+nb) if element.startswith('R') else (som-nb)
#     if som>99 :
#         counter+=som//100
#     elif som<0 : 
#           counter+=abs(som)//100
#     elif (som%100)==0:
#             counter+=1
#     som%=100
        
#     # elif (som%100)==0:
#     #         counter+=1

# print('new',som)
# print('new', counter)

# print( 'chat')
# som = 50 
# counter = 0

# for element in document:
#     nb = int(element[1:]) 
    
#     if element.startswith('R'):
#         nouvelle_som = som + nb
#         # On compare le nombre de centaines avant et après
#         # Ex: 50 (0) -> 150 (1). Différence = 1 clic.
#         counter += (nouvelle_som // 100) - (som // 100)
        
#         # On met à jour la position réelle sur le cadran [0-99]
#         som = nouvelle_som % 100
        
#     else: # Cas 'L'
#         nouvelle_som = som - nb
#         # On applique le décalage de -1 pour gérer le départ à 0
#         # Ex: 0 (-1) -> -5 (-1). Différence = 0.
#         # Ex: 50 (0) -> -18 (-1). Différence = 1.
#         counter += ((som - 1) // 100) - ((nouvelle_som - 1) // 100)
        
#         som = nouvelle_som % 100

# print('Position finale:', som)
# print('Compteur total:', counter)


print(len(4444))