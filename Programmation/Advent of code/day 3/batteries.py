donnee= []
with open('puzzle inp.txt', 'r') as f :
    for line in f : 
        donnee.append(line.strip()) 
# print(donnee)

# # =======================
# #   PART ONE 
# # =======================

# # print('='*40+"PART ONE"+"="*40+"\n")

# # def  plus_grande_combinaison( chaine ): 
# #     comb_tab=[]
# #     for i in range(len(chaine)): 
# #         for j in range ((i+1),len(chaine)): 
# #             comb=int(chaine[i]+chaine[j])
# #     #         print(comb)
# #             comb_tab.append(comb)
# #     # print(comb_tab)       
# #     return max(comb_tab)

# # som=0
# # for chaines in donnee : 
# #     som+= plus_grande_combinaison(chaines)
# # print ('la somme est :',som )




# # =======================
# #   PART TWO
# # =======================

# print('='*40+"PART WO"+"="*40+"\n")

# # def  plus_grande_combinaison2( chaine ): 
# #     comb_tab=[]
# #     couter=len(chaine) 
# #     for i in range((couter-11)): 
# #         for j in range ((i+1),(couter-10)):
# #             for k in range ((j+1),(couter-9)):
# #                 for l in range ((k+1),(couter-8)):
# #                     for m in range ((l+1),(couter-7)):
# #                         for o in range ((m+1),(couter-6)):
# #                             for p in range ((o+1),(couter-5)):
# #                                 for q in range ((p+1),(couter-4)):
# #                                     for r in range ((q+1),(couter-3)):
# #                                         for s in range ((r+1),(couter-2)):
# #                                             for t in range ((s+1),(couter-1)):
# #                                                 for u in range ((t+1),(couter)):
# #                                                     comb=int(chaine[i]+chaine[j]+chaine[k]+chaine[l]+chaine[m]+chaine[o]+chaine[p]+chaine[q]+chaine[r]+chaine[s]+chaine[t]+chaine[u])
# #                                                     # print(comb)
# #                                                     comb_tab.append(comb)
#     # print(comb_tab)
#     # return max(comb_tab)


def  plus_grande_combinaison2( chaine, comb_tab2, nb):
    if len(chaine)>=nb and nb>0: 
        com=[]
        limite=len(chaine)-(nb-1)
        for element in chaine[:(limite)]:
            com.append(int(element))
        maxi=max(com) 
        pos_depart=chaine[:(limite)].index(str(maxi))
        # for i, element in enumerate(chaine[:(limite)]) : 
        #     if element==maxi:
        #         pos_depart=i 
        comb_tab2.append(maxi)
        # print('le max de', chaine[:(limite)], 'est',max(com))
        plus_grande_combinaison2(chaine[pos_depart+1:],comb_tab2,nb-1)
    return comb_tab2




# print(plus_grande_combinaison2('283947519896',comb_tab2,5))
som2=0
# donnee=['54869326587','36956698563','36598678452']
for chaines in donnee : 
    comb_tab2=[]
    plus_grande_combinaison2(chaines,comb_tab2,12)
    new_comb=""
    for element in comb_tab2:
        new_comb+=str(element)
    som2+=int(new_comb)
    # print(new_comb,som2)
print('la som',som2)


# som2=0
# for chaines in donnee : 
#     som2+= plus_grande_combinaison2(chaines)
# print ('la somme est :',som2 )
