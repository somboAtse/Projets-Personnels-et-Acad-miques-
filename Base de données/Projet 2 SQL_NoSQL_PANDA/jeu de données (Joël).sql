/* Partie de Jeu de données SQL */

Insert into Categories (nomCat)
Values	('Sneakers'), 
		('Bottines et bottes'), 
		('Sandales et Talons'),
		('Sacs');

Insert into Marques (nomMarque,descMarque)
Values	('Mellow Yellow','Chaussures tendance et colorées'),
		('Panafrica','Baskets éthiques et éco-responsables'),
		('Girafon Bleu','Articles de lifestyle'),
		('Minelli','Articles de luxe et haute couture')

Insert into Operations(nomOp,dateDebutOp,dateFinOp)
Values	('Bonne année 2026','2026-01-01','2026-01-31'),
		('Vente Flash Printemps','2026-03-01','2026-03-05'),
		('Soldes d été','2026-06-20','2026-07-31'),
		('Black Friday','2025-11-28','2025-11-30'),
		('Magie de Noël','2025-12-01','2025-12-25')

Insert into Produits(nomProd,descProd,idCat,idMarque)
Values	('Sandales Girafon','Sandales à talon 8 cm, style élégant',3,3),
		('Baskets Wax','Baskets en tissu coloré',1,2),
		('Bottines Cuir','Bottines élégantes pour l hiver',2,1),
		('B&B','Grand sac en cuir véritable',4,4),
		('Vega','Chaussures de running iconiques',1,1)

Insert into Tailles(nomTaille)
Values ('41'),('38'),('37'),('40'),('Taille Unique')

Insert into Couleurs(nomCouleur)
Values ('Rouge'),('Multicolore'),('Marron'),('Bleu'),('Noir')

Insert into Promotions(qteStock,pxPromo,idProd,idTaille,idOp,idCouleur)
Values	(6,45.99,1,1,1,1),
		(12,55.00,2,2,3,2),
		(5,89.00,3,3,2,3),
		(8,60.00,4,4,4,4),
		(20,25.00,5,5,5,5)

Insert into TarifsPublics(pxInit,idProd,idTaille,idCouleur)
Values	(139.00,1,1,1),
		(110.00,2,2,2),
		(180.00,3,3,3),
		(120.00,4,4,4),
		(50.00,5,5,5)

Insert into Clients(nomCli,prenomCli,emailCli)
Values	('Kent','Alice','alice@email.fr'),
		('Martin','Jean','jean.martin@email.fr'),
		('Dupont','Marie','m.dupont@email.fr'),
		('Durant','Paul','p.durand@email.fr'),
		('Lefebvre','Lucie','l.lefebvre@email.fr')

Insert into Commentaires(texte,note,idProd,idCli)
Values	('Très jolies mais trop hautes pour moi.',3,1,1),
		('Superbe qualité et engagement éthique au top.',5,2,3),
		('Un peu serrées au niveau de la cheville.',2.5,3,2),
		('Très satisfait de mon achat.',4,4,5),
		('Parfait pour accompagner ma robe.',4.5,5,4)