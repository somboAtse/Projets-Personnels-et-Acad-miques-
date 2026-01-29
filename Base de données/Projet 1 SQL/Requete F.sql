SELECT e.nomEtab, e.adrEtab, COUNT(DISTINCT d.codDomaine) AS nbDomaineDiff
FROM etablissements e
JOIN offrir o ON e.codEtab = o.codEtab
JOIN filieres f ON o.codFiliere = f.codFiliere
JOIN domaines d ON d.codDomaine = f.codDomaine
GROUP BY e.nomEtab, e.adrEtab
HAVING COUNT(DISTINCT d.codDomaine) >= 2;



/* 
Ou alors en usant de sous sous requete (je n'arrive toujours pas à comprendre la logique de celle ci : 

SELECT e.nomEtab, e.adrEtab 
FROM etablissements e 
WHERE (
    SELECT COUNT(*) 
    FROM (
        SELECT d.codDomaine 
        FROM offrir o 
        JOIN filieres f ON o.codFiliere = f.codFiliere 
        JOIN domaines d ON f.codDomaine = d.codDomaine 
        WHERE o.codEtab = e.codEtab 
        GROUP BY d.codDomaine
    ) AS domaines_uniques
) >= 2;$
*/