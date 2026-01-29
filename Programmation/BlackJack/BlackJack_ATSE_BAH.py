# ------------
# Importations
# ------------
import json, random
from pprint import pprint
import colorama
from colorama import Fore, Style

# Initialise Colorama pour qu'il s'auto-reset après chaque print()
colorama.init(autoreset=True)









# ---------------
# Sous-programmes
# ---------------

# Constante pour la sauvegarde 
FICHIER_SAUVEGARDE = "blackjack_partie.json"

### création ou lecture du fichier json pour les cartes, les melange et retourne le sabot 
def charger_sabot(fichierJson,nbjeuxcarte):
    print("\n" + "="*40)
    print(Fore.YELLOW + Style.BRIGHT + "--- CHARGEMENT DU SABOT ---")
    print("="*40)
    
    #vérifie si les carte existe, si oui il les chargent directement, si non, il les les crées, 
    try :
        with open (fichierJson,"r", encoding="utf-8") as f:
            cartes=json.load(f)
        sabot=[]
        for i in range (nbjeuxcarte) :
            for carte in cartes:
                sabot.append(carte)
        random.shuffle(sabot)
        return sabot 
    
    except Exception as e : 
        #que le fichier soit vide ou inexistant, on ecrase et cré un nouveau/ cré un nouveau 
        rangs=["AS","2","3","4","5","6","7","8","9","10","DAME","VALET","ROI"]
        valeur={"AS":11,"DAME":10,"VALET":10,"ROI":10}
        symboles=["♥","♦","♣","♠"]
        #Les unicode pour ces symboles sont : coeur = "\u2665", carreau = "\u2666",  trefle = "\u2663", pique = "\u2660". 
        cartes=[]
        for symbole in symboles: 
            for rang in rangs:
                valeur_Carte=int(rang) if rang.isdigit() else valeur.get(rang,0)
                carte={"numero":rang, "symbole":symbole, "valeur":valeur_Carte}
                cartes.append(carte)  

        #enregistrement des cartes dans un fichier json: 
        with open(fichierJson,"w+", encoding="utf-8") as f:
            json.dump(cartes, f, indent=2, ensure_ascii=False)
                # indent=2 pour que ça soit joliment visible, ensure_ascii=False pour garder les symbole 
                # sans les changer en unicode, encoding=utf-8 pour s'assurer que les symboles s'affichent
        sabot = cartes * nbjeuxcarte
        random.shuffle(sabot)
        return sabot

### Verifie la longueur du sabot avant chaque pioche d'une carte 
def piocher_carte(sabot):
    # S'il  moins d'un jeu de carte on reload.
    if len(sabot) < 52: 
        print("--- Le sabot est presque vide. Re-mélange... ---")
        # On recharge et re-mélange
        sabot[:] = charger_sabot("cartes.json", 6) 
        # si on utilise sabot=, le programme principale  gardera le sabot presque vide alors qu'on veut une recharge 
    # Dans tous les cas, on pioche
    return sabot.pop(0)


## La table de jeu : Crée la structure principale du jeu, gérant les emplacements des joueurs.
def table_jeu(nbdejoueurs):
    table= {
        "banque":{ "main": [], "score": 0 },
        "joueurs": { }, #un dictionnaire de dictionaire avec clé le nom du joueurs et la valeur: main, mise,solde,score,statut,assurance etc...
        "places": [None]*nbdejoueurs
    }
    return table





## Vérification de saisie : demande une saisie à l'utilisateur et la compare à une liste d'options 
# valides. La fonction doit redemander la saisie tant qu'elle n'est pas correcte.

#pour les choix listé.
def veri_saisie_liste(optionvalide): 
    entrer_user=input('Veuillez entrer votre choix : ')
    entrer_user=entrer_user.upper()
    if entrer_user.isdigit():
        entrer_user=int(entrer_user)
    essaie=2
    while entrer_user not in optionvalide: 
        if essaie>0 : 
            print(f"Votre entrée n'est pas valide, veuillez reessayer.\nAttention !!! vous n'avez que {essaie} essaie{'s' if essaie>1 else''} restant, auxquels cas, vous serez exclu de la partie.")
            essaie-=1
            entrer_user=input('entrer votre choix : ')
            entrer_user=entrer_user.upper()
            if entrer_user.isdigit():
                entrer_user=int(entrer_user)
        else: 
            print("VOUS AVEZ DEPASSER LE COTA D'ENTRER INVALIDE.")
            return None 
    return entrer_user

#pour les intervalles
def veri_saisie_intervale(binf,bsup): 
    entrer_user=input('Veuillez entrer votre choix : ')
    if entrer_user.isdigit():
        entrer_user=int(entrer_user)
    else:
        entrer_user=-1
    essaie=2
    while entrer_user<binf or entrer_user>bsup: 
        if essaie>0 : 
            print(f"Votre entrée n'est pas valide, veuillez reessayer.\nAttention !!! vous n'avez que {essaie} essaie{'s' if essaie>1 else''} restant, auxquels cas, vous serez exclu de la partie.")
            essaie-=1
            entrer_user=input('Veuillez entrer votre choix : ')
            if entrer_user.isdigit():
                entrer_user=int(entrer_user)
            else:
                entrer_user=-1
        else: 
            print("VOUS AVEZ DEPASSER LE COTA D'ENTRER INVALIDE.")
            return None 
    return entrer_user






## Calcul de score :  Calculer la valeur d'une main de cartes.
# Prend une main (une liste de cartes) et retourne son score. Cette fonction doit gérer la double 
# valeur de l'As (1 ou 11) pour toujours donner le meilleur score possible sans dépasser 21. 
def score(main): #une main est une liste de dictionnaire de carte
    score=0 
    nb_as=0 
    for element in main: 
        score+=element["valeur"] 
        if element["numero"]=="AS": 
            nb_as+=1 
    while score>21 and nb_as>0: 
        score-=10
        nb_as-=1 
    return score 




### Ajouter un joueur :  Permettre à un nouveau joueur de rejoindre la partie.
def add_player(table,est_robot, etat_partie): #etat_partie et est_robot sont des  boleens de verification 
    if None not in table["places"]: 
        print("Vous ne pouvez pas ajouter de jouer, il n'y a pas de place disponible.")
        return None
    print("\n" + "="*40)
    print(Fore.CYAN + Style.BRIGHT +"--- AJOUT DE NOUVEAU JOUEUR/ROBOT ---")
    print("="*40)

    #initialisation de la stratégie
    strategie =None

    #Nom du  robot
    if est_robot:
        print("\n--- Ajout d'un Robot ---")
        print("Voulez-vous personnaliser son nom ? (O/N)")
        choix_nom = veri_saisie_liste(['O', 'N'])
        
        if choix_nom == 'O':
            nom_joueur = input("Nom personnalisé du robot : ") + " (Robot)"
        else:
            # Nom par défaut, on compte les robots existants
            robot_count = 1
            for j in table['joueurs'].values():
                if j['est_robot']:
                    robot_count += 1
            nom_joueur = f"Robot_{robot_count}"
        
        # Solde par défaut pour un robot
        soldeIn = 1000 
        print(f"Le robot {nom_joueur} est ajouté avec un solde de {soldeIn}$.")

        #Choix de la stratégie du ROBOT
        print("Quelle stratégie pour ce robot ?")
        print("(P)rudent/ (N)ormal / A)gressif") 
        # (P)rudent : Ne double/assure jamais.Tire jusqu'à 17.
        # (N)ormal: Fait tout aléatoirement
        # A)gressif :Double/Assure dès que possible. Tire jusqu'à 18.
        
        choix_strat = veri_saisie_liste(['P', 'N', 'A'])
        if choix_strat is None:
            print("Saisie invalide. Stratégie (N)ormale par défaut.")
            choix_strat = 'N'
        
        strategie = choix_strat #on l'ajoute à la fin pour un code unifié 
    
    #Nom du Joueur 
    else :
        print("\n--- Ajout d'un Joueur ---")
        #demande du nom du joueur 
        nom_joueur=input("Quel est votre nom ?\n (Par soucis d'affichage, il est interdit d'utiliser < None > ou toute variante possible.) :  ")
        print("\n\n")

        #demande du solde joueur
        print("Quelle est votre solde ?\nPar soucis d'affichage,veuillez entrer une valeur entre 1$ et 30.000$.\nVous ne pouvez pas ajouter de nombre à virgule)")
        soldeIn=veri_saisie_intervale(1,30000)
        #verification du respect des consignes par le joueur.
        if soldeIn is None:
            print( " Vous n'avez pas respecter les consignes. le programme d'ajout de joueur s'est arrêter, vous pourrez le relancer. ")
            return None  
        print("\n\n")


    # On vérifie si le nom (humain ou robot) existe déjà
    while nom_joueur in table["joueurs"].keys() or nom_joueur.lower() == "none":
        if nom_joueur.lower() == "none":
            nom_joueur = input("Vous avez entrer < None > alors que c'est interdit. \n Entrer votre nouveau choix : ")
        else:
            print(f"Ce nom '{nom_joueur}' est déjà utilisé.")
            if est_robot:
                nom_joueur = input("Nouveau nom personnalisé : ") + " (Robot)"
            else:
                nom_joueur = input("Veuillez en choisir un autre : ") 
    print("\n")

    #recherche des places disponiblent
    place_dispo=[]
    for i in range (len(table["places"])):
        if table["places"][i]==None:
            place_dispo.append(i)

    print(f"Il n'y a que {'la' if len(place_dispo)==1 else 'les'} place{'s' if len(place_dispo)>1 else''} :{place_dispo} de disponible{'nt' if len(place_dispo)>1 else ''}")

    #S'il n'y a qu'une seule place 
    if len(place_dispo)==1:
        place_joueur = place_dispo[0] # On mets directement le joueur à cette place 
        print(f"{'Le Robot sera 'if est_robot else'Vous serez'} donc ajouter à celle-ci")
        table["places"][place_joueur]= nom_joueur
    
    #S'il y a PLUSIEURS places
    else: 
        place_joueur = None # On initialise

        if est_robot:
            print("Souhaitez-vous choisir la place du robot (O/N)? ")
            choix_place = veri_saisie_liste(['O','N']) # Renommé pour éviter la confusion
            
            if choix_place == 'O':
                print("A quelle place souhaitez-vous mettre le robot ?\n(Veuillez juste entrer le chiffre)")
                place_joueur = veri_saisie_liste(place_dispo)
                
                #verification du respect des consignes par le joueur. 
                if place_joueur != None: 
                    table["places"][place_joueur] = nom_joueur
                    print(f"Le robot a bien été ajouter au jeu à la position demander=> {table['places']}")
                else : 
                    print( " Vous n'avez pas respecter les consignes. Le robot sera placé aléatoirement. ")
                    place_joueur = random.choice(place_dispo)
                    table["places"][place_joueur] = nom_joueur 
                    print(f"Le robot est placé aléatoirement à la place {place_joueur}.")
                    
            
            elif (choix_place == 'N') or choix_place==None: 
                place_joueur = random.choice(place_dispo)
                table["places"][place_joueur] = nom_joueur 
                print(f"Le robot est placé aléatoirement à la place {place_joueur}.")

        
        else: # C'est un humain (et il y a plusieurs places)
            print("A quelle place souhaitez-vous être ?\n(Veuillez juste entrer le chiffre)")
            place_joueur = veri_saisie_liste(place_dispo)
            
            #verification du respect des consignes par le joueur. 
            if place_joueur != None: 
                table["places"][place_joueur] = nom_joueur
                print(f"Vous avez bien été ajouter au jeu à la position demander=> {table['places']}")
            else : 
                print( " Vous n'avez pas respecter les consignes. Vous serez placé(e) aléatoirement. ")
                place_joueur = random.choice(place_dispo)
                table["places"][place_joueur] = nom_joueur 
                print(f"Vous êtes à la place {place_joueur}.")
    
    # FIN DE LA LOGIQUE DE PLACEMENT 

    #verification de l'etat de la partie pour determiner si joueur joue en meme temps ou pas 
    if etat_partie :
        print("\n\n")
        # On n'affiche le message qu'à l'humain
        if not est_robot: 
            print("Etant donné qu'une partie est en cours, vous ne pourrez pas jouer maintenant.\nVotre statut sera False pour dire que vous êtes en attente.")
        statJoueur=False  
    else:
        statJoueur=True
        print("\n\n")

    #Ajout du joueur/robot dans joeurs 
    table["joueurs"][nom_joueur]={"main":[],"score":0,"mise":0,"assurance":0,"solde":soldeIn,"statut":statJoueur,"soldeIn": soldeIn, "est_robot":est_robot, "strategie": strategie if est_robot else None} #On laisse vide la strat si c'est un humain #soldeIn pour le calcul des gains en fin dde partie si le joueur quitte
    print(f"{'le robot' if est_robot else 'Vous'}, {''if est_robot else 'M.'}{nom_joueur}, {'a'if est_robot else 'avez'} Bien été ajouté à la table. {'ses'if est_robot else 'vos'} informations sont les suivantes : {table['joueurs'][nom_joueur]}")
    return table


### Gestion des nouveau joueur au début de chaque nouvelle manche 
def gerer_nouveaux_joueurs(table):
    # Gère l'ajout de nouveaux joueurs avant le début d'une manche.
    # Utilise la fonction add_player.
    while True: # Boucle pour ajouter potentiellement plusieurs joueurs
        
        # 1. Vérifier s'il reste des places
        if None not in table["places"]:
            print("La table est complète. Impossible d'ajouter de nouveaux joueurs.")
            break # Sort de la boucle while
            
        # 2. Demander si quelqu'un veut s'ajouter
        print("\nSouhaitez-vous ajouter un nouveau joueur/Robot pour la prochaine manche ? (O/N)")
        choix = veri_saisie_liste(['O', 'N'])

        if choix == 'O':
            print("Est-ce un robot ? (O/N) ")
            choixR=veri_saisie_liste(['O', 'N'])
            if choixR=='O':
                est_robot=True
            elif choixR is None: 
                print("Vous n'avez pas respecter les consigne, veuillez recommencer ")
                continue #passe à l'itération suivante qui ici recommence l'ajout de joueur 
            else : #choix negatif
                est_robot=False 

            # On appelle add_player
            # On passe etat_partie=False car on est avant le début de la manche.
            
            # on vérifie d'abord si l'ajout a réussi.
            table_modifiee = add_player(table,est_robot, etat_partie=False) 
            if table_modifiee is None:
                # L'ajout a échoué (l'utilisateur a annulé)
                print("L'ajout du joueur a été annulé.")
            else:
                table = table_modifiee # Ré-assigne la table 
                print("Joueur ajouté avec succès.")

        elif choix == 'N':
            # L'utilisateur ne veut plus ajouter de joueur
            print("Aucun nouveau joueur ajouté.")
            break # Sort de la boucle while
            
        else: # Si veri_saisie_liste retourne None
            print("Saisie invalide. Annulation de l'ajout de nouveaux joueurs.")
            break # Sort de la boucle while
            
    return table


### Demande de la mise : Collecter les paris de début de manche.  
def mise(table) : 
    print("\n" + "="*40)
    print(Fore.YELLOW + Style.BRIGHT + "--- C'EST L'HEURE DE MISEYYY ---")
    print("="*40)
    for player in table["joueurs"].keys():
        joueur=table["joueurs"][player]
        
        #verrification du statut du joueur 
        if joueur["statut"]==True:

            #verification du solde 
            if joueur["solde"]>=1:
                
                # Mise des robots 
                if joueur["est_robot"]: 
                    mise_robot = 0
                    strat = joueur['strategie']
                    
                    if strat == 'P':
                        mise_robot = 20   # Le Prudent mise 20
                    elif strat == 'N':
                        mise_robot = 50   # Le Normal mise 50
                    elif strat == 'A':
                        mise_robot = 100  # L'Agressif mise 100

                    # On vérifie que le robot a assez sinon il met tout son solde
                    if joueur['solde'] < mise_robot:
                        mise_robot = joueur['solde']
                    
                    #actualisation de la table  
                    joueur["mise"] = mise_robot
                    joueur['solde'] -= mise_robot
                    print(f"M.{player} mise {mise_robot}$. (Solde: {joueur['solde']}$)")

      
                else:
                    print(f"Monsieur {player},\nVotre solde est de : {joueur['solde']}, la mise minimum est de 1$.\nCombien voulez vous miser pour cette manche ? (Vous ne pouvez pas entrer de nombre à virgule.)  : ")
                    mise_joueur=veri_saisie_intervale(1,joueur["solde"])
                    print("\n")

                    #verfication du respect des consignes par le joueurs 
                    if mise_joueur is None:
                        print("vous n'avez pas respecter les consignes. Vous jouerez au prochain tour.")
                        joueur["statut"]=False
                    else: 
                        print("Merci !! Votre solde mise a été enregistré et votre solde Actualisé.")
                        joueur["mise"]=mise_joueur
                        joueur["solde"]= joueur["solde"]-mise_joueur
                        print("\n")
                        print(f"Vos information actualisées sont les suivantes :\n {joueur}")
            else: #s'il n'a plus d'argent on l'exclu de la table 
                joueur["statut"] = False
                if not joueur['est_robot']:
                    print(f"Monsieur {player},\nVotre solde est de : {joueur['solde']}. Vous ne pouvez donc pas misé.\nJe vous invite donc à recharger votre solde ou quitter la table.")
        print("\n")
    return table 



### Distribution : Donner les deux premières cartes à tout le monde. 
def distribution(table,sabot):
    #distributon de 2 cartes à raison d'une à a foi par joueur 
    print("\n" + "="*40)
    print(Fore.BLUE + Style.BRIGHT + "--- DISTRIBUTION DES CARTES---")
    print("="*40)
    for i in range(2):
        for player in table['joueurs'].keys():
            joueur=table['joueurs'][player]
            #verification si le joueur est actif et distribution de la carte.
            if joueur['statut']==True:
                carte_donnee=piocher_carte(sabot)
                print(f"Le joueurs {player} reçoit la carte {carte_donnee['numero']}{carte_donnee['symbole']}")
                joueur['main'].append(carte_donnee)
                print(f"sa main est de {joueur['main']}")

                #calcul du score du joueur.  
                joueur['score']=score(joueur['main'])
                print(f"Son nouveau score est de {joueur['score']}")
                print("\n")

        #verification du nombre de carte de la banque et cacher la deuxieme 
        if i==0:
            banque=table['banque']
            carte_donnee=piocher_carte(sabot)
            print(f"La banque reçoit la carte {carte_donnee['numero']}{carte_donnee['symbole']}")
            banque['main'].append(carte_donnee)
            print(f"sa main est de {banque['main']}") 

            #calcul du score de la banque   
            banque['score']=score( banque['main'])
            print(f"Son nouveau score est de {banque['score']}")
        else :
            carte_donnee=piocher_carte(sabot)
            print(f"La banque reçoit une seconde carte, face caché. ")
            banque['main'].append(carte_donnee)
            banque['score']=score(banque['main'])
        print("\n")
    return table, sabot 




### Affichage de la Table: Montrer l'état du jeu aux joueurs en mode texte.
def etat_table(table): 
    print("\n" + "="*40)
    print(Fore.YELLOW + Style.BRIGHT + "--- ETAT DE LA TABLE ---")
    print("="*40)
    #affichage de la main de la  banque. 
    if len(table['banque']['main']) > 0:
        print(f" la main de la banque [{table['banque']['main'][0]} , carte masqué ]")
    
    #affichage de la main des joueurs 
    for i,player in enumerate(table['places']): #enumerate permet de prendre l'index et l'element
        if player==None: 
            print(f"La place {i} est vide.")
            print('\n')
        else:
            print(f" Le joueur {player} à la place {i} a misé {table['joueurs'][player]['mise']}")
            print(f"Sa main est de : {table['joueurs'][player]['main']}.")
            print(f"Et son score est de {table['joueurs'][player]['score']}.")
            print('\n')




### Tour des Joueurs :  Gérer le tour de chaque joueur actif, incluant les actions avancées.
def tours_joueurs(table,sabot):
    print("\n" + "="*40)
    print(Fore.YELLOW + Style.BRIGHT + "--- MESSIEURS/DAMES C'EST L'HEURE DE CHOISIR VOS ACTIONS ! ---")
    print("="*40)

    ### GESTION DE L'ASSURANCE :On vérifie si la carte visible de la banque est un As
    if table['banque']['main'][0]['numero']=='AS':
        print("!!! La carte visible de la Banque est un AS !!!")

        for player in table['joueurs'].keys():  # On ne propose qu'aux joueurs actifs
            joueur=table['joueurs'][player]

            if joueur['statut']==True: #lejoueur joue

                if joueur['est_robot']: #si c'est un robot 
                    print(f"\n> Assurance pour M.{player} ...")

                    #Le joueur ne peut pas mettre en assurance plus de la moité de sa mise initiale, ni au dela de son solde actuelle 
                    mise_max_assurance = joueur['mise'] / 2
                    limite_reelle = int(min(mise_max_assurance, joueur['solde']))
                    if limite_reelle < 1:
                        print(f"M.{player} n'a pas assez de solde pour s'assurer.")   
                    else:
                        strat = joueur['strategie']
                        choix_robot = 'N' # choix Par défaut

                        # Choix du robot selon la stratégie
                        if strat == 'P':
                            choix_robot = 'N' # Prudent : refuse toujours l'assurance 
                        elif strat == 'N':
                            choix_robot = random.choice(['O', 'N']) # Normal : 50/50
                        elif strat == 'A':
                            choix_robot = 'O' # Agressif : accepte toujours l'assure 
                        
                        #action selon le choix
                        if choix_robot == 'N':
                            print(f"Le robot {player} refuse l'assurance.")
                        else: # Le robot a choisi 'O'
                            assu_robot = 0
                            if strat == 'A':
                                assu_robot = limite_reelle # L'agressif mise le max
                            else: # Le Normal choisie aléatoirement
                                assu_robot = random.randrange(1, limite_reelle + 1)
                            #actualisation de la table 
                            joueur['assurance'] = assu_robot
                            joueur['solde'] -= assu_robot
                            print(f"M.{player} prend une assurance de {assu_robot}$.")


                else: #Si c'est un humain
                    print(f"Monsieur {player}") 
                    # On vérifie s'ils ont assez d'argent pour l'assurance  
                    mise_max_assurance = joueur['mise'] / 2
                    if joueur['solde'] >= 1:
                        print(f"Souhaitez vous prendre une assurance ? (O/N)")
                        choix_joueur = veri_saisie_liste(['O','N'])

                        if choix_joueur == 'O':
                            # Le joueur ne peut pas miser plus que la moitié de sa mise, ni plus que son solde
                            limite_reelle = int(min(mise_max_assurance, joueur['solde'])) #intt pour garantir un nombre rond au cas où la limite est decimal

                            if limite_reelle < 1:
                                print("Vous n'avez pas assez de solde pour prendre une assurance.")
                                continue # Passe au joueur suivant

                            print(f"Combien souhaitez vous mettre en assurance ? (Max: {limite_reelle}$)")
                            assu_joueur = veri_saisie_intervale(1, limite_reelle)
                            if assu_joueur is not None:
                                joueur['assurance'] = assu_joueur
                                # On déduit l'assurance du solde
                                joueur['solde'] -= assu_joueur
                                print(f"Votre assurance de {assu_joueur}$ a bien été prise en compte.")
                            else:
                                print("Saisie invalide. Nous considérons que vous ne prenez pas d'assurance.")
                        elif choix_joueur == 'N':
                            print("Votre choix a bien été pris en compte.")
                        else: # Si le joueur rate sa saisie O/N
                            print("Saisie invalide. Nous considérons que vous ne prenez pas d'assurance.")
                    else:
                        print(f"M. {player}, votre solde est insuffisant pour prendre une assurance.")

        print("\n" + "="*40)
        print("--- PLACE AUX JEUX ! ---")
        print("="*40)


    ### TOUR DES JOUEURS
    for player in table['joueurs'].keys(): 
        joueur=table['joueurs'][player]
        # On vérifie si le joueur est actif (il a misé et n'a pas été exclu)
        if joueur['statut']==True: 
            if joueur['est_robot']: #si c'est un robot
                print(f"\n--- Tour de M.{player} ---")
                print(f"Main: {joueur['main']} | Score: {joueur['score']})")
                strat = joueur['strategie']

                # STRATÉGIE DU PRUDENT
                # (Ne double jamais, tire jusqu'à 17)
                if strat == 'P':
                    while joueur['score'] < 17:
                        print(f" -> Le robot tire...")
                        carte_donnee = piocher_carte(sabot) 
                        joueur['main'].append(carte_donnee)
                        joueur['score'] = score(joueur['main'])
                        print(f" -> Carte: {carte_donnee['numero']}{carte_donnee['symbole']}. Nouveau score: {joueur['score']}")
                
                # STRATÉGIE DU NORMAL 
                # (Double 1 chance sur 3(sous conditions), sinon tire jusqu'à 17)
                elif strat == 'N':
                    peut_doubler = (len(joueur['main']) == 2 and joueur['solde'] >= joueur['mise'])
                    choix_robot_double = random.choice(['DOUBLER', 'NON', 'NON']) 

                    if peut_doubler and choix_robot_double == 'DOUBLER' and 9<=joueur['score']<=11 :
                        print(f"M.{player} décide de DOUBLER sa mise !")
                        mise_doublee = joueur['mise']
                        joueur['solde'] -= mise_doublee
                        joueur['mise'] += mise_doublee
                        carte_donnee = piocher_carte(sabot)
                        joueur['main'].append(carte_donnee)
                        joueur['score'] = score(joueur['main'])
                        print(f"Le robot tire sa carte unique: {carte_donnee['numero']}{carte_donnee['symbole']}. Score: {joueur['score']}")
                        if joueur['score'] > 21:
                            print("Bust !")
                            joueur['statut'] = False
                        continue # Tour terminé

                    # Si il n'a pas doublé, logique de banque
                    while joueur['score'] < 17:
                        print(f" -> Le robot tire...")
                        carte_donnee = piocher_carte(sabot) 
                        joueur['main'].append(carte_donnee)
                        joueur['score'] = score(joueur['main'])
                        print(f" -> Carte: {carte_donnee['numero']}{carte_donnee['symbole']}. Nouveau score: {joueur['score']}")

                # STRATÉGIE DE L'AGRESSIF 
                # (Double TOUJOURS si possible, sinon tire jusqu'à 18)
                elif strat == 'A':
                    peut_doubler = (len(joueur['main']) == 2 and joueur['solde'] >= joueur['mise'])

                    if peut_doubler:
                        print(f"M.{player} décide de DOUBLER sa mise !")
                        mise_doublee = joueur['mise']
                        joueur['solde'] -= mise_doublee
                        joueur['mise'] += mise_doublee
                        carte_donnee = piocher_carte(sabot)
                        joueur['main'].append(carte_donnee)
                        joueur['score'] = score(joueur['main'])
                        print(f"Le robot tire sa carte unique: {carte_donnee['numero']}{carte_donnee['symbole']}. Score: {joueur['score']}")
                        if joueur['score'] > 21:
                            print("Bust !")
                            joueur['statut'] = False
                        continue # Tour terminé
                    
                    # Si il n'a pas doublé, logique agressive
                    while joueur['score'] < 18: # Tire jusqu'à 18 !
                        print(f" ->Le robot tire...")
                        carte_donnee = piocher_carte(sabot) 
                        joueur['main'].append(carte_donnee)
                        joueur['score'] = score(joueur['main'])
                        print(f" -> Carte: {carte_donnee['numero']}{carte_donnee['symbole']}. Nouveau score: {joueur['score']}")
                
                # Résultat final du tour du robot (commun aux 3 strats)
                if joueur['score'] > 21:
                    print(f"M.{player} a BUST ! (Score: {joueur['score']})")
                    joueur['statut'] = False 
                else:
                    if joueur['statut']: # (Vérifie qu'il n'a pas bust en doublant)
                        print(f"M.{player} reste avec {joueur['score']} points.")
            
            else: #Si c'est un humain
                # Boucle pour la main principale du joueur
                # On utilise une variable pour contrôler la boucle 
                print(f"\n--- Tour de M.{player} ---")
                tour_en_cours = True
                while tour_en_cours:                 
                    print (f"\nVotre main est {joueur['main']}")
                    print(f"Et votre score est de {joueur['score']} ")
                    print(f"(Solde: {joueur['solde']}$ | Mise: {joueur['mise']}$)")

                    #Définition des actions possibles
                    options_actions = ['T', 'R'] # Tirer, Rester

                    # Vérification pour "Doubler" (Double Down)
                    peut_doubler = False
                    if (len(joueur['main']) == 2) and (joueur['solde'] >= joueur['mise']):
                        options_actions.append('D')
                        peut_doubler = True
                    
                    # Vérification pour "Split"
                    peut_splitter = False
                    if (len(joueur['main']) == 2) and (joueur['main'][0]['valeur'] == joueur['main'][1]['valeur']) and (joueur['solde'] >= joueur['mise']):
                        options_actions.append('S')
                        peut_splitter = True
                    
                    # Demande de l'action du joeur
                    print(f"Vos options sont : {options_actions}")
                    print(f"< T > pour Tirer, < R > pour Rester, {'< D > pour Doubler'if 'D' in options_actions else ''}, {'< S > pour Spliter' if 'S' in options_actions else ''}.")
                    #Conseilles
                    if peut_doubler and 9<=joueur['score']<=11:
                        print(f"Nous vous conseillons de Doubler")
                    else:
                        print(f"Nous vous conseillons de {'Tirer' if joueur['score'] < 17 else 'Rester'} ")
                    print(f"{'Nous vous conseillons aussi de spliter' if peut_splitter and 8<=joueur['score']<=16 else ''} ")                
                    choix = veri_saisie_liste(options_actions)
                    if choix is None:
                        print("Nous considérons que vous restez.")
                        choix = 'R' # Par défaut, on "Reste"
                    
                    # Exécution des actions 
                    if choix == 'T':
                        # ACTION: TIRER
                        carte_donnee = piocher_carte(sabot)
                        joueur['main'].append(carte_donnee)
                        joueur['score'] = score(joueur['main'])
                        print(f"Vous tirez la carte {carte_donnee['numero']}{carte_donnee['symbole']}. Nouveau score: {joueur['score']}")
                        #verification du score.
                        if joueur['score'] > 21:
                            print("BUST ! Vous avez dépassé 21.")
                            joueur['statut'] = False # Le joueur a perdu
                            tour_en_cours = False # Arrête la boucle 'while' pour ce joueur, et passe au suivant 
                    
                    elif choix == 'R':
                        # ACTION: RESTER
                        print(f"M.{player} reste avec {joueur['score']} points.")
                        tour_en_cours = False # Arrête la boucle 'while' pour ce joueur, et passe au suivant 
                    
                    elif choix == 'D' and peut_doubler:
                        # ACTION: DOUBLER
                        print("Vous doublez votre mise !")

                        # Payer la mise supplémentaire
                        mise_doublee = joueur['mise']
                        joueur['solde'] -= mise_doublee
                        joueur['mise'] += mise_doublee

                        # Donner UNE seule carte
                        carte_donnee = piocher_carte(sabot)
                        joueur['main'].append(carte_donnee)
                        joueur['score'] = score(joueur['main'])

                        print(f"Vous tirez votre unique carte: {carte_donnee['numero']}{carte_donnee['symbole']}.")
                        print(f"Score final: {joueur['score']}")
                        
                        if joueur['score'] > 21:
                            print("BUST !")
                            joueur['statut'] = False
                        tour_en_cours = False # Tour terminé quoi qu'il arrive

                    elif choix == 'S' and peut_splitter:
                        # ACTION: SPLITTER
                        print("Alors M.{player} decide de split huh...")
                        print("VOUS SEPAREZ VOTRE MAIN ! ")

                        # Payer la mise pour la nouvelle main
                        mise_split = joueur['mise']
                        joueur['solde'] -= mise_split
                    
                        # Création de  la structure pour la Main 2
                        carte_a_deplacer = joueur['main'].pop(1) # Retire la 2e carte
                        joueur['main2'] = [carte_a_deplacer]
                        joueur['mise2'] = mise_split
                        joueur['statut2'] = True # Statut pour la 2e main
                    
                        # Distribution d'une nouvelle carte sur chaque main
                        print("Distribution d'une carte sur chaque main...")
                        joueur['main'].append(piocher_carte(sabot))
                        joueur['main2'].append(piocher_carte(sabot))
                    
                        # Recalcule les scores
                        joueur['score'] = score(joueur['main'])
                        joueur['score2'] = score(joueur['main2'])

                        # --- Jouer la Main 1 ---
                        print(f"\n--- M.{player}, vous jouez votre PREMIÈRE main ---")
                        tour_main_1 = True
                        while tour_main_1:
                            print(f"Main 1: {joueur['main']} (Score: {joueur['score']})")
                            
                            # On ne peut plus splitter ou doubler après un split
                            choix_main_1 = veri_saisie_liste(['T', 'R'])
                            if choix_main_1 == 'T':
                                carte_donnee = piocher_carte(sabot)
                                joueur['main'].append(carte_donnee)
                                joueur['score'] = score(joueur['main'])
                                print(f"Main 1 - Vous tirez {carte_donnee['numero']}{carte_donnee['symbole']}. Score: {joueur['score']}")
                                
                                if joueur['score'] > 21:
                                    print("BUST ! (Main 1)")
                                    joueur['statut'] = False
                                    tour_main_1 = False

                            elif choix_main_1 == 'R':
                                print(f"Vous restez sur la Main 1 avec {joueur['score']} points.")
                                tour_main_1 = False
                            else: # Si le joueur rate sa saisie
                                print("Saisie invalide. Nous considérons que vous restez (Main 1).")
                                tour_main_1 = False

                        # --- Jouer la Main 2 ---
                        print(f"\n--- M.{player}, vous jouez votre DEUXIÈME main ---")
                        tour_main_2 = True
                        while tour_main_2:
                            print(f"Main 2: {joueur['main2']} (Score: {joueur['score2']})")
                            choix_main_2 = veri_saisie_liste(['T', 'R'])
                            
                            if choix_main_2 == 'T':
                                carte_donnee = piocher_carte(sabot)
                                joueur['main2'].append(carte_donnee)
                                joueur['score2'] = score(joueur['main2'])
                                print(f"Main 2 - Vous tirez {carte_donnee['numero']}{carte_donnee['symbole']}. Score: {joueur['score2']}")

                                if joueur['score2'] > 21:
                                    print("Bust ! (Main 2)")
                                    joueur['statut2'] = False
                                    tour_main_2 = False

                            elif choix_main_2 == 'R':
                                print(f"Vous restez sur la Main 2 avec {joueur['score2']} points.")
                                tour_main_2 = False
                            else: # Si le joueur rate sa saisie
                                print("Saisie invalide. Nous considérons que vous restez (Main 2).")
                                tour_main_2 = False
                        # Le tour du joueur (avec ses deux mains) est maintenant terminé
                    
                        tour_en_cours = False # Arrête la boucle 'while' principale

            # Fin du bloc pour les choix d'action
            # La boucle 'while tour_en_cours' se répète si 'T' a été choisi et score <= 21  
            print(f"--- Fin du tour pour M.{player} ---")

    # Fin de la boucle 'for player in...'
    print("\n" + "="*30)
    print("Tous les joueurs ont terminé leur tour.")
    print("="*30 + "\n")

    return table, sabot



### Tour de la Banque (Procédure) : La banque révèle sa carte et joue.
def tour_banque(table, sabot):
    # Gère le tour de la banque.
    # Révèle la carte cachée et tire jusqu'à 17 ou plus.
    print("\n" + "="*30)
    print(Fore.RED + Style.BRIGHT +"--- TOUR DE LA BANQUE ---")
    print("="*30)
    banque=table['banque']
    print("\n")
    # Révéler la main complète et le score
    print(f"La banque révèle sa main complète : {banque['main']}")
    print(f"Score initial de la banque : {banque['score']}")

    # Règle : la banque tire tant que son score est inférieur à 17
    while banque['score'] < 17:
        print("\n")
        print("La banque a moins de 17, elle tire une carte...")
        
        # Tirer une carte 
        carte_donnee = piocher_carte(sabot)
        banque['main'].append(carte_donnee)
        
        # Recalculer le score 
        banque['score'] = score(banque['main'])
        
        print(f"La banque tire la carte {carte_donnee['numero']}{carte_donnee['symbole']}.")
        print(f"Nouveau score de la banque : {banque['score']}")

    print("\n")
    # Fin du tour de la banque
    if banque['score'] > 21:
        print("La banque a BUST ! (Dépasse 21)")
    else:
        print(f"La banque s'arrête à {banque['score']}.")
    
    # Stocker le score final
    banque['score'] = score(banque['main'])
    return table, sabot




### Résultats et Paiements (Procédure) : Comparer chaque joueur à la banque.
def determiner_resultats(table):
    # Compare le score de chaque joueur à celui de la banque et met à jour les soldes.
    # (Version corrigée)

    print("\n" + ">"*30)
    print(Fore.GREEN + Style.BRIGHT +"--- C'EST L'HEURE DES RESULTAAAAATS---")
    print("<"*30)

    # Récupérer les infos de la banque
    score_banque = table['banque']['score'] #Recup le score de la banque 
    banque_a_bust = score_banque > 21 #true si la banque a bust(perdue)
    banque_a_blackjack = (score_banque == 21 and len(table['banque']['main']) == 2) #true si la banque a fait un blckJck 
    
    print(f"La banque a {score_banque}. {'( Bust !! )' if banque_a_bust else ''}")

    # Parcourir tous les joueurs
    for player in table['joueurs'].keys():
        joueur = table['joueurs'][player]
        
        # On ignore UNIQUEMENT si le joueur n'a pas de mise.
        if joueur['mise'] == 0:
            continue # Ce joueur n'a pas joué, on passe au suivant.
            
        print(f"\n--- Résultats pour M.{player} ---")
        
        # 1. PAIEMENT DE L'ASSURANCE
        if joueur['assurance'] > 0:
            if banque_a_blackjack:
                gain_assurance = joueur['assurance'] * 2 # Paiement 2:1
                print(f"La banque a un Blackjack ! M.{player} gagne son assurance de {joueur['assurance']}$.")
                joueur['solde'] += joueur['assurance'] + gain_assurance 
            else:
                print(f"La banque n'a pas de Blackjack. M.{player} perd son assurance de {joueur['assurance']}$.")
                # Le solde a déjà été déduit

        # 2. PAIEMENT DE LA MAIN PRINCIPALE 
        print(f"Votre main {'principale'if 'main2'in joueur else ''} comptabilise {joueur['score']} points :")
        joueur_score = joueur['score']
        joueur_a_blackjack = (joueur_score == 21 and len(joueur['main']) == 2)
        
        # On se base sur le score, pas sur le statut
        if joueur_score > 21:
            print(Fore.RED + f" Votre Main {'principale'if 'main2'in joueur else ''} a BUST !! (Score: {joueur_score}points). Vous perdez {joueur['mise']}$.")
            # (Perte : ne rien faire, la mise est déjà déduite)

        elif joueur_a_blackjack and not banque_a_blackjack:
             print(Fore.GREEN + Style.BRIGHT + f" > BLACKJACK !!! Vous gagnez 150% sur votre mise de {joueur['mise']}$.")
             gain = joueur['mise'] * 1.5
             joueur['solde'] += joueur['mise'] + gain # Rendre la mise + gain
        elif banque_a_bust:
             print(Fore.GREEN + f" > La banque a BUST ! Vous gagnez {joueur['mise']}$.")
             joueur['solde'] += joueur['mise'] * 2 # Rendre la mise + gain (100%)
        elif joueur_score > score_banque:
             print(Fore.GREEN + f" > Vous gagnez contre la banque ({joueur_score} vs {score_banque}). Vous gagnez {joueur['mise']}$.")
             joueur['solde'] += joueur['mise'] * 2 # Rendre la mise + gain (1:1)
        elif joueur_score == score_banque:
             print(Fore.BLUE + f" > Égalité ! Votre mise de {joueur['mise']}$ vous est rendue.")
             joueur['solde'] += joueur['mise'] # Rendre la mise
        else: # Perdu (joueur < banque)
             print(Fore.RED + f" > Vous perdez contre la banque ({joueur_score} vs {score_banque}). Vous perdez {joueur['mise']}$.")
             # (Perte : ne rien faire)

        # 3. PAIEMENT DE LA MAIN 2 (si elle existe)
        if 'main2' in joueur:
            print(f"Votre deuxième main comptabilise {joueur['score2']} points :")
            joueur_score_2 = joueur['score2']
            
            if joueur_score_2 > 21:
                print(Fore.RED + f" > Votre deuxième main a BUST !! (Score: {joueur_score_2}). Vous perdez {joueur['mise2']}$.")
            elif banque_a_bust:
                print(Fore.GREEN + f" > La banque a BUST. Vous gagnez {joueur['mise2']}$ (deuxième mise).")
                joueur['solde'] += joueur['mise2'] * 2
            elif joueur_score_2 > score_banque:
                print(Fore.GREEN + f" > Votre deuxième main gagne ({joueur_score_2} vs {score_banque}). Vous gagnez {joueur['mise2']}$.")
                joueur['solde'] += joueur['mise2'] * 2
            elif joueur_score_2 == score_banque:
                print(Fore.BLUE + f" > Égalité ! Votre mise de {joueur['mise2']}$ vous est rendue.")
                joueur['solde'] += joueur['mise2']
            else: # Perdu
                print(Fore.RED + f" > Votre deuxième main perd ({joueur_score_2} vs {score_banque}). Vous perdez {joueur['mise2']}$.")
        
        print(f"Nouveau solde pour M.{player} : {joueur['solde']}$")

    return table



### Réinitialiser la table : Nettoie la table pour la manche suivante.
# Réinitialise les mains, scores, mises, assurances. Active les joueurs en attente ou ceux qui ont assez d'argent.
# Supprime les clés de split ('main2', etc.).
def reinitialiser_manche(table):
    print("\n" + "*"*40)
    print(Fore.BLUE + Style.BRIGHT +"--- PREPARATION DE LA NOUVELLE MANCHE ---")
    print("*"*40)
    
    # Réinitialiser la banque
    table['banque']['main'] = []
    table['banque']['score'] = 0
    
    # Boucle sur les joueurs
    # On utilise .list() pour copier les clés, car on ne peut pas 
    # supprimer un joueur de la table pendant qu'on itère dessus
    for player in list(table['joueurs'].keys()):
        joueur = table['joueurs'][player]
        
        # Réinitialiser les champs de base
        joueur['main'] = []
        joueur['score'] = 0
        joueur['mise'] = 0
        joueur['assurance'] = 0
        
        # Supprimer les clés de split si elles existent
        if 'main2' in joueur:
            del joueur['main2']
        if 'score2' in joueur:
            del joueur['score2']
        if 'mise2' in joueur:
            del joueur['mise2']
        if 'statut2' in joueur:
            del joueur['statut2']
            
        # Mettre à jour le STATUT
        # Si le joueur a 1$ ou plus, il devient/reste actif
        if joueur['solde'] >= 1:
            if joueur['statut'] == False:
                print(f"Le joueur {player} (en attente) rejoint la partie.")
                joueur['statut'] = True
        else:
            # Si le joueur n'a plus d'argent
            print(f"Le joueur {player} n'a plus d'argent et est retiré de la table.")
            
            # Trouver sa place et la vider
            for i, place_nom in enumerate(table['places']):
                if place_nom == player:
                    table['places'][i] = None
                    break #on s'arrête dès qu'on a trouver le joueurs 
            
            # Suppression du dictionnaire du  'joueurs'
            del table['joueurs'][player]
            
    return table







# -------------------
# Programme principal
# -------------------

def Black_Jack():
    print(Fore.YELLOW + Style.BRIGHT + "--- ♠ ♥ BIENVENUE AU BLACK JACK ♦ ♣ ---")
    
    # On initialise 'table' et 'sabot'
    table = {} 
    sabot = []

    try:
        # On ESSAIE d'ouvrir le fichier
        with open(FICHIER_SAUVEGARDE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # On vérifie si le fichier est vide 
            if not data or 'table' not in data:
                 raise FileNotFoundError # Traiter comme un fichier non trouver 

        # Si on est ici, c'est que le fichier existe ET est valide
        print("Partie sauvegardée trouvée. (O)uvrir ou (N)ouvelle ? ")
        action = veri_saisie_liste(['O', 'N']) 
        
        if action == 'O':
            table = data['table'] 
            sabot = data['sabot']
            print("Partie chargée.")
        
        # Si 'N' ou None, 'table' reste {}, et le bloc 'if not table:' s'enclenchera.
    
    except FileNotFoundError:
        # 4. Si le 'try' a échoué (fichier non trouvé OU vide)
        # On ne fait rien, 'table' est vide.
        pass 
    except Exception as e:
        # 5. Gère les fichiers JSON corrompus
        print(f"Erreur (fichier corrompu?). Une nouvelle partie va commencer. ({e})")
        table = {} # Force la réinitialisation


    # Si c'est une nouvelle partie (si 'table' est vide)
    if not table: 
        print("\n" + "="*40)
        print(Fore.YELLOW + Style.BRIGHT +"--- CREATION D'UNE NOUVELLE PARTIE---")
        print("="*40)
        
        # Chargement du sabot
        sabot = charger_sabot("cartes.json", 6) 
        
        # Initialisation de la table
        print("Combien de places à la table ? (5 places maximum )")
        nb_places = veri_saisie_intervale(1,5)
        if nb_places is None: 
            print("Saisie invalide. 5 places par défaut.")
            nb_places = 5 # Par défaut
        
        table = table_jeu(nb_places)
        
        # AJOUT DES NOUVEAUX JOUEURS 
        table = gerer_nouveaux_joueurs(table)
        
        # On vérifie s'il y a au moins un joueur
        if not table['joueurs']:
             print("Aucun joueur n'a été ajouté. La partie ne peut pas commencer.")
             return # Quitte le programme

    # Boucle de Jeu Principale 
    partie_en_cours = True
    while partie_en_cours:

        # 1. Préparer la manche (Retirer joueurs sans solde, activer les nouveaux)
        table = reinitialiser_manche(table) 

        # 1b. Gérer les nouveaux joueurs (avant les mises)
        table = gerer_nouveaux_joueurs(table)
        
        # S'il n'y a plus de joueurs actifs
        joueurs_actifs = [j for j in table['joueurs'].values() if j['statut']]
        if not joueurs_actifs:
            print("Il n'y a plus de joueurs actifs à la table. Fin du jeu.")
            # On supprime la sauvegarde si la table est vide
            try:
                with open(FICHIER_SAUVEGARDE, 'w', encoding='utf-8') as f:
                    json.dump({}, f) # Écrit un dictionnaire vide
            except Exception as e:
                print(f"Impossible d'effacer la sauvegarde: {e}")

            break

        print("\n" + "="*40)
        print(Fore.YELLOW + Style.BRIGHT + "--- NOUVELLE MANCHE ---")
        print("="*40)

        # 2. Demander les mises
        table = mise(table) 

        # 3. Distribuer les cartes
        table, sabot = distribution(table, sabot) 

        # 4. Afficher la table (carte caché)
        etat_table(table) 

        # 5. Tour des joueurs (gère assurance, split, double)
        table, sabot = tours_joueurs(table, sabot) 

        # 6. Tour de la banque
        table, sabot = tour_banque(table, sabot) 

        # 7. Déterminer les gagnants et payer
        table = determiner_resultats(table) 

        # 9. Demander si on continue
        print("\n" + "-" * 30)
        print("(S)auvegarder et Quitter, (Q)uitter, ou (C)ontinuer ? ")
        
        # verification 
        action = veri_saisie_liste(['S', 'Q', 'C'])

        if action == 'Q':
            partie_en_cours = False
            
            # On ne peut pas supprimer donc on ÉCRASE avec un fichier vide
            try:
                with open(FICHIER_SAUVEGARDE, 'w', encoding='utf-8') as f:
                    json.dump({}, f) # Écrit un dictionnaire vide
            except Exception as e:
                print(f"Impossible d'effacer la sauvegarde: {e}")
                
        elif action == 'S':
            with open(FICHIER_SAUVEGARDE, 'w', encoding='utf-8') as f:
                data = {"table": table, "sabot": sabot} 
                json.dump(data, f, indent=2, ensure_ascii=False)
            print("Partie sauvegardée. Au revoir !")
            partie_en_cours = False
        
        elif action == 'C':
            # On ne fait rien, la boucle 'while' va simplement recommencer
            pass 
        
        elif action is None: # Si le joueur a fait trop d'erreurs
            print("Trop d'erreurs de saisie. On continue la partie par défaut.")
            # On continue par défaut
            pass

    print("\nMerci d'avoir joué !")





#
# --- Lancement du Programme ---
#
Black_Jack()