import pandas as pd 

# 1. Le DataFrame des Clients
df_clients = pd.DataFrame({
    'idCli': [1, 2],
    'nomCli': ['Kent', 'Martin'],
    'prenomCli': ['Alice', 'Jean']
})

# 2. Le DataFrame des Produits
df_produits = pd.DataFrame({
    'idProd': [101, 102],
    'nomProd': ['Chaussures de sport', 'Escarpins rouges'],
    'categorie': ['Chaussures', 'Chaussures']
})

# 3. Le DataFrame des Commentaires
# C'est ici qu'on a les notes pour les calculs
df_commentaires = pd.DataFrame({
    'idCli': [1, 1, 2],
    'idProd': [101, 102, 101],
    'note': [5, 1, 2],
    'texte': ['Super !', 'Trop petit...', 'Pas terrible']
})

# Vérification 
print("--- Aperçu des commentaires ---")
print(df_commentaires.head()) 


# # questions 6.a) 

# jointure 
data1 = pd.merge(df_commentaires,df_produits, on='idProd',how='inner')
print(data1)
print('\n')

data1 = pd.merge(data1, df_clients, on='idCli', how='inner')
print(data1)
print('\n')

#restriction 
data1 = data1[data1["note"] <= 2 ]
print(data1)
print('\n')

#projection 
data1= data1[["texte","nomCli","prenomCli","nomProd"]]
print(data1)
print('\n')




# quetion 6.b 

# jointure 
data2 = pd.merge(df_commentaires,df_produits, on='idProd',how='inner')
print(data2)
print('\n')

# regroupement 
data2 = data2.groupby("nomProd", as_index= False).agg({"note":'mean'})
print(data2)
print('\n')

# restriction 
data2 = data2[data2['note'] >= 2]
print (data2)
print('\n')
