'''
Script d'extractiopn des livres du site http://books.toscrape.com/, en fonction de plusieurs
critères
'''
import argparse
import os
import shutil

import csv
import requests
from bs4 import BeautifulSoup

# ajout de ce commentaire pour juste tester le workflow github pylint

DOMAINE = 'http://books.toscrape.com'


def extract_info_livre(url_du_livre_a_extraire):
    """
    Extraction des informations d'un livre
    :param url_du_livre_a_extraire: string
    :return:  livre_a_extraire : dict
    """
    print("[DEBUT]extract_info_livre:", url_du_livre_a_extraire)
    page = requests.get(url_du_livre_a_extraire)
    livre_a_extraire = {}

    if page.ok:
        livre_a_extraire['product_page_url'] = url_du_livre_a_extraire
        try:
            soup = BeautifulSoup(page.content, 'html.parser')
            livre_a_extraire['upc'] = soup.find('th', string='UPC').find_next_sibling('td').string
            livre_a_extraire['title'] = soup.find('h1').string
            livre_a_extraire['price_including_tax'] = soup.find('th', string='Price (incl. tax)') \
                .find_next_sibling('td').string
            livre_a_extraire['price_excluding_tax'] = soup.find('th', string='Price (excl. tax)') \
                .find_next_sibling('td').string
            livre_a_extraire['number_available'] = soup.find('th', string='Availability') \
                .find_next_sibling('td').string
            livre_a_extraire['category'] = soup.find('ul', class_="breadcrumb") \
                .findAll("li")[-2].find("a").string
            if soup.find(id='product_description'):
                livre_a_extraire['description'] = soup.find(id='product_description') \
                    .find_next_sibling('p').string
            else:
                livre_a_extraire['description'] = ""

            livre_a_extraire['review_rating'] = soup.find('p', class_='star-rating')['class'][1]
            livre_a_extraire['image_url'] = soup.find('div', class_='thumbnail').find('img')['src']\
                .replace('../..', DOMAINE)
        except AttributeError as erreur_extraction:
            raise ValueError("001:[extraction informations d'un livre]cette erreur se produit \n "
                             "soit parce que l'url de la page à extraire est erronée\n "
                             "et/ou ne concerne pas une page livre.\n "
                             "Detail de l'erreur:" + str(erreur_extraction)) from erreur_extraction
    else:
        raise ValueError(
            "002:[extraction informations d'un livre]cette erreur se produit au moment de "
            "l'extraction d'une page de type livre; la page demandée n'est pas accessible")

    print("[FIN]extract_info_livre:", url_du_livre_a_extraire, "infos:", livre_a_extraire)
    return livre_a_extraire


def extraire_urls_livres_par_categorie(url_categorie_des_livres_a_extraire):
    """
     Extraction des urls des livres d'une catégorie
    :param url_categorie_des_livres_a_extraire: string
    :return: urls_livres list
    """

    def reforme_url(url, num_page):
        url_split = url.split('/')
        url_split = url_split[0:7]
        url_split.append('page-' + str(num_page) + ".html")
        url = "/".join(url_split)
        return url

    num_page = 1

    urls_livres = []
    page = requests.get(url_categorie_des_livres_a_extraire)
    print("[DEBUT]extract_urls_livre_par_catégorie:", url_categorie_des_livres_a_extraire)
    if not page.ok:
        raise ValueError(
            "004:[extraction urls des livres d'une page categorie]cette erreur se produit au moment"
            " de l'extraction d'une page de type livre; la page demandée n'est pas accessible")
    while page.ok:
        try:
            soup = BeautifulSoup(page.content, 'html.parser')
            links = soup.find_all("h3")

            for link in links:
                urls_livres.append(
                    link.find("a")['href'].replace("../../..", DOMAINE + "/catalogue"))
            print("[EN COURS]extract_urls_livre_par_catégorie page", num_page,
                  "nombre de livres total:",
                  str(len(urls_livres)))
            num_page += 1
            url_reforme = reforme_url(url_categorie_des_livres_a_extraire, num_page)
            page = requests.get(url_reforme)
            print("[FIN]extract_urls_livre_par_catégorie:", url_reforme)

        except AttributeError as erreur_extraction:
            raise ValueError(
                "003:[extraction urls des livres d'une page categorie]cette erreur se produit "
                "soit la page a évoluée, soit l'url de la page à extraire est erronée "
                "et/ou ne concerne pas une page catégorie") from erreur_extraction

    return urls_livres


def extract_info_livres_par_categorie(url_categorie_livres_a_extraire):
    '''
    Extrait les informations concernant des livres correspondant aux urls transmises
    :param url_categorie_livres_a_extraire: list
    :return: livres_a_extraire: list
    '''
    url_livres = extraire_urls_livres_par_categorie(url_categorie_livres_a_extraire)
    livres_a_extraire = []
    for url in url_livres:
        livres_a_extraire.append(extract_info_livre(url))
    return livres_a_extraire


def extract_urls_categorie(url_origine):
    '''
    Extrait les urls des catégories de l'url du site transmis
    :param url_origine: str
    :return: urls_categorie : list
    '''
    page = requests.get(url_origine)
    if page.ok:
        print("[DEBUT]export urls des categories à partir de l'url", url_origine)
        soup = BeautifulSoup(page.content, "html.parser")
        links = soup.find('div', class_="side_categories").find_all('a')
        links.pop(0)  # suppression de la catégorie parent Books
        urls_categorie = []
        for link in links:
            urls_categorie.append(url_origine + link['href'])
        print("[FIN]export urls des catégories à partir de l'url", url_origine, "de ",
              len(urls_categorie), " catégories")

    else:
        raise ValueError("005:[extraction urls des categories]cette erreur se produit "
                         "car la page demandée n'est pas accessible")
    return urls_categorie


def extract_all(url_origine):
    '''
    Génère les fichiers csv de l'ensemble des livres; avec un fichier csv par catégorie de livre
    :param url_origine: str
    :return: None
    '''
    print("[DEBUT]extraction intégral de:", url_origine)
    urls_categorie = extract_urls_categorie(url_origine)
    for url in urls_categorie:
        elements = extract_info_livres_par_categorie(url)
        export_csv(elements)
    print("[FIN]extraction intégral de:", url_origine)


def export_csv(elements):
    '''
    Enregistre les elements dans un fichier csv
    :param elements: list
    :return: None
    '''
    if len(elements) > 0:

        print("[DEBUT]export: de ", len(elements), "livre(s) dont le premier est :", elements[0])
        if not os.path.exists("data"):
            os.mkdir("data")
        nom_du_fichier = "data/" + elements[0]['category'] + ".csv"

        en_tete = list(elements[0].keys())

        with open(nom_du_fichier, "w", encoding="utf-8") as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=",")
            writer.writerow(en_tete)
            for element in elements:
                ligne = list(element.values())
                writer.writerow(ligne)
        print("[FIN]export: de ", len(elements), "livre(s) dont le dernier est :",
              elements[len(elements) - 1])
    else:
        print("[WARNING] Aucun livre à exporter")


def telecharger_image(url_de_l_image, path, nom_fichier):
    '''
    Télécharge l'image correspondant à l'url_image
    :param url_de_l_image: str
    :param path: str
    :param nom_fichier: str
    :return: none
    '''
    print("[DEBUT]Télécharger image  ", "chemin", path, "nom fichier ", nom_fichier)
    path_exist = os.path.exists(path)
    if not path_exist:
        os.makedirs(path)
    page = requests.get(url_de_l_image, stream=True)
    if page.ok:
        page.raw.decode_content = True

        with open(path + nom_fichier, 'wb') as fichier_image:
            shutil.copyfileobj(page.raw, fichier_image)
    print("[FIN]Télécharger image  ", url_de_l_image, "chemin", path, "nom fichier ", nom_fichier)


def telecharger_images():
    '''
    Télécharge les images dont l'url_image est reprise dans les fichiers csv générés par
    l'application et les mémorise dans le répertoire data/images
    :return:
    '''
    path = "data"
    files = os.listdir(path)
    for file in files:
        if file.endswith('.csv'):
            with open(path + "/" + file, encoding="utf-8") as fichier_csv:
                dict_reader = csv.DictReader(fichier_csv, delimiter=",")
                for row in dict_reader:
                    url = row['image_url']
                    nom_fichier_a_telecharger = row['upc'] + ".jpg"
                    telecharger_image(url, "data/images/", nom_fichier_a_telecharger)


livres = []

parser = argparse.ArgumentParser(
    description="exporter les informations concernant les livres du site "
                "http://books.toscrape.com/")
parser.add_argument("--csv", action="store_true",
                    help="Export les informations dans un fichier CSV présent dans data")
parser.add_argument("--url",
                    help="Indiquer l'url de la page à partir de laquelle exporter les informations")
parser.add_argument("--images", action="store_true",
                    help="Télécharge et enregistre les images dans data/images")
parser.add_argument("--impact", choices=['livre', 'cat', 'tout'],
                    help="Extrait les informations d'un livre avec type=livre "
                         "ou d'une categorie type=cat, "
                         "ou de l'ensemble des livres avec type=tout; tout génère automatiquement "
                         "les CSV")

args = parser.parse_args()

if args.url and (args.impact is None):
    parser.error("--url requiert --impact.")

if args.csv and (args.impact is None or args.url is None):
    parser.error("--csv requiert --impact et --url.")

if args.impact and (args.url is None):
    parser.error("--impact requiert --url.")

try:
    if args.url and args.impact == 'livre':
        livre = extract_info_livre(args.url)
        if livre:
            livres.append(livre)
            if args.csv:
                export_csv(livres)
            else:
                print(livre)
    elif args.url and args.impact == 'cat':
        livres = extract_info_livres_par_categorie(args.url)
        if livres:
            if args.csv:
                export_csv(livres)
            else:
                print(livres)
    elif args.url and args.impact == 'tout':
        extract_all(args.url)

    if args.images:
        telecharger_images()
except ValueError as exc:
    print(exc)
