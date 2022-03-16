import argparse
import os
import shutil

import csv
import requests
from bs4 import BeautifulSoup

"""
Liste des champs à récupérer
x product_page_url
x universal_ product_code (upc)
x title
* price_including_tax
* price_excluding_tax
x number_available
x product_description
x category
x review_rating
x image_url
"""
# ajout de ce commentaire pour juste tester le workflow github pylint

domaine = 'http://books.toscrape.com'


def extract_info_livre(url):
    print("[DEBUT]extract_info_livre:", url)
    page = requests.get(url)
    element = {}

    if page.ok:
        element['product_page_url'] = url
        try:
            soup = BeautifulSoup(page.content, 'html.parser')
            element['upc'] = soup.find('th', string='UPC').find_next_sibling('td').string
            element['title'] = soup.find('h1').string
            element['price_including_tax'] = soup.find('th', string='Price (incl. tax)')\
                .find_next_sibling('td').string
            element['price_excluding_tax'] = soup.find('th', string='Price (excl. tax)')\
                .find_next_sibling('td').string
            element['number_available'] = soup.find('th', string='Availability')\
                .find_next_sibling( 'td').string
            element['category'] = soup.find('ul', class_="breadcrumb")\
                .findAll("li")[-2].find("a").string
            if soup.find(id='product_description'):
                element['description'] = soup.find(id='product_description')\
                    .find_next_sibling('p').string
            else:
                element['description'] = ""

            element['review_rating'] = soup.find('p', class_='star-rating')['class'][1]
            element['image_url'] = soup.find('div', class_='thumbnail').find('img')['src']\
                .replace('../..', domaine)
        except AttributeError as exc:
            element = {}
            raise ValueError("001:[extraction informations d'un livre]cette erreur se produit \n "
                             "soit parce que l'url de la page à extraire est erronée\n "
                             "et/ou ne concerne pas une page livre.\n "
                             "Detail de l'erreur:" + str(exc))
    else:
        raise ValueError(
            "002:[extraction informations d'un livre]cette erreur se produit au moment de "
            "l'extraction d'une page de type livre; la page demandée n'est pas accessible")

    print("[FIN]extract_info_livre:", url, "infos:", element)
    return element


def extraire_urls_livres_par_categorie(url):
    def reforme_url(url, num_page):
        url_split = url.split('/')
        url_split = url_split[0:7]
        url_split.append('page-' + str(num_page) + ".html")
        url = "/".join(url_split)
        return url

    num_page = 1

    urls_livres = []
    page = requests.get(url)
    print("[DEBUT]extract_urls_livre_par_catégorie:", url)
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
                    link.find("a")['href'].replace("../../..", domaine + "/catalogue"))
            print("[EN COURS]extract_urls_livre_par_catégorie page", num_page,
                  "nombre de livres total:",
                  str(len(urls_livres)))
            num_page += 1
            url_reforme = reforme_url(url, num_page)
            page = requests.get(url_reforme)
            print("[FIN]extract_urls_livre_par_catégorie:", url_reforme)

        except AttributeError:
            raise ValueError(
                "003:[extraction urls des livres d'une page categorie]cette erreur se produit "
                "soit la page a évoluée, soit l'url de la page à extraire est erronée "
                "et/ou ne concerne pas une page catégorie")
            urls_livres = []
    return urls_livres


def extract_info_livres_par_categorie(url_categorie):
    url_livres = extraire_urls_livres_par_categorie(url_categorie)
    livres = []
    for url in url_livres:
        livres.append(extract_info_livre(url))
    return livres


def extract_urls_categorie(url_origine):
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
        return urls_categorie
    else:
        raise ValueError("005:[extraction urls des categories]cette erreur se produit "
                         "car la page demandée n'est pas accessible")


def extract_all(url_origine):
    print("[DEBUT]extraction intégral de:", url_origine)
    urls_categorie = extract_urls_categorie(url_origine)
    for url in urls_categorie:
        elements = extract_info_livres_par_categorie(url)
        export_csv(elements)
    print("[FIN]extraction intégral de:", url_origine)


def export_csv(elements):
    if len(elements) > 0:

        print("[DEBUT]export: de ", len(elements), "livre(s) dont le premier est :", elements[0])
        if not (os.path.exists("data")):
            os.mkdir("data")
        nom_du_fichier = "data/" + elements[0]['category'] + ".csv"

        en_tete = list(elements[0].keys())

        with open(nom_du_fichier, "w") as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=",")
            writer.writerow(en_tete)
            for element in elements:
                ligne = list(element.values())
                writer.writerow(ligne)
        print("[FIN]export: de ", len(elements), "livre(s) dont le dernier est :",
              elements[len(elements) - 1])
    else:
        print("[WARNING] Aucun livre à exporter")


def telecharger_image(url, path, nom_fichier):
    print("[DEBUT]Télécharger image  ", url, "chemin", path, "nom fichier ", nom_fichier)
    path_exist = os.path.exists(path)
    if not path_exist:
        os.makedirs(path)
    page = requests.get(url, stream=True)
    if page.ok:
        page.raw.decode_content = True

        with open(path + nom_fichier, 'wb') as fichier_image:
            shutil.copyfileobj(page.raw, fichier_image)
    print("[FIN]Télécharger image  ", url, "chemin", path, "nom fichier ", nom_fichier)


def telecharger_images():
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
