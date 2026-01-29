select f.nomFiliere, s1.nomSpecialite as spe1 , s2.nomSpecialite as spe2, ad.txReussite
from filieres f join adapter ad on f.codFiliere=ad.codFiliere 
join specialites s1 on ad.codSpe1=s1.codSpecialite 
join specialites s2 on ad.codSpe2=s2.codSpecialite
where f.modalitesRecrutement='Dossier'  