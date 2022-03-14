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
    page = requests.get(url)
    livre = {}
    status = "000:extraction ok"
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
        except AttributeError:
            livre = {}
            status = "001:problème d'attribut lors de l'extraction"
    else:
        status = "002:page inaccessible lors de l'extraction"

    return status, livre


def export_csv(livres):
    status = "000:export csv ok"
    if not (os.path.exists("data")):
        os.mkdir("data")
    nom_du_fichier = "data/"+livres[0]['category'] + ".csv"
    en_tete = []
    en_tete = list(livres[0].keys())

    with open(nom_du_fichier, "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=",")
        writer.writerow(en_tete)
        for livre in livres:
            ligne = list(livre.values())
            writer.writerow(ligne)

    return status


livres = []

#url = "http://books.toscrape.com/catalogue/soumission_998/index.html"

url = -1
while url:
    print("Entrer l'url d'une page d'un livre du site http://books.toscrape.com/ ou laisser vide pour quitter:")
    url = input()
    if url != "":
        status, livre = extract_info_livre(url)
        if livre:
            print(livre)
            print(status)

            livres.append(livre)
        if len(livres) > 0:
            resultat = export_csv(livres)
            print(resultat)


