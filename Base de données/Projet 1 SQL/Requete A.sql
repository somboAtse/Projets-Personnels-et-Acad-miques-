select m.*
from metiers as m join approprier as ap on ap.codMetier=m.codMetier
join filieres as f on ap.codFiliere=f.codFiliere
inner join adapter as ad on ad.codFiliere=f.codFiliere
join specialites as sp1 on sp1.codSpecialite=ad.codSpe1 
join specialites as sp2 on sp2.codSpecialite=ad.codSpe2
where ad.txReussite>50 
and sp1.nomSpecialite='Mathématiques' and sp2.nomSpecialite='SES' 