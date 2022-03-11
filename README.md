# Projet 2 : Utiliser les bases de Python pour l'analyse de marché

## Objectif: 
À terme, notre objectif sera de suivre les prix des livres chez 
[Book To Scrape](http://books.toscrape.com/), un revendeur de livres en ligne. 

## Sommaire

[Feuille de route](#route)

[Feuille de route](#route)

[Feuille de route](#route)

------------
### <a name="installation"></a>Installation

[A écrire]

### <a name="utilisation"></a>Utilisation

[A écrire]

### <a name="route"></a> Feuille de Route
#### Etape 1 :Récupération, à la demande, des prix pratiqués
Nous procéderons en plusieurs itérations :

*Extraction d'un livre*
- [ ] **Extraire les informations concernant un seul livre**: 
     - product_page_url
     - universal_ product_code (upc)
     - title 
     - price_including_tax 
     - price_excluding_tax 
     - number_available
     - product_description 
     - category
     - review_rating
     - image_url
- [ ] **Ecrire ces informations dans un fichier CSV**; les champs ci-dessus
correspondront aux en-têtes de colonnes.

*Extraction des livres d'une catégorie*

- [ ] **Extraire les urls des livres attachés à une catégorie, présent 
sur une page catégorie**
- [ ] **Extraire les urls des livres attachés à une catégorie, présent 
sur l'ensemble des pages concernées par la catégorie**
- [ ] **extraire les données produit de tous les livres de la catégorie 
choisie,** 
- [ ] **Ecrire ces informations dans un seul fichier CSV**

*Extraction de l'ensemble des catégories puis des livres associés*
- [ ] Extraire les informations
- [ ] Pour chaque catégorie, écrire les informations dans un fichier CSV

* Télécharger et enregistrer le fichier image de chaque produit
