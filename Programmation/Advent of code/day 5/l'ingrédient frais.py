# ver_ingr= []
# ingr_test=[]
# ingr_frais=[]
# with open( 'fresh_ID.txt','r') as f : 
#     for line in f: 
#         if "-" in line:
#             inter=line.strip().split("-")
#             ver_ingr.append((int(inter[0]),int(inter[1])))
#         else: 
#             inter=line.strip()
#             if inter.isdigit():
#                 ingr_test.append(int(inter))

# # print("renge: ", ver_ingr)
# # print("ingr_test :", ingr_test)


# # =======================
# #   PART ONE 
# # =======================

# # print('='*40+"PART ONE"+"="*40+"\n")


# # def ver_fresh(ver, val_test): 
# #     for inter in ver :
# #         if (val_test>=inter[0]) and (val_test<=inter[1]):
# #             return True
# #     return False 

# # print("nombre d'ingrediens  à test",len(ingr_test))

# # for id in ingr_test:
# #     if ver_fresh(ver_ingr,id) : 
# #         ingr_frais.append(id)
# # print ("il ya ",len(ingr_frais),"en tout")


# # # =======================
# # #   PART  TWO 
# # # =======================

# import portion as p 

# print('='*40+"PART TWO"+"="*40+"\n")
# print(len(ver_ingr))
# new_ver_ingr=p.empty()
# for inter in ver_ingr:
#     new_ver_ingr=new_ver_ingr | p.closed(inter[0],inter[1])

# total_fresh_id=0
# for inter in new_ver_ingr:
#     total_fresh_id+=(inter.upper-inter.lower+1)
# print(total_fresh_id)
# # print(new_ver_ingr)
# # print(len(new_ver_ingr))



# # print("nombre d'ingrediens  à test",len(ingr_test))

# # ingr_frais2=nb_ingr_fresh(ver_ingr)

# # print("il ya", len(ingr_frais2),"ingrédients considérer frais en tout. ")


ch='+000'
ch=ch.replace('0','+')
print(ch)