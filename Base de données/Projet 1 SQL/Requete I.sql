select et.nomEtape, organisation.dtDebutEtape, organisation.dtFinEtape 
from etapes et join organisation on organisation.codEtape=et.codEtape 
join etablissements e on organisation.codEtab=e.codEtab 
join offrir o on o.codEtab=e.codEtab 
join filieres f on o.codFiliere=f.codFiliere 
join approprier ap on ap.codFiliere= f.codFiliere 
join metiers m on m.codMetier=ap.codMetier 
join filieres_concours fc on organisation.codFiliereConcours=fc.codFiliereConcours 
where ---fc.codFiliere=f.codFiliere and
m.nomMetier='Assistant vétérinaire' 
and e.nomEtab='Ecole vétérinaire de Haute-Garonne' 