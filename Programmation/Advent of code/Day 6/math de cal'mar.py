import math 


# =======================
#   PART ONE 
# =======================

# print('='*40+"PART ONE"+"="*40+"\n")

# donnees=[]
# with open('Math worksheets.txt','r') as f: 
#     for l in f :
#         donnees.append(l.strip().split())
# # for l in donnees :
# #     print(len(l))
# print(donnees) 


# new_donnees=[]
# for j in range (len(donnees[0])): 
#     i=0
#     col=[]
#     while i<5:
#         donnee=donnees[i][j]
#         col.append(int(donnee) if donnee.isdigit() else donnee)
#         i+=1
#     new_donnees.append(col)


# results=[]
# som=0
# for element in new_donnees:
#     if element[-1]=='+':
#         results.append(sum(element[:-1]))
#     else : 
#         results.append(math.prod(element[:-1]))

# print (len(results))
# print (results)
# print (sum(results))





# # =======================
# #   PART  TWO 
# # =======================

# print('='*40+"PART TWO"+"="*40+"\n")


# En gros je rajoute des @ aux espaces vides qui servent à délimité les colones, et des 0 aux autres. pour avoir la même longueur de données à chaque colone (pareil pour les signe)
# à la fin pour une colone on aura => ['xxx','xxx','xxx','+++'] ce qui va nous facilité le calcules en cephalopode. 
donnees=[]
with open('Math worksheets.txt','r') as f: 
    for l in f :
        donnees.append(l.strip())

# print(len(donnees[1]),len(donnees[0]),len(donnees[2]),len(donnees)) 
# print(donnees)

#creation de liste de chaine de caractère avec TOUT LES CARACTERES pour mieux les structurer 
for i in range (len(donnees)):
    don=[]
    for element in donnees[i]: 
        don.append(element)
    donnees[i]=don
# print(donnees)

#separation des colonnes
for j,element in enumerate(donnees[0]): 
    if element==" ":
        ver=donnees[0][j]==donnees[1][j]==donnees[2][j]==donnees[3][j]==donnees[4][j]
        # print (ver)
        if ver : 
            for element in donnees:
                element[j]="@" 
# print(donnees)

#remplacement des espaces vides par 0
for element in donnees : 
    for i in range(len(element)): 
        if element[i]==" ":
            element[i]='.'
# print(donnees)

#retour  sur les chaines de caractères 
new_donnees=[]
for elt in donnees: 
    don=""
    for el in elt: 
        don+=el 
    new_donnees.append(don)
# print(new_donnees)
# with open('donnees.txt','w') as f: 
#     f.writelines(new_donnees)

#creation de la nouvelle liste mieux struturer 
donnees=[]
for elt in new_donnees:
    donnees.append(elt.split('@'))
# print (donnees)


signes=[]
for elt in donnees[-1]: 
    signe=elt[0]
    new=elt.replace(".",signe)
    signes.append(new)
donnees[-1]=signes
# print(donnees)
#fin structuration_________________________

new_donnees=[]
for j in range (len(donnees[0])): 
    i=0
    col=[]
    while i<5:
        donnee=donnees[i][j]
        col.append(donnee)
        i+=1
    new_donnees.append(col)

# print(new_donnees)

results=[]
lliste=4
for liste in new_donnees:
    new_liste=[] 
    lchaine=len(liste[-1])
    for col in range(lchaine): 
        ch=""
        for ligne in range(lliste):
            if liste[ligne][col]!=".":
                ch+= liste[ligne][col]
        if ch:
            new_liste.append(int(ch))
    if '+' in liste[-1]: 
        results.append(sum(new_liste))
    else :
        results.append(math.prod(new_liste))

print(len(new_donnees))
print(len(results))
# print(results)
print(sum(results))


