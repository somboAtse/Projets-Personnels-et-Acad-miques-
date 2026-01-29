select e.codEtab, e.nomEtab, e.dptEtab
from filieres f join offrir on f.codFiliere=offrir.codFiliere 
join etablissements e on offrir.codEtab=e.codEtab 
where e.codEtab not in ( select organisation.codEtab from organisation) -- ou un f.modalitesRecrutement!='concours'
group by e.codEtab, e.nomEtab, e.dptEtab; --faire attention au group by 

--on aurai pu faire un except 

/*Except 
select e.codEtab, e.nomEtab, e.dptEtab
from filieres f join offrir on f.codFiliere=offrir.codFiliere 
join etablissements e on offrir.codEtab=e.codEtab 
where f.modalitesRecrutement='concours'*/