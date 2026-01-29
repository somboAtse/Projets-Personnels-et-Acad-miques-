select e.nomEtab, e.dptEtab
from etablissements e join offrir o on e.codEtab=o.codEtab
join filieres f on o.codFiliere=f.codFiliere
join domaines d on d.codDomaine=f.codDomaine
where d.nomDomaine='Médical/Para-Médical' 
intersect 
select e.nomEtab, e.dptEtab
from etablissements e join offrir o on e.codEtab=o.codEtab
join filieres f on o.codFiliere=f.codFiliere
join domaines d on d.codDomaine=f.codDomaine
where d.nomDomaine='Biologie'  