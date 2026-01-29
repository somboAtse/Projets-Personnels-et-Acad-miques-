
grille=[]
with open('rolls_paper_grid.txt', 'r')as f: 
    for line in f:
        gr=[]
        for element in line.strip():
            gr.append(element.strip())
        grille.append(gr)

for line in grille: 
    line.insert(0,'.')
    line.append('.')
grille.insert(0,['.' for i in range (len(grille[1]))])
grille.append(['.' for i in range (len(grille[1]))])

# print(grille)
gc=0
for line in grille:
    for elt in line:
        if elt=='@':
            gc+=1
print ('il y avait premièrement',gc,'rouleaux dans la grille ') 


# =======================
#   PART ONE 
# =======================

print('='*40+"PART ONE"+"="*40+"\n")

grille_access=[] #elements accessible de toute les ligne # pas obligé vu qu'on veut juste compter ici tout les element accessible. 
count=0 #compteur des élement accessible 
for i, elt in enumerate(grille):
    gr_access=[] #element accessible pour le ligne d'index i  
    # cpt=0 # compteur des rouleaux pour verification
    for j,el in enumerate(elt): 
        cpt=0 # compteur des rouleaux pour verification
        if el=='@':
            if grille[i][j-1]=='@':
                cpt+=1       
            if grille[i][j+1]=='@':
                cpt+=1      
            if grille[i-1][j-1]=='@':
                cpt+=1      
            if grille[i-1][j]=='@':
                cpt+=1      
            if grille[i-1][j+1]=='@':
                cpt+=1       
            if grille[i+1][j-1]=='@':
                cpt+=1       
            if grille[i+1][j]=='@':
                    cpt+=1      
            if grille[i+1][j+1]=='@':
                cpt+=1           
            if cpt<4:
                gr_access.append((i,j)) 
                count+=1
    grille_access.append(gr_access) # pas obligé mais pourrait etre utile. 

print('il ya ',count, 'elements accessibles')
print ('il y a donc pour la partie 1 ',(gc-count),'rouleaux restant dans la grille ') 


# # =======================
# #   PART  
# # =======================


print('='*40+"PART TWO"+"="*40+"\n")


count_T=0 #compteur des élement retiré au total après chaque itération 
def removable(grille,count_T):
    # count=0 #compte les element retiré de la grille
    grille_access=[] # position des elements à supprimé dans toute la grille  (ligne par ligne)
    for i, elt in enumerate(grille):
        gr_access=[] #element accessible pour le ligne d'index i  
        for j,el in enumerate(elt): 
            cpt=0 # compte pour chaque element de la ligne les rouleaux autour 
            if el=='@':
                if grille[i][j-1]=='@':
                    cpt+=1 
                if grille[i][j+1]=='@':
                    cpt+=1
                if grille[i-1][j-1]=='@':
                    cpt+=1
                if grille[i-1][j]=='@':
                    cpt+=1
                if grille[i-1][j+1]=='@':
                    cpt+=1 
                if grille[i+1][j-1]=='@':
                    cpt+=1 
                if grille[i+1][j]=='@':
                    cpt+=1
                if grille[i+1][j+1]=='@':
                    cpt+=1
                if cpt<4: # prend tout les element à supprimer de la ligne 
                    gr_access.append((i,j))
                    # count+=1
                    count_T+=1 #peut le mettre ici
        if gr_access: # la grille des elt à supprimer ne recoit que s'il y a des elts à supprimé sur la ligne
            grille_access.append(gr_access)
    
    if grille_access: #si la grille des elts à supp n'est pas vide, alors on supprime les élément et on rappelle la fonction avec la nouvelle grille 
        for ligne in grille_access:
            for element in ligne : 
                grille[element[0]][element[1]]='.'
        return removable(grille,count_T)
    else : # si elle est vide on retourne la grille vide 
        return count_T, grille

nb_remove, last_grille=removable(grille, count_T) 
print('retiré totale :',nb_remove)
# print('grille finalle :\n', last_grille)    

gc=0
for line in grille:
    for elt in line:
        if elt=='@':
            gc+=1
print ('il y a au final ',gc,'rouleaux restant dans la grille ') 


