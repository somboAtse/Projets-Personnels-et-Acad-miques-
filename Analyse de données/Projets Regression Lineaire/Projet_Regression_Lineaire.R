#### Partie 1 Analyse univarié et test statistiques ##### 
attach(medecins)
#1 
summary(medecins)
medecins$genre=as.factor(medecins$genre)
medecins$spec=as.factor(medecins$spec)
medecins$secteur=as.factor(medecins$secteur)


#Pour les variables qualitatives : 
table(genre)
round(prop.table(table(genre)),digits=3)
barplot(prop.table(table(genre)),
        main="Répartition des des professionnel de santé \n par leurs genre",
        ylab="Fréquence relative", xlab="genre")

table(spec)
round(prop.table(table(spec)),digits=3)
barplot(prop.table(table(spec)),
        main="Répartition des des professionnel de santé \n par leurs spécialité",
        ylab="Fréquence relative", xlab="spécialité")

table(secteur)
round(prop.table(table(secteur)),digits=3)
barplot(prop.table(table(secteur)),
        main="Répartition des des professionnel de santé \n selon leur secteur",
        ylab="Fréquence relative", xlab="secteur")

#Pour les variables quantitative :

summary(nbpatients)
cv_nbpat= sd(nbpatients)/mean(nbpatients)
hist(nbpatients,freq=FALSE,xlab="nombre de patient annuel",
     ylab="Densité de fréquence",main="Histogramme du nombre de patient")

summary(moins16)
cv_moins16= sd(moins16)/mean(moins16)
hist(moins16,freq=FALSE,xlab="nombre de patient de -16 annuel",
     ylab="Densité de fréquence",main="Histogramme du nombre de patient de -16")

summary(X60a69)
cv_x60= sd(moins16)/mean(moins16)
hist(X60a69,freq=FALSE,xlab="nombre de patient de 60 a 69 annuel",
     ylab="Densité de fréquence",main="Histogramme du nombre de patient de -16")

summary(plus70)
cv_plus70= sd(plus70)/mean(plus70)
hist(plus70,freq=FALSE,xlab="nombre de patient de +70 annuel",
     ylab="Densité de fréquence",main="Histogramme du nombre de patient de +70")


summary(honor)
cv_honor= sd(honor)/mean(honor)
hist(honor,freq=FALSE,xlab="montant des honoraire annuel",
     ylab="Densité de fréquence",main="Histogramme du montant des honoraire annuelel")





#2 analyse bivarié  selon le genre  
# a) 
tableauGS = table(spec, genre)
tableauGS
addmargins(tableauGS)
barplot(t(prop.table(tableauGS,1)),beside=TRUE,col=c("blue","green"),
        main="Distributions conditionnelles du genre   \n  sachant la spécialité",
        xlab= "specialité",ylab="Fréquence relative",legend.text=TRUE)
# Test du Khi-deux d'indépendance
#H0:indépendance du genre et du statut professionnel
#H1:pas d'indépendance (=les variables sont liées)
# conditions de validité
round(chisq.test(tableauGS)$expected,digits=2)
khi2GS=chisq.test(tableauGS)
khi2GS
round(khi2GS$residuals^2,digits=2)

## on remarque ici que la pvalue est inérieu au seuil de 5% ce qui signifie que l'on rejette Ho 
## le choix de la spécialité n'est pas vraiment lié au genre selon le graphique en remarque juste que les hommes 
## sont toujours les plus présent quelque soit la spécialité 
## là où le choix est fonction du genre selon notre test c'est que les femme se veront plus partir 
## dans le dom mixte, quand les hommes eux iront dans le domane chirurgicale


# b) 
boxplot(honor~genre,
        main="Boîtes à moustaches juxtaposées \n du salaire en fonction du genre")
tapply(honor,genre,summary)
moycond=tapply(honor,genre,mean)
tapply(honor,genre,var)
points(moycond,col="red",pch=5,cex=1)
#on veut tester H_0 : la moyenne des salaires des femmes est
# égale à la moyenne des salaires des hommes
# contre H1 : ces salaires moyens sont différents
t.test(honor~genre,var.equal=FALSE)

## on remarque ici que la pvalue est inérieu au seuil de 5% ce qui signifie que l'on rejette Ho 
## et donc que les hommes gagne en générale plus que les femme sur une année
## cela se remarque aussi sur la boite à moustache où le 3e quantile du salaire des femme depasse de peu le 1e de celui des hommes. 



#3 analyse bivarié  selon le secteur tarifaire :
# a) 
tableauGS = table(secteur, spec)
tableauGS
addmargins(tableauGS)
barplot(t(prop.table(tableauGS,1)),beside=TRUE,col=c("blue","green","red"),
        main="Distributions conditionnelles de la specialité   \n  selon le secteur ",
        xlab= "secteur",ylab="Fréquence relative",legend.text=TRUE)

## on voit déjà à l'aide du grapphe, que les specialité sont plutot dspersé dans le sec 1 
## que dans le sec 2. une forte proportion de médicale au sec1 quans ce sera mixte au sec2. 

# b) 
boxplot(honor~secteur,
        main="Boîtes à moustaches juxtaposées \n du salaire en fonction du secteur")
tapply(honor,secteur,summary)
moycond=tapply(honor,secteur,mean)
tapply(honor,secteur,var)
points(moycond,col="red",pch=5,cex=1)
#on veut tester H_0 : la moyenne des salaires du secteur 1 est
# égale à la moyenne des salaires du secteur 2 
# contre H1 : ces salaires moyens sont différents
t.test(honor~secteur,var.equal=FALSE)


## alors oui, ces salaire moyens sont différent, le salaire sera plus élévée sur une année pour
## les medecins du secteur 2, sauf quelque medecins atypique du secteur 1 qu'on pourrait expliquer par 
## grand nombre de patient car oui les patient auront plus tendance à partir vers les medecins du secteur 1. 




#4 analyse bivariée  des variable sur les honoraire :
# a) 
plot(X60a69,honor,main="Nuage de points",xlab="nombre de patient entre 60 et 69",
     ylab="Salaireactuel(endollars)")
round(cor(X60a69,honor),digits=2)
cor.test(X60a69,honor)

plot(plus70,honor,main="Nuage de points",xlab="nombre de patient de plus de 70 ans",
     ylab="Salaireactuel(endollars)")
round(cor(plus70,honor),digits=2)
cor.test(plus70,honor)

## on pourrait dire oui, l les honoraire depende légèrement de sa patientele en personne agé avec des coef de correl <=31%, c'est quand même assez slight
## avec des pvalue tout deux inférieur à 5% 

#b) 
boxplot(honor~spec,xlab="spécialité",
        main="Boîtes à moustaches juxtaposées des honoraires \n en fonction de la spécalité ")
tapply(honor,spec,summary)
moycond2=tapply(honor,spec,mean)
moycond2
points(moycond2,col="red",pch="*",cex=2)
tapply(honor,spec,var)

## les vaiance et les moyennes sont très differentes. 
## Ici on veut saovir si la spéc a une influence sur les honoraire d'un medecins : 
# H0 : toute les moyenne des salaire sont les memes ( auccune influence donc. )
# H1 : elles sont differentes (les moyennes)

## mais on ne sait pas si les variance sont egales, et on va faire un test pour savoir c'est le levenet test
## H0: les var sont egales; H1: elles ne le sont pas. 

leveneTest(honor,spec)

## pvalue < 5% alors les variances sont differentes donc  :

oneway.test(honor~spec,var.equal=FALSE)

## same la pvalues n'est pas suffisante, on rejette donc H0, les moyennes sont differente.
## mais lesquelles diffferent  ? 
pairwise.t.test(honor,spec,p.adjust.method="none",pool.sd=FALSE)

##icic toutes les moyennes sont differentes deux à deux alors oui le type de spécialité a une influence sur 
## les honoraire du medecins. 




#### Partie 2 regression linéaire simple ####
## 1) 
plot(nbpatients,honor,main="Liaison entre les honoraire et le nombre de patient",
     xlab="nombre de patient",ylab="honoraire")
#text(nbpatients,honor,1:500)
#coefficient de corrélation linéaire et test associé : 
cor(nbpatients,honor)
# ces deux variable sont donc assez fortement liée avec r=61%
cor.test(nbpatients,honor)
# pvalue<5% alors oui c'est sure que les honoraire d'un medecins est lié à son nombre de patient. 

## 2) le modèe de regresssion linéairesimple théorque est : 
# honoraire= B_0 + B_1.nbpatiens + e_i 

## 3) 
regression=lm(honor~nbpatients)
regression
summary(regression)
# R^2= 37%  alors 37% de la variation des honoraire est du au nb de patients. 
# pvalue < 5% nous dis que tout parametre ne sont pas nulle, qu'il y en a au moins un de viable
# alors on rejette H0 et le modèle est globalement valide
#l'équation de la droite de regression est donc : honoraire= 47.42 + 0.06.nbpatients
## on passe au test de significativité du modèle : H_0: la var est significative, H_1 :elle ne l'est pas
## dans notre test pvalues<5% alors on rejette H_0 et oui la variable est donc signifative.

### en finale si le nb de patients augmente d'une unité : les honoraire des medecins augmentent d'envion 
## 0.06milliers d'euro (60euro)

abline(regression,col="red")
points(mean(nbpatients),mean(honor),pch="+",col="blue",cex=1.5)



## 4)
#sert à vérifier la normalité des erreurs et à repérer d'éventuels points aberrants
par(mfrow=c(1,2))
qqnorm(regression$residuals)
qqline(regression$residuals)
hist(regression$residuals,freq=FALSE)
par(mfrow=c(1,1))
# on voit sur le qqplot que les points ne sont pas vraiment alignés ce qui 
# remet en cause l'hypothèse de normalité des erreurs
# l'histogramme des résidus est très asymètrique avec un étalement à droite
# ce qui confirme que l'hypothèse de normalité des erreurs n'est pas parfaitement 
# vérifiée sur ces données

res_std=regression$residuals/118.1
#calcul des résidus standardisés

#Représentation graphique des résidus standardisés
plot(res_std,ylim=c(-5.5,5.5))
abline(h=-2,col="red")
abline(h=2,col="red")

# lesquels sont aberrant ? 
which(abs(res_std)>2)
length(which(abs(res_std)>2))

# 12 individus abbérant ! : 3  20  57 135 235 294 320 447 459 488

 

#### Partie 3  regression linéaire multiple ########

### 1) 
spec_Med=ifelse(spec=="Médicale",1,0)
spec_Chir=ifelse(spec=="Chirurgicale",1,0)
reg2=lm(honor~genre+spec_Chir+spec_Med+secteur+nbpatients+moins16+X60a69+plus70)
summary(reg2)

##le modèle théorique ici est : 
# honoraire_i = B_0 + B_1.genre_i + B_2.spec_Med_i + B_3.spec_Chir_i + B_4.secteur_i
# + B_5.nbpatients_i + B_6.moins16_i + B_7.X60a69_i + B_8.plus70_i + e_i avec i dans [0,500].
# il y a k=9 paramètre dans notre modèle 

## R^2= 52% alors  52%  du loyer est expliquer par les variables que nous avons choisies. 
## pvalues aussi <5% alors oui les parametre ne sont pas nuls et donc le modèle est globalement valide. 

## selon le test de signiicativité, seul les variable : genreHomme,spec_Chir,spec_Med,
## nbpatients, moins16, X60a69 sont significativent. 
## ET les variables NS sont : secteur et plus70 


### 2) 
## on retire d'abord la variable plus70 car elle a la plus grande pvalue>5%

spec_Med=ifelse(spec=="Médicale",1,0)
spec_Chir=ifelse(spec=="Chirurgicale",1,0)
reg3=lm(honor~genre+spec_Chir+spec_Med+secteur+nbpatients+moins16+X60a69)
summary(reg3)

## le R globale reste pratiquement le même (baisse très légère) et  le R2 ajusté augmente très légèrement. 
## le modèle reste tout de meme valide, mais la variable secteur reste toujours NS, étant la
## seule, on la retire. 

spec_Med=ifelse(spec=="Médicale",1,0)
spec_Chir=ifelse(spec=="Chirurgicale",1,0)
reg4=lm(honor~genre+spec_Chir+spec_Med+nbpatients+moins16+X60a69)
summary(reg4)

## le R globale baisse très légèrement et  le R2 ajusté baisse très légèrement. 
## le modèle reste tout de meme valide sans aucune variable non signidicative. 

# R2=51% 
# pvalue<5% 

##le modèle theorique ici est donc : 
# honoraire_i = B_0 + B_1.genre_i + B_2.spec_Med_i + B_3.spec_Chir_i + B_4.nbpatients_i
# + B_5.moins16_i + B_6.X60a69_i + e_i avec i dans [0,500].
# il y a k=7 paramètre dans notre modèle. 

##la droite de regression linéaire est donc ici : 
# honoraire= -72.86 + 53.21.genre_i + 75.82.spec_Med_i + 94.74.spec_Chir_i + 0.06.nbpatients_i
# - 0.6.moins16_i + 2.45.X60a69_i.

## toute choses egale par ailleurs, : 
#un médecin homme perçoit en moyenne 53210 euros de plus qu'un médecin femme
# un medecin de spec medicale perçoit en moyenne 75820euros  de plus qu'un medecins mixte
# un medecin de spec chirurgicale perçoit en moyenne 94740euros  de plus qu'un medecins mixte
# un patient supllementaire rapporte 60euros supplementaire
# un patient supplémentaire de moins de 16ans fait perdre 600euros supplementaire ( nous donne une perte nette de 
# 600-60= 540euro car c'est un patient en plus )
# un patient supplémentaire agée de 60 à 69ans rapporte 2450euros supplementaire 


### 3) 

qqnorm(reg4$residuals)
qqline(reg4$residuals) #pas aligné du tout 
hist(reg4$residuals,freq=FALSE) # histograme asymétrique et très etaler sur la droite. 
res_std4=reg4$residuals/104.1 #résidus standardisés
plot(res_std4,ylim=c(-5.5,5.5),main="Graphique des \nrésidus standardisés")
abline(h=-2,col="red")
abline(h=2,col="red")
which(abs(res_std4)> 2)
length(which(abs(res_std4)>2))


## les aberrant sont au nombre de 11 et ce sont : 3  20  57 135 235 294 320 417 447 459 488






