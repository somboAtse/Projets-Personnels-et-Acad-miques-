# ------------
# Importations
# ------------
import matplotlib.pyplot as plt
import random
from pprint import pprint




















# ---------------
# Sous-programmes
# ---------------



# ----- Affiche d'une liste de points.
def affiche_points (liste):

    for point in liste:
        plt.scatter(point[0],point[1],color='blue')

    plt.title("Liste de points")
    plt.show()

def affiche_points_wCenter (liste):

    if liste : 
        center=sky_center(liste) 
    for point in liste:
        plt.scatter(point[0],point[1],color='blue')
    if center is float or int :
        plt.scatter(center[0],center[1],color='red', marker='x') 

    # plt.axis([-12,12,-12,12])
    plt.title("Liste de points avec centre ")
    plt.show()

### 1) Ecrire une fonction qui génére aléatoirement une liste de N points.
# Utiliser cette fonction pour générer votre ciel et afficher-le.

def gen_list_point(N,inf,sup,): 
    list_point=[(random.randint(inf,sup),random.randint(inf,sup)) for i in range(N)]
    print("la liste de point est :", list_point)
    return list_point 


### 2) Ecrire une fonction qui calcule le centre d'une liste de points c'est-à-dire le point de coordonnées (X,Y) avec X 
# (resp. Y) moyenne des x (resp. y) de tous les points. Utiliser cette fonction pour calculer le centre de votre ciel 
# et afficher-le.

def sky_center(liste): 
    somX=0
    somY=0 
    for point in liste: 
        somX+=point[0]
        somY+=point[1]
    moyX=somX/len(liste)
    moyY= somY/len(liste)
    center=(moyX,moyY)
    # print("le centre de ce ciel est :", center)
    return center


### 3 ) Ecrire une fonction qui calcule la distance entre 2 points donnés

def distance_2pts(p1,p2):
    dis= round(((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5,3) 
    # print(f"la distance entre {p1} et {p2} est {dis}.")
    return  dis



### 4) Ecrire une fonction qui va générer un ciel de nuages.
### Cette fonction aura les paramètres suivants :
### inf, sup : bornes de espace 2D
### nb : nombre de nuages à générer
### densite : nombre de points dans chaque nuage
### rayon : rayon des nuages

def create_Sky(inf,sup,nb,densite,rayon) :
    # on veux creer nb nuages (3 par défaut)
    ciel=[] 
    for i in range(nb): 
        nuage=[]
        #prend un point aleatoire dans les bornes de l'espace qui sera "le centre de notre nuage"
        center=(random.randint(inf,sup),random.randint(inf,sup)) 
        # print('le centre est :', center )
        minX=center[0]-rayon
        maxX=center[0]+rayon
        minY=center[1]-rayon
        maxY=center[1]+rayon
        #crée le nuage autour 
        for e in range(densite): 
            point=(random.randint(minX,maxX),random.randint(minY,maxY))
            #pour aller vite 
            '''ciel.append(point)''' 
            #pour tester  
            nuage.append(point)
        # print('le nuage est :', nuage)
        ciel.extend(nuage)
    # print('le ciel est ', ciel)
    return ciel


### 5) Afficher un ciel de nuages.
## Après avoir générer aléatoirement un ciel avec 2 nuages, le but de l'exercice est de retrouver
## ces 2 nuages. Pour cela, vous trouverez ci-dessous les étapes d'un algorithme qui permet de 
## partitionner une liste de points (le ciel) en 2 sous-listes (les nuages). 

## Etape 1 :	Choisir aléatoirement 2 points du ciel, nous les appelerons les centroïdes.
def choix_ctro(ciel): 
    # # trois points du ciel  
    # c1=random.choice(ciel)
    # c2=random.choice(ciel)
    # c3=random.choice(ciel)
    # ctro_list=[c1,c2,c3]

    # generalisée
    ctro_list=[]
    print('combien de nuage cherchez-vous ?' )
    c=verify()
    ctro_list=random.sample(ciel,k=c)
    return ctro_list

def afficher_centroide(ciel, ctro_list): 

    for i,point in enumerate(ciel) :
        plt.scatter(point[0],point[1], label='Ciel' if i==0 else '', color='blue')
    for i,ctro in enumerate(ctro_list):
        plt.scatter(ctro[0],ctro[1],label=f"Centroide{'s' if len(ctro_list)>1 else ''}" if i==0 else '', color='red', marker='x') 

    plt.xlabel('Xerus')
    plt.ylabel('Yuri')
    plt.legend()
    plt.title('LA FABRIQUE À NUAGES')
    plt.show()

## Etape 2 :	A partir du ciel, créer 2 nuages tels que le premier contient les points les plus proches
# d’un des 2 centroïdes et le second les points les plus proches de l’autre centroïde.7
def create_nuage(ciel,ctro_list):
    nuages=[[] for i in range(len(ctro_list))]
    for point in ciel: #pour chaque point dans le ciel 
        tab_dis=[] # cré une table pour stocker les distances
        for ctro in ctro_list: #on calcule la distance entre le point et le centroïde, ensuite les stock dans tab_dis
            dis=distance_2pts(point,ctro)
            tab_dis.append(dis)
        c=min(tab_dis) #prend le minimum 
        # print( 'distance', tab_dis)
        # print('minimum' ,c)
        # print('index ', tab_dis.index(c))
        nuages[tab_dis.index(c)].append(point) #ajout du point dans la sous list (nuage), selon l'index de sa distance la plus courte.
    # for i in range(len(nuages)): 
    #     print(f" Le Nuages {i+1} est {nuages[i]} \n{'='*40}\n") 
    return nuages


## Etape 3 :	Calculer le centre pour chacun des 2 nuages. Ces centres deviennent les nouveaux centroïdes.
def newCenter(nuages,ctro_list): 
    for i in range(len(nuages)): 
        ctro_list[i]=sky_center(nuages[i])
    return ctro_list
    

## Etape 4 :	Afficher les 2 nuages avec leur centroïde avec des couleurs différentes.
def affiche_nuages(nuages,ctro_list): 
    # print(len(nuages))
    for i, nuage in enumerate(nuages): 
        # print('nuage :', nuage)
        x=[n[0] for n in nuage]
        y=[n[1] for n in nuage]
        plt.scatter(x,y,label=f'Nuage {i+1}')
    for i,point in enumerate(ctro_list):
        plt.scatter(point[0],point[1], label=f"Centroide{'s' if len(ctro_list)>1 else ''}" if i==0 else '' , color='black', marker='x')
    plt.xlabel('Xerus')
    plt.ylabel('Yuri')
    plt.legend()
    plt.title('LA FABRIQUE À NUAGES')
    plt.show()
        

## Etape 5 :	On recommence à l’étape 2 un certain nombre de fois.

# verification des entrées 
def verify():
    while True:
        entree_user=input("entrez votre choix : ")
        if entree_user.isdigit():
            entree_user=int(entree_user)
            return entree_user

#6) Ecrire les sous-programmes nécessaires pour réaliser l'algorithme ci-dessus.


# -------------------
# Programme principal
# -------------------

######### debut Test #########

# ----- Programme principal.
# ciel = [(1,1),(-2,0),(2,5),(1,-1)]
# affiche_points(ciel)

### 1)
'''affiche_points(gen_list_point(5))''' 

### 2 )
'''random.seed(1)
ciel= gen_list_point(5)
center=sky_center(ciel)
affiche_points_wCenter(ciel,center)'''

### 3) 
'''distance_2pts(random.choice(ciel),random.choice(ciel))'''

### 4) création du ciel 
# random.seed(5)
# #seed 5 très bon 

# ciel=create_Sky(-10,10,3,50,3)
# # affiche_points_wCenter(ciel)


# ### 5 et 6) 
# # 1 etape : choix de centroide  
# ctro_list=choix_ctro(ciel)

# # 2e etape: creation des nuages autours des centroides. 
# nuages=create_nuage(ciel,ctro_list)

# # 3e etape, calcule des nouveaux centroide 
# newCenter(nuages, ctro_list)

# # 4e etape : affichage 
# affiche_nuages(nuages,ctro_list)

# 5e etape : voir boucle principale 


######### fin test ######### 







######### Boucle principale ######### 


## Creation du ciel et affichage du ciel 

# il serait possible de généraliser la creation du ciel et des nuages en suivant ce qui est ci dessous (non terminer) car  pas demander 
'''print(f'Quelles sont les bornes de votre nuages ? \n {'!'*4} (les bornes réelles seront celles que vous donne + votre rayon demander plus bas) {'!'*4}')
print("Borne inf ")
inf=verify()
print('\n')
print("Borne sup ")
sup=verify()
print('\n')
print('combien de nuages souhaitez vous c')'''

random.seed(5)
#seed 5  
#seed 6 
ciel=create_Sky(-10,10,3,50,3)
affiche_points(ciel)


#choix des premier centroide et affichache 
ctro_list=choix_ctro(ciel) 
afficher_centroide(ciel,ctro_list)


# boucle de 5 par defaut
# counter=5 
print("Combien d'iteration souhaitez vous effectuer sur ce ciel ? " )
counter=verify()

while counter>0: 
    print(f" {counter} itération{'' if counter==1 else 's'} restante{'' if counter==1 else 'nt'}")
    # Creation des nuages autours des centroides. 
    nuages=create_nuage(ciel,ctro_list)
    # affiche_nuages(nuages,ctro_list)
    # 3e etape, calcule des nouveaux centroide 
    newCenter(nuages, ctro_list)

    # Affichage des nuages et leur centroide  
    affiche_nuages(nuages,ctro_list)

    counter-=1
print ('done')


# 7) ce code est déjà généralisé 