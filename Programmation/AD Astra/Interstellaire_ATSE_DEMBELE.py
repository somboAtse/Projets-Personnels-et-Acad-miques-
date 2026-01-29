##################################### PROJET VOYAGE INTERSTELLAIRE #####################################################

# --------------------------

# Importations de librairies

# --------------------------


import pygame as pg

import sys

import random

import math

from pygame import mixer

# --------------------------

# Constantes du programme

# --------------------------



### Initiation Pygame

pg.init()



###---- VISUALISATON ET PARTIE GRAPHIQUE ----###

LARGEUR , HAUTEUR = 800, 600

FPS = 60


#Taille du vaisseau

vaisseauL, vaisseauH = 150,150 



##--Images, sons , icône(si possible), police 

### IMAGES ###

Ad_Astra_logo=pg.transform.scale(pg.image.load('image/AdAstraLog.png'),(400,200))
Ad_Astra_logoI=pg.image.load('image/AdAstraLog.png')
#vaisseau
vaisseau_img_C= pg.transform.scale(pg.image.load("image/vaisseau_centre.png"), (vaisseauL,vaisseauH))
vaisseau_img_G= pg.transform.scale(pg.image.load("image/vaisseau_gauche.png"), (vaisseauL,vaisseauH))
vaisseau_img_D= pg.transform.scale(pg.image.load("image/vaisseau_droite.png"), (vaisseauL,vaisseauH))
vaisseau_img_H= pg.transform.scale(pg.image.load("image/vaisseau_haut.png"), (vaisseauL,vaisseauH))
vaisseau_img_B= pg.transform.scale(pg.image.load("image/vaisseau_bas.png"), (vaisseauL,vaisseauH))

# background et defilement et son
background = pg.image.load("image/background2.png")
bg_heigt= background.get_height() #hauteur de notre image
tiles= math.ceil(LARGEUR/bg_heigt)  # combien d'image de notre bckgrnd faut-il pour remplir la fenetre de jeu ? en l'occurence une seule suffit.
scroll = 0 # défilement du bckgrnd

#son du bckgrd
mixer.music.load("sounds/background.wav")



# Astéroids
AstR= pg.image.load("image/astRouge.png") #pg.transform.scale(pg.image.load("image/astRouge.png"), (70,70))
AstO= pg.image.load("image/astOrange.png") #pg.transform.scale(pg.image.load("image/astOrange.png"), (50,50))
AstV= pg.image.load("image/astVert.png") #pg.transform.scale(pg.image.load("image/astVert.png"), (30,30))
debrImg= pg.transform.scale(pg.image.load("image/debris.png"),(50,50)) 


#son des tir 
shot_sound= mixer.Sound("sounds/laser.wav")

#son et image  des esplosion obstacles
xplose = mixer.Sound("sounds/explosion.wav")
xploseImg = pg.image.load("image/explosion.png")

#sons collision vaisseau
choc_vaiss_sound=mixer.Sound("sounds/shockVaisseau.ogg")
choc_shield_sound=mixer.Sound("sounds/shockBouclier.ogg")
xplose_vaiss_sound= mixer.Sound("sounds/xploseVaisseau.ogg")

#image bonus 
bonusImg= pg.image.load("image/bonusplus.png") #pg.transform.scale(pg.image.load("image/astRouge.png"), (70,70))
#sons bonnus 
bonusPlus_sound=mixer.Sound("sounds/bonnusPlus.ogg")



# soleil et postion
sun = pg.transform.scale(pg.image.load("image/sun.png"),(200,100))
sun_X = 700
sun_Y = 0

#lune et position
moon = pg.transform.scale(pg.image.load("image/moon.png"),(200,100))
moon_X = -10
moon_Y = 500


### POLICES ###

score_font = pg.font.Font('font/Minecraft.ttf',35)
over_font = pg.font.Font('font/Daydream_DEMO.otf',50)
congrat_font = pg.font.Font('font/Slugs Racer.ttf',35)


#Gestion des Couleurs

BLEU = (10,10,20)

BLEU_n= (50, 50, 100)

BLEU_c = (0,255,255)

NOIR= (0,0,0)

VERT_biz= (50,100,20)

GRIS = (137,137,137)

ROUGE=(255,0,0)

Bleu_dragée = (223, 242, 255)

bleu_charette = (142, 162, 198)

OR_met = (212, 175, 55)

ORANGE = (255, 140, 0)







#Paramètre spécifique

VITESSE_DEFILEMENT = 5  # ce qui represente reellement la vitesse du vaisseau

SENSI_DEPLACEMENT = 6  # Anciennement VAISSEAU_VITESSE


#Definition des modèles (Dictionnaire) :

vaisseau = {

    "vssX": ((LARGEUR//2)-(vaisseauL//2)), # on centre en fonction de la largeur

    "vssY": ((HAUTEUR//2)-(vaisseauH//2)), # on centre en fonction de la hauteur

    "image": vaisseau_img_C, #image du vaisseau

    "vitesse": SENSI_DEPLACEMENT,

    "rect": pg.Rect((LARGEUR // 2),HAUTEUR - 100, vaisseauL,vaisseauH,),  # ce serait pas plutôt la position x et y du vaisseau

    "vie": 9,

    "z" : 0,  # peut aider à pouvoir mieux gérer la collision

    "bouclier" : False,
    "bouclier_chg" : 50, # à remettre à zéro plus tard
    "bouclier_max" : 100,
    "bouclier_clr" : BLEU_c,



    "rl" : vaisseauL//2, #rayon en fonction de L (X)
    "rh" : vaisseauH//2  # rayon en fonction de H (Y)

}


#Elaboration des objets
#Obstacles
def creer_obstacle(x_tnl,y_tnl):

    rayon = random.choice([30,50,70])

    if rayon == 30 : 
        astImg = AstV
        vie=1
        mod="V"
    elif rayon == 50 : 
        astImg=AstO 
        vie=2 
        mod="O"
    elif rayon == 70 :
        astImg= AstR
        vie=3
        mod="R"
       

    #Décalage aleatoire par zone
    set_x = random.randint(-200,200)
    set_y = random.randint(-200,200)
    ast = {

        "type": "obstacle",

        "x": x_tnl + set_x, # random.randint(0, LARGEUR+1) , #on va les considérer comme des event aleatoire par zone da la fénêtre

        "y":  y_tnl + set_y, # random.randint(0, HAUTEUR+1),

        "z": nb_anneaux * profondeur,

        "r": rayon,

        "actif": True,

        "image" : astImg,

        "vie" : vie,

        "typAst" : mod
    }

    return ast

def debris_xplose(parent_obs, l_obs):

    # On décide combien d'éclats on veut (entre 3 et 5 par exemple)
    nb_debris = 5
    
    for i in range(nb_debris):

        # position aléatoire autour de l'obstacle 
        decalage_x = random.randint(-40, 40)
        decalage_y = random.randint(-40, 40)
        
        debris = {
            "type": "obstacle", # On les traite comme des obstacles normaux

            "x": parent_obs["x"] + decalage_x,

            "y": parent_obs["y"] + decalage_y,

            "z": parent_obs["z"] + random.randint(10, 50), # un peu derriere pour l'effet visuelle 

            "r": (parent_obs["r"]//nb_debris), # Rayon beaucoup plus petit

            "actif": True,

            "image": debrImg, # On réutilise la même image

            "typAst" : "V", # vue que ce sont des débris ils seront de type vert( peu d'effet sur les vies du vaisseau ) 
 
            "vie": 1 
        }
        
        
        l_obs.append(debris)



#Tirs
def creer_tirs(vss):

    tir = {
        "type": "tirs",
        "x": vss["vssX"] + vss["rl"],  # Centre du vaisseau

        "y": vss["vssY"] + vss["rh"],

        "z": 0,  # Part du vaisseau

        "r": 25,  # Petit rayon

        "actif": True
    }
    return tir






#Bonus
def creer_bonus(x_tnl, y_tnl):

    # Décalage aleatoire par zone
    set_x = random.randint(-100, 100)
    set_y = random.randint(-100, 100)
    pdv = {

        "type": "bonus",

        "x": x_tnl + set_x,

        "y": y_tnl + set_y,

        "z": nb_anneaux * profondeur,

        "r": 50,

        "actif": True,

        "image" : bonusImg 
    }

    return pdv


# ---------------

# Sous-programmes

# ---------------


# gestion du defilement des obstacles
def obstacle_defil(obs : dict):  # ou gerer les obstacles
    obs["z"] -= VITESSE_DEFILEMENT

    #si l'anneau sort de notre champs de vision on le supprime de la liste obstacles
    if obs["z"] < 0 :
        obs["actif"]=False

#Gestion des tirs
def tirs_defil_gest(l_tirs, l_obs,l_xplose):

    global VITESSE_DEFILEMENT

    for tir in l_tirs:
        tir["z"] += VITESSE_DEFILEMENT + 50 #Vitesse du laser

        #Si trop loin par rapport à obstacle
        if tir["z"] > nb_anneaux * profondeur :
            tir["actif"] = False

        #Si collision avec obstacle
        for obs in l_obs:
            if obs["actif"]:
                #Si tir et obs ont la même profondeur
                if  abs(tir["z"] - obs["z"]) < 100:
                    dist = math.sqrt((tir["x"] - obs["x"])**2 + (tir["y"] - obs["y"])**2)

                    if dist < (tir["r"] + obs["r"]):
                        obs["vie"]-=1
                        tir["actif"] = False #tir disparait avec obs
                        if obs["vie"]==0:
                        #Boom
                            obs["actif"] = False #obs détruit
                            xplose.play()
                            nouvelle_exp = {
                                "type": "explosion",
                                "x": obs["x"],
                                "y": obs["y"],
                                "z": obs["z"], # Même profondeur
                                "r": obs["r"], # Même taille
                                "timer": 15    # Elle durera 15 images (1/4 de seconde)
                            }
                            l_xplose.append(nouvelle_exp)

                            if obs["r"]>30: #s'pplique seulement aux obstacles rouge et orange. 
                                debris_xplose(obs,l_obs)
                                
#Gestion des bonus
def bonus_defil(bns : dict):  # ou gérer les bonus
    bns["z"] -= VITESSE_DEFILEMENT

    #si l'anneau sort de notre champs de vision on le supprime de la liste obstacles
    if bns["z"] < 0 :
        bns["actif"]=False

# Detection de collision
def verif_collision_obs(vss, l_obs): # vérifie si vss touche un obstacle et retourne true ou false
    global VITESSE_DEFILEMENT

    vss_rayon = vss["rl"]*0.4
    vss_ctr_x = vss["vssX"] + vss["rl"]
    vss_ctr_y = vss["vssY"] + vss["rh"]

    marge_collision = 20

    for obs in l_obs:
        #collision si l'obstacle est à hauteur du vaisseau
        #Avec une marge d'erreur de Z=0 à Z=50

        if -marge_collision <= obs["z"] < (VITESSE_DEFILEMENT + marge_collision):
        #prend les coordonnées de l'obsacle
            o_x = obs["x"]
            o_y = obs["y"]
            o_ray = obs["r"]

        #Formule de distance entre deux centres
            dist = math.sqrt((vss_ctr_x - o_x)**2 + (vss_ctr_y - o_y)**2)
            if dist < (vss_rayon + o_ray):
                if vss["bouclier"] == True :
                    if obs["typAst"]== "V" : 
                        vss["bouclier_chg"]-=1
                    elif obs["typAst"]== "O" :
                        vss["bouclier_chg"]-=2
                    elif obs["typAst"]== "R" :
                        vss["bouclier_chg"]-=3
                    choc_shield_sound.play()
                    return False
                else :
                    if obs["typAst"]== "V" : 
                        vss["vie"]-=1
                    elif obs["typAst"]== "O" :
                        vss["vie"]-=2
                    elif obs["typAst"]== "R" :
                        vss["vie"]-=3
                    choc_vaiss_sound.play()
                    return True #KABOOM

    return False


# collision avec les bonus 

def verif_collision_bonus(vss, l_bns):
    
    vss_rayon = vss["rl"] * 0.5 
    vss_ctr_x = vss["vssX"] + vss["rl"]
    vss_ctr_y = vss["vssY"] + vss["rh"]
    
    marge_collision = 20

    for bns in l_bns:
        # 1. Vérification de la Profondeur (Z)
        if -marge_collision <= bns["z"] < (VITESSE_DEFILEMENT + marge_collision):
            
            # 2. Vérification de la Distance (X, Y)
            b_x = bns["x"]
            b_y = bns["y"]
            b_ray = bns["r"]
            
            dist = math.sqrt((vss_ctr_x - b_x)**2 + (vss_ctr_y - b_y)**2)
            
            # 3. Verdict
            if dist < (vss_rayon + b_ray):
                bonusPlus_sound.play()
                return True # MIAM !

    return False


#Gestion du Bouclier
def gest_bouclier(vss,vts_act):
    #Vérifie que le bouclier est inactif
    
    if vss["bouclier"] == False :
        if vss["bouclier_chg"] < vss["bouclier_max"]:
            vss["bouclier_chg"] += 2 / (1 * 60)
            
    elif vss["bouclier"] == True :
        vss["bouclier_chg"] -= 5 / (1 * 60)
        if vss["bouclier_chg"] <= 0 :
            vss["bouclier_chg"] = 0
            vss["bouclier"] = False

#Gestion de bone
#Visualisation du jeu

##-- affichage du vaisseau

def vaisseau_aff(x,y) :
    global vaisseau
    fenetre.blit(vaisseau["image"], (x,y))
    if vaisseau["bouclier"] == True :
        pg.draw.circle(fenetre, vaisseau["bouclier_clr"], (vaisseau["vssX"]+vaisseau["rl"], vaisseau["vssY"]+vaisseau["rh"]),80,3)



###----- Formatons du tunnel -----###

'''NOTES A MOI MEME :
_Penser à accorder la sensi_vaisseau à la vitesse du vaisseau #
_Si tu sors du tunnel, tu meurs. #*Joel* Trop compliqué pour le joueur dans les jeux ils sont justes coller et remonte ou descende en fonction de la direction
_Certain objets que tu cognes diminue ta vie
_Des objets qui sont des nerf pour diminuer les capacités d'autre des buff pour les up
_Mettre un bckgrd défilant de haut vers le bas (espace étoilé) avec des planètes, soleil etc s'affichant. Mais sans forcement apparaitre à l'intérieur du tunnel
_ varier les rayons du tunnel
_ mettre differente image du vaisseau sous les 9angles differents pour un effet pseudo 3D
_mettre des balles ?
*Joel* Le vaisseau semble être incliner qq soit la direction qu'il prend comme un avion de combat en qui effectue un decollage sur une piste

'''


#Paramètre spécifique

focale= 400 # à quelle vitesse, vitesse les objets devienne plus petits quand ils s'éloigne ou inversement

cible_x = LARGEUR // 2

cible_y = HAUTEUR // 2

compteur=50

cible_rayon= 250

nb_anneaux = 50

tunnel = []

profondeur= 100

for i in range( nb_anneaux):
    anneau= {

        "type": "anneau",

        "x" : LARGEUR//2,  #400

        "y" : HAUTEUR//2,  #300

        "z" : i*profondeur, # profondeur, distance entre l'anneau et moi. plus il est petit plus l'anneau est devant

        "r" : 250 # taille réelle de notre tunnel. 400 max, 100min
    }
    tunnel.append(anneau)



# affichage et tunnel, et obstacles
def afficher_monde(tun : list, obs : list, tir : list, bns : list, exp : list):
    # 1. LA FUSION : On additionne les 3 listes
    monde = tun + obs + tir + bns + exp

    # On crée une liste temporaire triée par profondeur (Z) décroissante (du plus loin au plus près)
    # La clé lambda obj: obj["z"] dit "trie en regardant la valeur de z"
    monde_trie = sorted(monde, key=lambda obj: obj["z"], reverse=True)

    # Variable en mémoire pour relier les anneaux entre eux
    precedent_anneau = None

    # On parcourt cette liste triée pout nos dessin
    for obj in monde_trie:

        # --- CALCULS ---
        # pour chaque objet 
        # on prends sa distance
        z = obj["z"]

        # Si un l'objet est derrière la caméra (z < 0), on ne l'affiche pas
        if z < 0: continue

        # on calcule  l'illusion, en gros plus l'obj est proche, mieux on le voit (grand), s'il est loin,
        # on le verra moins bien. ici si z=0 alors facteur = 100%, on voit bien l'obj et il a sont rayon exact.
        facteur = focale / (focale + z)
        cx = obj["x"]
        cy = obj["y"]


        # le rayon apparent (r_visuel) lui nous donne la taille du rayon en fonction du facteur. celui-ci dit :
        # si le facteur est à 50% alors on voit le cerlce avec 50% de son rayon initial (rayon de l'obj) pour
        # essayer de copier l'effet d'optique

        # --- CAS 1 : C'EST UN OBSTACLE ---
        if obj["type"] == "obstacle":
            # On calcule son rayon visuel
            r_visuel = int(obj["r"] * facteur)
            # On le dessine (Rond plein ROUGE)
            # pg.draw.circle(fenetre, ROUGE, (cx, cy), r_visuel)
            img=pg.transform.scale(obj["image"],(r_visuel+40,r_visuel+40))
            fenetre.blit(img, (cx - img.get_width()//2, cy - img.get_height()//2))


        # --- CAS 2 : C'EST UN BONNUS ---
        elif obj["type"] == "bonus":
            # On calcule son rayon visuel
            r_visuel = int(obj["r"] * facteur)
            # On le dessine (Rond plein VERT)
            # pg.draw.circle(fenetre, VERT_biz, (cx, cy), r_visuel)
            img = pg.transform.scale(obj["image"], (r_visuel*2, r_visuel*2))
            fenetre.blit(img, (cx - img.get_width()//2, cy - img.get_height()//2))
        

        # --- CAS 3 : C'EST UN TIR DU VAISSEAU ---
        elif obj["type"] == "tirs":
            if obj["actif"] == True :
                r_visuel = int(obj["r"] * facteur)

                # On le dessine (Rond plein ORANGE)
                pg.draw.circle(fenetre, ORANGE, (cx, cy+3), r_visuel)


        # --- CAS 4 : C'EST UNE EXPLOSION ---
        elif obj["type"] == "explosion":
            r_visuel = int(obj["r"] * facteur * 1.5) # Un peu plus gros que l'astéroïde
            img = pg.transform.scale(xploseImg, (r_visuel*2, r_visuel*2))
            fenetre.blit(img, (cx - img.get_width()//2, cy - img.get_height()//2))
            
            # On diminue le timer
            obj["timer"] -= 1


        # --- CAS 5 : C'EST UN ANNEAU DU TUNNEL ---
        elif obj["type"] == "anneau":
            # On calcule son rayon visuel
            r_visuel = int(obj["r"] * facteur)

            # A. LES LIGNES (Le maillage du tunnel)
            # On relie cet anneau UNIQUEMENT au précédent ANNEAU (on ignore les obstacles entre deux)
            if precedent_anneau is not None:
                px, py, pr = precedent_anneau

                # nombre de corde pour le maillage
                nb_lignes = 18
                for i in range(nb_lignes):
                    angle = (math.pi * 2 / nb_lignes) * i

                    # Point sur l'anneau ACTUEL
                    x1 = cx + r_visuel * math.cos(angle)
                    y1 = cy + r_visuel * math.sin(angle)

                    # Point sur l'anneau PRÉCÉDENT (plus loin)
                    x2 = px + pr * math.cos(angle)
                    y2 = py + pr * math.sin(angle)

                    pg.draw.line(fenetre, bleu_charette, (x1, y1), (x2, y2), 2)

            # B. LE CERCLE
            pg.draw.circle(fenetre, bleu_charette, (cx, cy), r_visuel, 2)

            # C. MISE EN MÉMOIRE
            # On ne met à jour 'precedent' QUE si c'est un anneau.
            # Comme ça, les lignes passent "à travers" les obstacles sans se casser.
            precedent_anneau = (cx, cy, r_visuel)





# défilement du tunnel logique
def tunnel_defil( an : dict):
    #Peut définir de
    # On doit dire à la fonction qu'on veut modifier les variables globales définies plus haut
    global cible_x, cible_y, compteur, cible_rayon, VITESSE_DEFILEMENT


    an["z"] -= VITESSE_DEFILEMENT

    #si l'anneau sort de notre champs de vision on le mets à la fin (profondeur)
    if an["z"] < 0 :
        an["z"] = nb_anneaux*profondeur
        compteur-=1

        # gestion de la largeur du tunnel chaque 50 anneaux
        if compteur <= 0:
            # On change la variable globale "cible_rayon"
            cible_rayon = random.choice([170, 200, 250])
            if VITESSE_DEFILEMENT > 60 :
                cible_rayon = random.choice([170, 200])

            # On relance le compteur ( pour une durée aléatoire ? )
            compteur = 50

        # IMPORTANT : L'anneau prend TOUJOURS la valeur de la zone actuelle
        # (Que le compteur soit à 0 ou pas, on applique la cible)
        an["r"] = cible_rayon


        ###-----Mobilité aleatoire du tunnel-----####

        # On déplace un petit peu l'anneau renvoyer à la fin de manière aléatoire
        cible_x += random.randint(-20, 20) # Décalage horizontal
        cible_y += random.randint(-20, 20) # Décalage vertical


        # On empêche le tunnel de sortir de l'écran
        # On garde une marge de 200 pixels sur les bords X et 150 sur
        # on peut soit le forcer à rester à 200 ou le jetter aleatoirement quelque part sur l'ecran (juste ajouter un random.randint(200,601)

        if cible_x < 200:
            cible_x = 200
        if cible_x > LARGEUR - 200:
            cible_x = LARGEUR - 200

        #pareille pour y  (random.randint(150,451)
        if cible_y < 150:
            cible_y = 150
        if cible_y > HAUTEUR - 150:
            cible_y = HAUTEUR - 150

        # 3. On applique cette nouvelle position à l'anneau recyclé
        an["x"] = cible_x
        an["y"] = cible_y



# Verification de la sortie du tunnel
def ver_sortie_tunnel(tun : list, vss : dict):

    #Centre vaisseau
    v_ctr_x = vss["vssX"] + vss["rl"]
    v_ctr_y = vss["vssY"] + vss["rh"]

    #Centre tunnel (on verifie toujours avec l'anneau le plus proche )
    ctr_tnl_x = tun[0]["x"]
    ctr_tnl_y = tun[0]["y"]


    #Distance du vaisseau par rapport au centre du tunnel
    dist_vss_tnl =  math.sqrt((v_ctr_x - ctr_tnl_x)**2 + (v_ctr_y - ctr_tnl_y)**2)

    #on prend le rayon de l'anneau le plus proche
    ray_tnl_act = tun[0]["r"]

    #Si la somme des rayons du vaisseau et de l'anneau est plus grande que la distance entre les deux centres, alors
    # le vaisseau n'est plus dans le tunnel
    if dist_vss_tnl >= (ray_tnl_act -(vss["rl"])+40):
        xplose_vaiss_sound.play()
        print("SORTIE DE TUNNEL ! PERDU !")
        return True

    return False


# Gestion du score
def show_score(x,y) :
    global score_value, high_score_value
    if score_value >= high_score_value :
        score = score_font.render('SCORE : '+ str(int(score_value)),True, Bleu_dragée)
    elif score_value < high_score_value :
        score = score_font.render('HIGH SCORE : '+ str(int(high_score_value-score_value)),True, Bleu_dragée)
    fenetre.blit(score,(x,y))

    # pour le nombre de vie 
    live = score_font.render(str(vaisseau["vie"])+" lives left",True,ROUGE)

    hei = live.get_height()
    fenetre.blit(score,(x,y))
    fenetre.blit(live,(x+20,y+hei))

    # pour la jauge du bouclier 
    pg.draw.rect(fenetre,(255,255,255),[x+30, y+hei+40, vaisseau["bouclier_max"], 20],2) #jauge vide 

    if vaisseau["bouclier_chg"] < 30 : 
        pg.draw.rect(fenetre,ROUGE,[x+30, y+hei+40, vaisseau["bouclier_chg"], 20]) #jauge rouge pas assez
    elif vaisseau["bouclier_chg"] >= 30 and vaisseau["bouclier_chg"] < 100: 
        pg.draw.rect(fenetre,Bleu_dragée,[x+30, y+hei+40, vaisseau["bouclier_chg"], 20]) # jauge bleu. on peut lancer
    else : 
        pg.draw.rect(fenetre,VERT_biz,[x+30, y+hei+40, vaisseau["bouclier_chg"], 20]) # jauge vert. charger totalement 
    



# chargement du meilleur score :
def charger_high_score():
    try:
        # "r" signifie "read" (lire)
        with open("high_score.txt", "r") as f:
            contenu = f.read()
            return int(contenu) # On convertit le texte en nombre entier
    except FileNotFoundError :
        # Si le fichier n'existe pas encore, le meilleur score est 0
        return 0


# sauvegarde du meilleur score
def sauvegarder_high_score(nouveau_score):
    with open("high_score.txt", "w") as f:
        f.write(str(int(nouveau_score)))


def show_game_over(x : bool) :
    global score_value, high_score_value

    if x :
        over_text = over_font.render("Sortie du TUNEL",True, VERT_biz)
    else :
        over_text = over_font.render("COLLISION",True, VERT_biz)

    # Interface
    # On assombrit un peu l'écran pour que le texte ressorte mieux 
    surf_noir = pg.Surface((LARGEUR,HAUTEUR))  # Crée une surface
    surf_noir.set_alpha(128)                # Transparence (0-255)
    surf_noir.fill((0,0,0))                 # Noir
    fenetre.blit(surf_noir, (0,0))          # On l'applique par dessus le jeu

    fenetre.blit(over_text,((LARGEUR // 2) - (over_text.get_width()//2),200))

    # Score
    if score_value < high_score_value :
        Hscore= score_font.render('HIGH SCORE : '+ str(int(high_score_value)),True, OR_met)
        score = score_font.render('SCORE : '+ str(int(score_value)),True, Bleu_dragée)

        # affichage
        fenetre.blit(Hscore,((LARGEUR // 2) - (Hscore.get_width()//2),HAUTEUR//2))
        fenetre.blit(score,((LARGEUR // 2) - (score.get_width()//2),(HAUTEUR//2)+60))

    else :
        congrats = congrat_font.render(" FELICITATION !! ", True, ORANGE)
        new_score = score_font.render(' NOUVEAU HIGH SCORE : '+ str(int(score_value)),True, OR_met)

        fenetre.blit(congrats,((LARGEUR // 2) - (congrats.get_width() // 2),HAUTEUR//2))
        fenetre.blit(new_score,((LARGEUR // 2) - (new_score.get_width() // 2),(HAUTEUR//2)+60))
    
    # Message pour quitter
    quit_txt = score_font.render("Appuyez sur une ENTRER pour quitter", True, (255, 255, 255))
    fenetre.blit(quit_txt, ((LARGEUR // 2) - (quit_txt.get_width() // 2), HAUTEUR - 100))
    
    pg.display.update()

    # 3. Boucle d'attente (Anti-Freeze)
    attente = True
    while attente:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # Si on appuie sur n'importe quelle touche, on sort de l'écran
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN : # touche entrer 
                    attente = False


def intro_sequence():
    intro = True
    # On place le logo très loin au début 
    logo_z = 3000

    # 0 = Approche, 1 = Pause, 2 = Sortie
    etat = 0
    temps_debut_pause = 0

    # On charge l'image originale pour éviter qu'elle soit floue en redimensionnant
    logo_orig = pg.image.load('image/AdAstraLog.png')

    while intro:
        # Permettre de quitter pendant l'intro si on veut
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # Affichage du fond
        fenetre.blit(background, (0,0))

        # Calcul de la taille (Effet Tunnel / Perspective)

        if focale + logo_z != 0: # Sécurité pour ne pas diviser par 0
            facteur = focale / (focale + logo_z)
        else:
            facteur = 1

        # Nouvelle taille apparente
        w = int(logo_orig.get_width() * facteur)
        h = int(logo_orig.get_height() * facteur)

        # Affichage du Logo Centré
        if w > 0 and h > 0:
            logo_scaled = pg.transform.scale(logo_orig, (w, h))
            # Calcul pour centrer parfaitement
            pos_x = (LARGEUR // 2) - (w // 2)
            pos_y = (HAUTEUR // 2) - (h // 2)
            fenetre.blit(logo_scaled, (pos_x, pos_y))


        # Logique de mouvement

        # ÉTAT 0 : LE LOGO ARRIVE
        if etat == 0:
            logo_z -= 20 # Vitesse d'approche
            # Quand il est assez proche (z=200), on passe en pause
            if logo_z <= 200:
                etat = 1
                temps_debut_pause = pg.time.get_ticks() # On note l'heure

        # ÉTAT 1 : LA PAUSE (3 SECONDES)
        elif etat == 1:
            maintenant = pg.time.get_ticks()
            # Si 3000ms (3s) sont passées
            if maintenant - temps_debut_pause > 3000:
                etat = 2

        # ÉTAT 2 : LA SORTIE (IL NOUS FONCE DESSUS)
        elif etat == 2:
            logo_z -= 30 # Il part plus vite
            # Si Z est négatif, il est derrière nous (ou "dans nos yeux")
            if logo_z < -100:
                intro = False # FIN DE L'INTRO

        pg.display.update()
        heure.tick(60)






# -------------------
# Programme principal
# -------------------

## Boucle principale



#Fenetre du jeu

fenetre = pg.display.set_mode((LARGEUR,HAUTEUR))

pg.display.set_caption("AD Astra")

pg.display.set_icon(Ad_Astra_logoI)

heure = pg.time.Clock()

score_value = 0
score_X, score_Y= 10, 10

high_score_value = charger_high_score()


#Initialisation

obstacles = []
tirs = []
bonus = []
explosion=[]
dernier_tir = 0
# boucle infinie pour faire tourner le jeu
intro_sequence()

mixer.music.play(-1)

en_cours = True

while en_cours:

   
     # sortir du jeu
    for event in pg.event.get():
        if event.type == pg.QUIT:
            en_cours=False
        # sauvegarde du high score le joueur veut quitter la partie
        #Bouclier
        if event.type == pg.KEYDOWN:

        #Active le bouclier
            if event.key == pg.K_x : 
                # Cas 1 : Le bouclier est déjà allumé -> On l'éteint
                if vaisseau["bouclier"] == True:
                    vaisseau["bouclier"] = False
                    print("Bouclier désactivé")
                
                # Cas 2 : Le bouclier est éteint -> On l'allume SI on a assez d'énergie
                else:
                    # On impose un seuil de 25% pour éviter le spam quand c'est vide
                    if vaisseau["bouclier_chg"] > 30:
                        vaisseau["bouclier"] = True
                        print("Bouclier activé")
                    else:
                        print("Pas assez d'énergie !")
            
        #Tirs
            if event.key == pg.K_w : 
                shot=pg.time.get_ticks()
                if shot - dernier_tir > 50: # 250ms entre chaque tir
                    tirs.append(creer_tirs(vaisseau))
                    shot_sound.play()
                    dernier_tir = shot

    ###--- BACKGROUND ---###

    # Défilement du bckground :
    for i in range(0,tiles+1) :
        fenetre.blit(background,(0,-i * bg_heigt + scroll)) #defilement verticale.
    # verifie si scroll est > la hauteur du bckgrnd alors on le remets à 0.
    scroll+=0.5
    if abs(scroll) >= bg_heigt :
        scroll=0

    # soleil et lune
    fenetre.blit(sun,(sun_X,sun_Y))
    fenetre.blit(moon,(moon_X,moon_Y))

    # Gestion du score
    show_score(score_Y,score_X)
    # if high_score_value > 0 :
    #     high_score_value -= VITESSE_DEFILEMENT
    score_value += VITESSE_DEFILEMENT # 1 / ( 1 * 60 ) # x / ( y * 60 ) => Augmente de x toute les y secondes

   # Réinitialisation du vaisseau de base
    vaisseau["image"]=vaisseau_img_C

    #trie pas profondeur du tunnel
    tunnel_trie=sorted(tunnel, key= lambda an : an["z"], reverse=False)

    # sommes-nous toujours dans le tunnel ?
    if ver_sortie_tunnel(tunnel_trie, vaisseau) :
        
        boom = pg.transform.scale(xploseImg, (200, 200))
        # On l'affiche sur le vaisseau
        fenetre.blit(boom, (vaisseau["vssX"], vaisseau["vssY"]))
        pg.display.update()

        xplose_vaiss_sound.play()  

        show_game_over(True)
    
        en_cours = False


    keys = pg.key.get_pressed()

    vx, vy = vaisseau["vssX"], vaisseau["vssY"]

    # Gestion des Déplacements

    #Horizontal
    if keys[pg.K_LEFT] and vx > 0 :
        vx -= vaisseau["vitesse"]
        vaisseau["image"]=vaisseau_img_G
    if keys[pg.K_RIGHT] and vx < LARGEUR - vaisseauL :
        vx += vaisseau["vitesse"]
        vaisseau["image"]=vaisseau_img_D

    #Vertical
    if keys[pg.K_UP] and vy > 0:
        vy -= vaisseau["vitesse"]
        vaisseau["image"]=vaisseau_img_H
    if keys[pg.K_DOWN] and vy < HAUTEUR - vaisseauH:
        vy += vaisseau["vitesse"]
        vaisseau["image"]=vaisseau_img_B

    # Gestion action
    #Acceleration et deceleration
    if keys[pg.K_RSHIFT] :
        VITESSE_DEFILEMENT += 0.5 #Acceleration
        #Limite
        if VITESSE_DEFILEMENT > 90 : VITESSE_DEFILEMENT = 90
    if keys[pg.K_LSHIFT]:
        VITESSE_DEFILEMENT -= 0.5
        if VITESSE_DEFILEMENT < 5 : VITESSE_DEFILEMENT = 5
    
    




    #Mise à jour des paramètres de positions
    vaisseau["vssX"] ,vaisseau["vssY"] = vx , vy

    #Mise à jour du rectangle de collision pour qu'il suive l'image
    # vaisseau["rect"].topleft = (vx,vy)



    # gestion de la vitesse
    #la vitesse augmente au fil du temps. on fixe une limite de 45,
    # et une diminution aléatoire de celle ci.
    #Copie de la vitesse inutile prendre plus les évènements spéciaux
    VITESSE_DEFILEMENT += 5 / (10 * 60)  # x / ( y * 60 ) => Augment la vitesse de x toute les y secondes




    # défilement du tunnel  et des obstacles
    for elt in tunnel:
        tunnel_defil(elt)

    if obstacles :
        for obs in obstacles:
            obstacle_defil(obs)

        # --Test collision obstacle
        if verif_collision_obs(vaisseau,obstacles):
            # print("Collision")
            # vaisseau["vie"] -= 1
            #Flash roupe
            fenetre.fill(ROUGE)
            pg.display.update()

            #Supprime les obstacles mutiples pour eviter de mourir 50 fois
            obstacles = [obs for obs in obstacles if obs["z"] > 200]
            if vaisseau["vie"] <= 0 :
                # print("COLLISION")
                boom = pg.transform.scale(xploseImg, (200, 200))
                # On l'affiche sur le vaisseau
                fenetre.blit(boom, (vaisseau["vssX"], vaisseau["vssY"]))
                pg.display.update()

                xplose_vaiss_sound.play()  

                show_game_over(False)

                en_cours = False

    # Gestion des bonus 
    if bonus :
        for bns in bonus:
            bonus_defil(bns)

        # --Test collision bonus
        if verif_collision_bonus(vaisseau, bonus):
            print("contact")
            vaisseau["vie"] += 1

            # Flash Vert
            fenetre.fill(VERT_biz)
            pg.display.update()  

            # Supprime les multiples bonus pour éviter d'avoir trop de bonus
            bonus = [bns for bns in bonus if bns["z"] > 200]
            if vaisseau["vie"] >= 9:
                vaisseau["vie"] = 9
                print("Vie Pleine")


                pg.display.update()


    tirs_defil_gest(tirs, obstacles,explosion)
    gest_bouclier(vaisseau,VITESSE_DEFILEMENT)

    # Nettoyage des liste
    obstacles = [obs for obs in obstacles if obs["actif"]]
    bonus = [bns for bns in bonus if bns["actif"]]
    tirs = [t for t in tirs if t["actif"]]
    explosion = [exp for exp in explosion if exp["timer"] > 0]

    #Obstacles (génération aléatoire)
    if random.random() < 0.02:
        nouvel_obs = creer_obstacle(cible_x,cible_y)#Utilisation des variables globales
        obstacles.append(nouvel_obs)
    #Bonus (génération aléatoire)
    if random.random() < 0.001:
        new_bns = creer_bonus(cible_x,cible_y)#Utilisation des variables globales
        bonus.append(new_bns)


    #Affichage du tunnel et obs
    afficher_monde(tunnel, obstacles,tirs, bonus, explosion)

    


    # affichage du vaisseau
    vaisseau_aff(vaisseau["vssX"], vaisseau["vssY"])





    pg.display.update()

    heure.tick(FPS)

if score_value > high_score_value:
    new_high_score_value = score_value # Mise à jour 
    sauvegarder_high_score(new_high_score_value) # Écriture dans le fichier txt
    print("Nouveau record sauvegardé !")




# Fonctions mathématiques ou aides
# Le point d'entrée qui lance la boucle de jeu
# Fin

pg.quit()

sys.exit()