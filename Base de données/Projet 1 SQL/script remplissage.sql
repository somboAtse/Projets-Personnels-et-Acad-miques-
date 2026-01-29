-- 1. Remplissage des 'domaines' [cite: 11, 69]
INSERT INTO [dbo].[domaines] (codDomaine, nomDomaine) VALUES
(1, 'Médical/Para-Médical'),
(2, 'Biologie'),
(3, 'Gestion'),
(4, 'Informatique'),
(5, 'Droit');
GO

-- 2. Remplissage des 'specialites' [cite: 9, 70]
INSERT INTO [dbo].[specialites] (codSpecialite, nomSpecialite) VALUES
(10, 'Mathématiques'),
(20, 'SES'),
(30, 'Littérature'),
(40, 'SVT');
GO

-- 3. Remplissage des 'filieres' [cite: 10, 71]
INSERT INTO [dbo].[filieres] (codFiliere, nomFiliere, dureeEtudes, resumeFiliere, modalitesRecrutement, codDomaine) VALUES
(100, 'Licence Economie et Gestion', 3, 'Formation en économie et gestion des entreprises.', 'dossier', 3),
(101, 'Manipulateur Radio', 3, 'Formation aux techniques d''imagerie médicale.', 'dossier', 1),
(102, 'Médecine (PACES/PASS)', 6, 'Première année des études de santé.', 'concours', 1),
(103, 'Licence SVT', 3, 'Sciences de la Vie et de la Terre.', 'dossier', 2),
(104, 'Ecole Vétérinaire', 5, 'Formation au métier de vétérinaire.', 'concours', 2),
(105, 'Licence Informatique', 3, 'Bases de la programmation et des systèmes.', 'dossier', 4),
(106, 'Licence de Droit', 3, 'Formation juridique générale.', 'dossier', 5);
GO

-- 4. Remplissage des 'metiers' [cite: 23, 73]
INSERT INTO [dbo].[metiers] (codMetier, nomMetier, resumeMetier, salaireDebutantMetier) VALUES
(1, 'Assistant Vétérinaire', 'Assiste le vétérinaire dans les soins aux animaux.', 24000),
(2, 'Data Scientist', 'Analyse les données pour en tirer des informations stratégiques.', 45000),
(3, 'Comptable', 'Tient les comptes de l''entreprise.', 30000),
(4, 'Manager de Projet', 'Supervise les équipes et la réalisation des projets.', 40000),
(5, 'Médecin Généraliste', 'Soigne les patients et assure le suivi médical.', 55000),
(6, 'Analyste Financier', 'Évalue la santé financière des entreprises.', 42000),
(7, 'Radiologue', 'Spécialiste en imagerie médicale.', 52000);
GO

-- 5. Remplissage des 'etablissements' [cite: 18, 75]
INSERT INTO [dbo].[etablissements] (codEtab, nomEtab, adrEtab, dptEtab) VALUES
(10, 'Ecole vétérinaire de Haute-Garonne', '23 Chemin des Capelles, 31300 Toulouse', 31),
(20, 'Université Toulouse Capitole', '2 Rue du Doyen-Gabriel-Marty, 31000 Toulouse', 31),
(30, 'Université Paul Sabatier', '118 Route de Narbonne, 31400 Toulouse', 31),
(40, 'Lycée Pierre-de-Fermat', '1 Parvis des Jacobins, 31000 Toulouse', 31),
(50, 'CHU de Montpellier', '191 Av. du Doyen Gaston Giraud, 34000 Montpellier', 34);
GO

-- 6. Remplissage des 'etapes' (pour les concours) [cite: 20, 76]
INSERT INTO [dbo].[etapes] (codEtape, nomEtape) VALUES
(1, 'Dépôt des dossiers'),
(2, 'Examen des candidatures'),
(3, 'Épreuves écrites'),
(4, 'Épreuves orales');
GO

-- 7. Remplissage des 'filieres_concours' [cite: 66, 77]
INSERT INTO [dbo].[filieres_concours] (codFiliereConcours, codFiliere) VALUES
(1, 102), -- Médecine
(2, 104); -- Ecole Vétérinaire
GO

-- 8. Remplissage 'adapter' (Lien Spécialités <-> Filières) [cite: 15, 78]
-- Note: Le couple (spe1, spe2) est géré (ex: 10, 20 et 20, 10 sont identiques). 
-- On stocke en ordre (min, max) pour éviter les doublons.
INSERT INTO [dbo].[adapter] (codSpe1, codSpe2, codFiliere, txReussite) VALUES
(10, 20, 100, 60), -- (Maths, SES) -> Eco Gestion, txReussite > 50% [pour Q.a]
(30, 20, 100, 55), -- (Littérature, SES) -> Eco Gestion [pour Q.g]
(10, 40, 103, 70), -- (Maths, SVT) -> Licence SVT
(10, 40, 102, 30), -- (Maths, SVT) -> Médecine
(10, 20, 105, 45), -- (Maths, SES) -> Licence Info, txReussite < 50%
(10, 40, 104, 25), -- (Maths, SVT) -> Ecole Vétérinaire
(30, 20, 106, 65); -- (Littérature, SES) -> Licence de Droit [pour Q.g]
GO

-- Vider la table adapter au cas où (même si elle est déjà vide)
DELETE FROM [dbo].[adapter];
GO

-- Remplissage 'adapter' (Lien Spécialités <-> Filières)
-- (Maintenant que la Clé Primaire est corrigée, cette insertion fonctionnera)
INSERT INTO [dbo].[adapter] (codSpe1, codSpe2, codFiliere, txReussite) VALUES
(10, 20, 100, 60), -- (Maths, SES) -> Eco Gestion, txReussite > 50%
(30, 20, 100, 55), -- (Littérature, SES) -> Eco Gestion
(10, 40, 103, 70), -- (Maths, SVT) -> Licence SVT
(10, 40, 102, 30), -- (Maths, SVT) -> Médecine
(10, 20, 105, 45), -- (Maths, SES) -> Licence Info, txReussite < 50%
(10, 40, 104, 25), -- (Maths, SVT) -> Ecole Vétérinaire
(30, 20, 106, 65); -- (Littérature, SES) -> Licence de Droit
GO

-- Vous pouvez maintenant vérifier que les données sont présentes :
SELECT * FROM [dbo].[adapter];

-- 9. Remplissage 'approprier' (Lien Filières <-> Métiers) [cite: 23, 79]
INSERT INTO [dbo].[approprier] (codFiliere, codMetier) VALUES
(100, 3), -- Eco Gestion -> Comptable [pour Q.a]
(100, 6), -- Eco Gestion -> Analyste Financier [pour Q.a]
(100, 4), -- Eco Gestion -> Manager
(105, 2), -- Info -> Data Scientist
(104, 1), -- Vétérinaire -> Assistant Vétérinaire [pour Q.i]
(102, 5), -- Médecine -> Médecin Généraliste [pour Q.d]
(101, 7), -- Manip Radio -> Radiologue
(106, 4), -- Droit -> Manager
(103, 4); -- SVT -> Manager [pour Q.j]
GO

-- 10. Remplissage 'offrir' (Lien Filières <-> Etablissements) [cite: 17, 78]
INSERT INTO [dbo].[offrir] (codFiliere, codEtab) VALUES
(100, 20), -- Eco Gestion (Dom 3) -> UT Capitole
(106, 20), -- Droit (Dom 5) -> UT Capitole [Etab 20 a 2 domaines, pour Q.f]
(101, 30), -- Manip Radio (Dom 1) -> Paul Sabatier [pour Q.c]
(103, 30), -- Licence SVT (Dom 2) -> Paul Sabatier [Etab 30 a 2 domaines, pour Q.c & Q.f]
(104, 10), -- Ecole Vétérinaire -> Ecole Vétérinaire [pour Q.i]
(102, 50), -- Médecine -> CHU Montpellier
(103, 40), -- Licence SVT -> Lycée Fermat [Filière 103 a 2 étab, pour Q.e]
(105, 30); -- Info -> Paul Sabatier [Etab 30 a 3 domaines]
GO
-- Etab 20 (UT Capitole) n'organise pas de concours [pour Q.h]

-- 11. Remplissage 'reorienter' (Lien Filière -> Filière) [cite: 16, 80]
INSERT INTO [dbo].[reorienter] (codFiliereActuelle, codFiliereNouvelle) VALUES
(100, 101), -- Eco Gestion -> Manip Radio (Dom 1, dossier) [pour Q.b]
(100, 102), -- Eco Gestion -> Médecine (Dom 1, concours) [filtré par Q.b]
(100, 103), -- Eco Gestion -> Licence SVT (Dom 2, dossier) [filtré par Q.b]
(105, 100); -- Info -> Eco Gestion
GO

-- 12. Remplissage 'decomposer' (Lien Concours <-> Etapes) [cite: 67, 80]
INSERT INTO [dbo].[decomposer] (codFiliereConcours, codEtape, noEtape) VALUES
(1, 1, 1), -- Concours Médecine -> Dépôt dossier
(1, 2, 2), -- Concours Médecine -> Examen candidatures
(1, 3, 3), -- Concours Médecine -> Épreuves écrites
(2, 1, 1), -- Concours Vétérinaire -> Dépôt dossier [pour Q.i]
(2, 3, 2), -- Concours Vétérinaire -> Épreuves écrites [pour Q.i]
(2, 4, 3); -- Concours Vétérinaire -> Épreuves orales [pour Q.i]
GO

-- 13. Remplissage 'organisation' (Lien Concours+Etab+Etape -> Dates) [cite: 21, 67, 80]
INSERT INTO [dbo].[organisation] (codFiliereConcours, codEtab, codEtape, dtDebutEtape, dtFinEtape) VALUES
(2, 10, 1, '2025-01-15', '2025-02-15'), -- Veto (FC 2) à Ecole Veto (E 10) - Etape 1 [pour Q.i]
(2, 10, 3, '2025-04-10', '2025-04-12'), -- Veto (FC 2) à Ecole Veto (E 10) - Etape 3 [pour Q.i]
(2, 10, 4, '2025-06-01', '2025-06-10'), -- Veto (FC 2) à Ecole Veto (E 10) - Etape 4 [pour Q.i]
(1, 50, 1, '2025-01-10', '2025-02-10'), -- Médecine (FC 1) à CHU Mtp (E 50) - Etape 1
(1, 50, 2, '2025-02-11', '2025-03-01'), -- Médecine (FC 1) à CHU Mtp (E 50) - Etape 2
(1, 50, 3, '2025-03-20', '2025-03-22'); -- Médecine (FC 1) à CHU Mtp (E 50) - Etape 3
GO
