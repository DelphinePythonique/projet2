# Projet 2 : Utiliser les bases de Python pour l'analyse de marché

## Objectif: 
À terme, notre objectif sera de suivre les prix des livres chez 
[Book To Scrape](http://books.toscrape.com/), un revendeur de livres en ligne. 

version: 1.6.1

## Sommaire

[Installation](#installation)

[Utilisation](#utilisation)

[Feuille de route](#route)

[Changelog](#changelog)

------------
### <a name="installation"></a>Installation

Cette installation concerne un environnement de développement.

Pré-requis: 

- \>= python3,9

Via un terminal : 

- Se positionner dans le répertoire local dans lequel vous voulez positionner les sources de l'application
``` bash
 cd [chemin_vers_mon_repertoire_de_sources]
```
-  Cloner le dépot via la commande clone en mode ssh
[ssh](https://docs.github.com/en/authentication/connecting-to-github-with-ssh), via la commande suivante

``` bash
 git clone git@github.com:DelphinePythonique/projet2.git
```

- Se positionner dans le répertoire du projet, créer et activer un environnement virtuel
``` bash
 cd projet
 python -m venv env
 source env/bin/activate
```
- Installer les packages python utiles au script
``` bash
 pip install -r requirements.txt 
```

### <a name="utilisation"></a>Utilisation

#### Extraction des informations d'un livre, 
Saisir la commande suivante
``` bash
 python script.py --url=[url du livre] --impact=livre
```
Ajouter l'option --csv pour générer un fichier csv dans le répertoire data
``` bash
 python script.py --url=[url du livre] --impact=livre --csv
```

#### Extraction des informations d'une catégorie de livre, 
Saisir la commande suivante
``` bash
 python script.py --url=[url d'une catégorie] --impact=cat
```
Ajouter l'option --csv pour générer un fichier csv dans le répertoire data
``` bash
 python script.py --url=[url d'une catégorie] --impact=cat --csv
```
#### Extraction des informations de l'ensemble des livres, 
Saisir la commande suivante
``` bash
 python script.py --url=[url du site] --impact=tout
```
Cela exporte l'ensemble des informations des livres dans des fichiers csv;
un fichier CSV par catégorie de livre

#### Télécharger et enregistrer les images des livres 
Saisir la commande suivante
``` bash
 python script.py --images
```
Cela enregistre les fichiers images des livres dans le répertoire data/images. 
Le nom du fichier est de la forme [upc du livre].jpg
### <a name="route"></a> Feuille de Route
#### Etape 1 :Récupération, à la demande, des prix pratiqués
Nous procéderons en plusieurs itérations :

*Extraction d'un livre*
- [X] **Extraire les informations concernant un seul livre**: 
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
- [X] **Ecrire ces informations dans un fichier CSV**; les champs ci-dessus
correspondront aux en-têtes de colonnes.

*Extraction des livres d'une catégorie*

- [X] **extraire les urls des livres attachés à une catégorie, présent 
sur une page catégorie**
- [X] **extraire les urls des livres attachés à une catégorie, présent 
sur l'ensemble des pages concernées par la catégorie**
- [X] **extraire les données produit de tous les livres de la catégorie 
choisie** 
- [X] **écrire ces informations dans un seul fichier CSV**

*Extraction de l'ensemble des catégories puis des livres associés*
- [X] Extraire les informations
- [X] Pour chaque catégorie, écrire les informations dans un fichier CSV

*Télécharger et enregistrer le fichier image de chaque produit*
- [x] Télécharger et enregitrer une image
- [x] Télécharger et enregistrer l'ensemble des images

### <a name="Changelog"></a>Changelog

- v1.0.0: extraction des informations du livre de l'url 
"http://books.toscrape.com/catalogue/soumission_998/index.html"
- v1.1.0: Ajout d'un prompt pour selectionner une page d'une livre à extraire
- v1.2.0: Export csv des informations du livre
- v1.3.0: Export csv des informations des livres d'une catégorie
- v1.4.0: Extraction de l'ensemble des catégories du site et les livres liés.
- v1.5.0: Télécharger et enregistrer le fichier image de chaque produit
- v1.6.0: Fonctionnalités accessibles en lignes de commandes.