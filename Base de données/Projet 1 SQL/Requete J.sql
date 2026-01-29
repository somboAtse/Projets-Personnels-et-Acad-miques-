select nomM
from (select m.nomMetier as nomM, COUNT(f.codFiliere) as totFiliere
	from filieres f join approprier ap on ap.codFiliere=f.codFiliere
	join metiers m on ap.codMetier=m.codMetier 
	group by m.nomMetier) as nbdeFiliere
where totFiliere IN (select max(totFiliere) from (select m.nomMetier, COUNT(f.codFiliere) as totFiliere
													from filieres f join approprier ap on ap.codFiliere=f.codFiliere
													join metiers m on ap.codMetier=m.codMetier 
													group by m.nomMetier)as maxF);



/*
select m.nomMetier, COUNT(f.codFiliere) as nbdeFiliere
from filieres f join approprier ap on ap.codFiliere=f.codFiliere
join metiers m on ap.codMetier=m.codMetier 
group by m.nomMetier 
*/



/* code Mamadou 
1e version 
SELECT TOP 1  M.nomMetier
FROM metiers AS M
INNER JOIN approprier AS A ON M.codMetier = A.codMetier
GROUP BY M.codMetier, M.nomMetier
ORDER BY  COUNT(A.codFiliere) DESC;

--2e version
SELECT   M.nomMetier
FROM metiers AS M
INNER JOIN approprier AS A ON M.codMetier = A.codMetier
INNER JOIN filieres AS F ON F.codFiliere=A.codFiliere
group by M.codMetier, M.nomMetier, F.codFiliere
having F.codFiliere = (Select max(codFiliere)
from filieres);*/