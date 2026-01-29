--QUESTION A/  
UPDATE Promotions 
SET qteStock=0
WHERE idProd=(SELECT idProd FROM Produits WHERE nomProd='Sandales Girafon') 
AND idTaille=(SELECT idTaille FROM Tailles WHERE nomTaille='41')
AND idCouleur=(SELECT idCouleur FROM Couleurs WHERE nomCouleur='Rouge'); 
GO 


--QUESTION B 
DELETE FROM Clients WHERE prenomCli='Alice'; 
GO

--QUESTION C 
CREATE VIEW ProdDispo(nomProduit,quantDispo,taille,couleur) As
	SELECT Prod.nomProd, Prom.qteStock, T.nomTaille, C.nomCouleur
	FROM Produits Prod join Promotions Prom on Prod.idProd=Prom.idProd
		 join Tailles T on Prom.idTaille=T.idTaille 
		 join Couleurs C on Prom.idCouleur=C.idCouleur
	WHERE Prod.idProd in ( Select idProd from Produits P join Categories C on P.idCat=C.idCat WHERE C.nomCat!='Sacs')
	--comme nous n'avons pas explicitement 'chaussure' dans notres base, mais seulement 'sacs' qui n'est pas une chaussure par rapport aux autre catégorie. 
	-- on aurait pu mettre 'sneakers' ou autre aussi 
	AND Prom.idOp in (SELECT idOp FROM Operations WHERE dateDebutOp>='2026-01-01' AND dateFinOP<='2026-01-31')
	AND Prom.qteStock>0; 
GO 
	
/*
--VERSION OPTIMISER 
CREATE VIEW ProdDispo AS
	SELECT 
        Prod.nomProd AS Nom, 
        Prom.qteStock AS Quantite, 
        T.nomTaille AS Taille, 
        C.nomCouleur AS Couleur
	FROM Produits Prod 
    JOIN Categories Cat ON Prod.idCat = Cat.idCat
    JOIN Promotions Prom ON Prod.idProd = Prom.idProd
    JOIN Operations Ope ON Prom.idOp = Ope.idOp
    JOIN Tailles T ON Prom.idTaille = T.idTaille 
    JOIN Couleurs C ON Prom.idCouleur = C.idCouleur
	WHERE Cat.nomCat!='Sacs'
	AND Ope.dateDebutOp >= '2026-01-01' 
    AND Ope.dateFinOp <= '2026-01-31'
	AND Prom.qteStock > 0 ; 
*/