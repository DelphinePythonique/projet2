"""
 Fonctionnalités en lien avec l'extraction d'information du site http://books.toscrape.com/
"""

import os
import shutil

from log import logger
import requests
from bs4 import BeautifulSoup


def extract_domaine(url):
    return url.split("/")[0]


def extract_info_livre(url_du_livre_a_extraire):
    """
    Extraction des informations d'un livre

    :param url_du_livre_a_extraire : Url de la page concernant un livre à extraire
    :type url_du_livre_a_extraire: str
    :return: livre_a_extraire: Dictionnaire contenant l'ensemble des informations du livre
    :rtype:  dict

    >>> extract_info_livre(
    ... "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    ... )  # doctest: +NORMALIZE_WHITESPACE
    {'product_page_url':
    'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html',
    'upc': 'a897fe39b1053632',
    'title': 'A Light in the Attic',
    'price_including_tax': '£51.77',
    'price_excluding_tax': '£51.77',
    'number_available': 'In stock (22 available)',
    'category': 'Poetry', 'description': "It's hard to imagine a world without A Light
    in the Attic. This now-classic collection of poetry and drawings from Shel Silverstein
    celebrates its 20th anniversary with this special edition. Silverstein's humorous and creative
    verse can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still and read
    these rhythmic words and laugh and smile and love th It's hard to imagine a world without A
    Light in the Attic. This now-classic collection of poetry and drawings from Shel Silverstein
    celebrates its 20th anniversary with this special edition. Silverstein's humorous and creative
    verse can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still and read
    these rhythmic words and laugh and smile and love that Silverstein. Need proof of his genius?
    RockabyeRockabye baby, in the treetopDon't you know a treetopIs no safe place to rock?And
    who put you up there,And your cradle, too?Baby, I think someone down here'sGot it in for you.
    Shel, you never sounded so good. ...more",
    'review_rating': 'Three',
    'image_url': 'https:/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg'}
    """

    logger.info("[DEBUT]extract_info_livre:%s", url_du_livre_a_extraire)
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
            livre_a_extraire['image_url'] = soup.find('div', class_='thumbnail') \
                .find('img')['src'] \
                .replace('../..', extract_domaine(url_du_livre_a_extraire))
        except AttributeError as erreur_extraction:
            raise ValueError("001:[extraction informations d'un livre]cette erreur se produit \n "
                             "soit parce que l'url de la page à extraire est erronée\n "
                             "et/ou ne concerne pas une page livre.\n "
                             "Detail de l'erreur:" + str(erreur_extraction)) from erreur_extraction
    else:
        raise ValueError(
            "002:[extraction informations d'un livre]cette erreur se produit au moment de "
            "l'extraction d'une page de type livre; la page demandée n'est pas accessible")

    logger.info("[FIN]extract_info_livre:%s, infos:%s", url_du_livre_a_extraire, livre_a_extraire)
    return livre_a_extraire


def extract_urls_categorie(url_origine):
    """
    Extrait les urls des catégories de l'url du site transmis
    :param url_origine
    :type url_origine: str
    :return: urls_categorie : list

    >>> len(extract_urls_categorie("http://books.toscrape.com/")) > 0
    True

    """
    page = requests.get(url_origine)
    if page.ok:
        logger.info("[DEBUT]export urls des categories à partir de l'url %s", url_origine)
        soup = BeautifulSoup(page.content, "html.parser")
        links = soup.find('div', class_="side_categories").find_all('a')
        links.pop(0)  # suppression de la catégorie parent Books
        urls_categorie = []
        for link in links:
            urls_categorie.append(url_origine + "/" + link['href'])
        logger.info("[FIN]export urls des catégories à partir de l'url %s "
                    "de %s catégories", url_origine, len(urls_categorie))

    else:
        raise ValueError("005:[extraction urls des categories]cette erreur se produit "
                         "car la page demandée n'est pas accessible")
    return urls_categorie


def extraire_urls_livres_par_categorie(url_categorie_des_livres_a_extraire):
    """
     Extraction des urls des livres d'une catégorie

    :param url_categorie_des_livres_a_extraire
    :type url_categorie_des_livres_a_extraire:str
    :returns
    urls_livres list

    """

    def reforme_url(url, num_page_active):
        url_split = url.split('/')
        url_split = url_split[0:7]
        url_split.append('page-' + str(num_page_active) + ".html")
        url = "/".join(url_split)
        return url

    num_page = 1

    urls_livres = []
    page = requests.get(url_categorie_des_livres_a_extraire)
    logger.info("[DEBUT]extract_urls_livre_par_catégorie:%s", url_categorie_des_livres_a_extraire)
    if not page.ok:
        raise ValueError(
            "004:[extraction urls des livres d'une page categorie]cette erreur se produit "
            "au moment de l'extraction d'une page de type livre; la page demandée "
            "n'est pas accessible")
    while page.ok:
        try:
            soup = BeautifulSoup(page.content, 'html.parser')
            links = soup.find_all("h3")

            for link in links:
                urls_livres.append(
                    link.find("a")['href'].replace("../../..",
                                                   extract_domaine(
                                                       url_categorie_des_livres_a_extraire)
                                                   + "/catalogue"))
            logger.info("[EN COURS]extract_urls_livre_par_catégorie page %s "
                        "nombre de livres total:%s", num_page, str(len(urls_livres)))
            num_page += 1
            url_reforme = reforme_url(url_categorie_des_livres_a_extraire, num_page)
            page = requests.get(url_reforme)
            logger.info("[FIN]extract_urls_livre_par_catégorie:%s", url_reforme)

        except AttributeError as erreur_extraction:
            raise ValueError(
                "003:[extraction urls des livres d'une page categorie]cette erreur se produit "
                "soit la page a évoluée, soit l'url de la page à extraire est erronée "
                "et/ou ne concerne pas une page catégorie") from erreur_extraction

    return urls_livres


def extract_info_livres_par_categorie(url_categorie_livres_a_extraire):
    """
    Extrait les informations concernant des livres correspondant aux urls transmises
    :param url_categorie_livres_a_extraire: list
    :return: livres_a_extraire: list
    """
    url_livres = extraire_urls_livres_par_categorie(url_categorie_livres_a_extraire)
    livres_a_extraire = []
    for url in url_livres:
        livres_a_extraire.append(extract_info_livre(url))
    return livres_a_extraire


def extract_all(url_origine):
    """
    Génère les fichiers csv de l'ensemble des livres; avec un fichier csv par catégorie de livre
    :param url_origine: str
    :return: livres_extraits list
    """
    logger.info("[DEBUT]extraction intégral de:%s", url_origine)
    urls_categorie = extract_urls_categorie(url_origine)
    livres_extraits = []
    for url in urls_categorie:
        livres_extraits.extend(extract_info_livres_par_categorie(url))
    logger.info("[FIN]extraction intégral de:%s", url_origine)
    return livres_extraits


def extract_image(url_de_l_image, path, nom_fichier):
    """
    Télécharge l'image correspondant à l'url_image
    :param url_de_l_image: str
    :param path: str
    :param nom_fichier: str
    :return: none
    """
    logger.info("[DEBUT]Télécharger image, chemin %s nom fichier %s", path, nom_fichier)
    path_exist = os.path.exists(path)
    if not path_exist:
        os.makedirs(path)
    page = requests.get(url_de_l_image, stream=True)
    if page.ok:
        page.raw.decode_content = True

        with open(path + nom_fichier, 'wb') as fichier_image:
            shutil.copyfileobj(page.raw, fichier_image)
    logger.info("[FIN]Télécharger image %s chemin %s nom fichier %s", url_de_l_image,
                path, nom_fichier)
