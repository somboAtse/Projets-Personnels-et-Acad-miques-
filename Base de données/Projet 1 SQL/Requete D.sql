--premier partie 
select nomMetier, resumeMetier 
from metiers
where salaireDebutantMetier=(select max(salaireDebutantMetier) from metiers);


--deuxieme partie 
select f.nomFiliere
from filieres f join approprier ap on f.codFiliere=ap.codFiliere
join metiers m  on ap.codMetier=m.codMetier
where m.salaireDebutantMetier = (select max(salaireDebutantMetier) as salaire_maximum from metiers);

