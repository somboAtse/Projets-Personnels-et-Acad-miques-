select f.nomFiliere, count(e.codEtab) as nbEtablissement
from etablissements e join offrir o on e.codEtab=o.codEtab 
join filieres f on f.codFiliere=o.codFiliere
group by f.codFiliere, f.nomFiliere;