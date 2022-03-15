import os
import sys

import requests
from bs4 import BeautifulSoup
import csv

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
review_rating
image_url


"""
domaine = 'http://books.toscrape.com'


def extract_info_livre(url):
    print("[DEBUT]extract_info_livre:", url)
    page = requests.get(url)
    livre = {}

    if page.ok:
        livre['product_page_url'] = url
        try:
            soup = BeautifulSoup(page.content, 'html.parser')
            livre['upc'] = soup.find('th', string='UPC').find_next_sibling('td').string
            livre['title'] = soup.find('h1').string
            livre['price_including_tax'] = soup.find('th', string='Price (incl. tax)').find_next_sibling('td').string
            livre['price_excluding_tax'] = soup.find('th', string='Price (excl. tax)').find_next_sibling('td').string
            livre['number_available'] = soup.find('th', string='Availability').find_next_sibling('td').string
            livre['category'] = soup.find('ul', class_="breadcrumb").findAll("li")[-2].find("a").string
            livre['description'] = soup.find(id='product_description').find_next_sibling('p').string
            livre['review_rating'] = soup.find('p', class_='star-rating')['class'][1]
            livre['image_url'] = soup.find('div', class_='thumbnail').find('img')['src'].replace('../..', domaine)
        except AttributeError as exc:
            livre = {}
            raise ValueError("001:[extraction informations d'un livre]cette erreur se produit soit parce que l'url "
                             "de la page à extraire est erronée et/ou ne concerne pas une page livre")
    else:
        raise ValueError("002:[extraction informations d'un livre]cette erreur se produit au moment de l'extraction "
                         "d'une page de type livre; la page demandée n'est pas accessible")

    print("[FIN]extract_info_livre:", url, "infos:", livre)
    return livre


def extraire_urls_livres_par_categorie(url):
    print("[DEBUT]extract_urls_livre_par_catégorie:", url)
    def reforme_url(url, num_page):
        url_split = url.split('/')
        url_split = url_split[0:7]
        url_split.append('page-' + str(num_page) + ".html")
        url = "/".join(url_split)
        return url

    num_page = 1
    url_reforme = reforme_url(url, num_page)
    urls_livres = []
    page = requests.get(url_reforme)
    if not page.ok:
        raise ValueError("004:[extraction urls des livres d'une page categorie]cette erreur se produit au moment"
                         " de l'extraction d'une page de type livre; la page demandée n'est pas accessible")
    while page.ok:
        try:
            soup = BeautifulSoup(page.content, 'html.parser')
            links = soup.find_all("h3")

            for link in links:
                urls_livres.append(link.find("a")['href'].replace("../../..", domaine + "/catalogue"))
            print("[EN COURS]extract_urls_livre_par_catégorie page", num_page, "nombre de livres total:",
                  str(len(urls_livres)))
            num_page += 1
            url_reforme = reforme_url(url, num_page)
            page = requests.get(url_reforme)
            print("[FIN]extract_urls_livre_par_catégorie:", url_reforme)

        except AttributeError:
            raise ValueError("003:[extraction urls des livres d'une page categorie]cette erreur se produit "
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


def export_csv(livres):
    if len(livres) > 0:

        print("[DEBUT]export: de ", len(livres), "livre(s) dont le premier est :", livres[0])
        if not (os.path.exists("data")):
            os.mkdir("data")
        nom_du_fichier = "data/" + livres[0]['category'] + ".csv"

        en_tete = list(livres[0].keys())

        with open(nom_du_fichier, "w") as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=",")
            writer.writerow(en_tete)
            for livre in livres:
                ligne = list(livre.values())
                writer.writerow(ligne)
        print("[FIN]export: de ", len(livres), "livre(s) dont le dernier est :", livres[len(livres)-1])
    else:
        print("[WARNING] Aucun livre à exporter")


livres = []
'''
# url = "http://books.toscrape.com/catalogue/soumission_998/index.html"
url = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
livres = extract_info_livres_par_categorie(url)
export_csv(livres)
print(len(livres))
'''
try:
    print("Saisir 1 pour extraire les informations d'un livre et 2 pour les informations d'une catégorie, laisser vide"
          "pour quitter")
    choix = input()
    if choix in ["1", "2"]:
        url = -1
        while url:
            print(
                "Entrer l'url concernant les infos à extraire du site http://books.toscrape.com/ ou laisser vide pour quitter:")
            url = input()
            if url != "":
                if choix == "1":
                    livre = extract_info_livre(url)
                    if livre:
                        print(livre)

                        livres.append(livre)

                    if len(livres) > 0:
                        export_csv(livres)

                elif choix == "2":
                    livres = extract_info_livres_par_categorie(url)
                    export_csv(livres)

except ValueError as exc:
    print(exc)
