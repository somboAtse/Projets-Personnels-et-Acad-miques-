select f2.nomFiliere, f2.dureeEtudes
from filieres f1 join reorienter r on f1.codFiliere=r.codFiliereActuelle
join filieres f2 on r.codFiliereNouvelle=f2.codFiliere
join domaines d on f2.codDomaine=d.codDomaine 
where f1.nomFiliere='Licence Economie et gestion' 
and f2.modalitesRecrutement!='concours'
and d.nomDomaine='Médical/Para-Médical' 