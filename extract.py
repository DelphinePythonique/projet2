"""
Functionality related to the extraction of information from the site http://books.toscrape.com/
"""

import os
import shutil

import requests
from bs4 import BeautifulSoup

from log import logger

DOMAIN = "https://books.toscrape.com/"

def extract_domain(url):
    """
    Return domain linked to l'url
    :param url
    :type url: str
    :return:
    :rtype: str
    """
    domain = url.split("/")[2]
    return f"https://{domain}"


def extract_book_datas(book_to_extract_url):
    """
    Extract book's datas

    :param book_to_extract_url : book's url concerning a book to extract
    :type book_to_extract_url: str
    :return: book_to_extract: book's datas dict
    :rtype:  dict

    >>> len(extract_book_datas("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/" \
    "index.html")) > 0
    True
    """

    logger.info("[BEGIN]extract_info_livre:%s", book_to_extract_url)
    page = requests.get(book_to_extract_url)
    book_to_extract = {}

    if page.ok:
        book_to_extract['product_page_url'] = book_to_extract_url
        try:
            soup = BeautifulSoup(page.content, 'html.parser')
            book_to_extract['upc'] = soup.find('th', string='UPC').find_next_sibling('td').string
            book_to_extract['title'] = soup.find('h1').string
            book_to_extract['price_including_tax'] = soup.find('th', string='Price (incl. tax)') \
                .find_next_sibling('td').string
            book_to_extract['price_excluding_tax'] = soup.find('th', string='Price (excl. tax)') \
                .find_next_sibling('td').string
            book_to_extract['number_available'] = soup.find('th', string='Availability') \
                .find_next_sibling('td').string
            book_to_extract['category'] = soup.find('ul', class_="breadcrumb") \
                .findAll("li")[-2].find("a").string
            if soup.find(id='product_description'):
                book_to_extract['description'] = soup.find(id='product_description') \
                    .find_next_sibling('p').string
            else:
                book_to_extract['description'] = ""

            book_to_extract['review_rating'] = soup.find('p', class_='star-rating')['class'][1]
            book_to_extract['image_url'] = soup.find('div', class_='thumbnail') \
                .find('img')['src'] \
                .replace('../..', extract_domain(book_to_extract_url))
        except AttributeError as erreur_extraction:
            raise ValueError("001:[Extract book's datas] This error is \n "
                             "in case page's url is not exist \n "
                             "and/or is not a book's page.\n "
                             "error:" + str(erreur_extraction)) from erreur_extraction
    else:
        raise ValueError(
            "002:[Extract book's datas]this erreur occurs if the requested page is not accessible")

    logger.info("[END]extract_info_livre:%s, infos:%s", book_to_extract_url, book_to_extract)
    return book_to_extract


def extract_urls_category(url_origin):
    """
    Extrait les urls des catégories de l'url du site transmis
    :param url_origin
    :type url_origin: str
    :return: urls_categories : list

    >>> len(extract_urls_category("http://books.toscrape.com/")) > 0
    True

    """
    page = requests.get(url_origin)
    if page.ok:
        logger.info("[BEGIN]export urls of categories from url %s", url_origin)
        soup = BeautifulSoup(page.content, "html.parser")
        links = soup.find('div', class_="side_categories").find_all('a')
        links.pop(0)  # delete of parent category Books
        urls_categories = []
        for link in links:
            urls_categories.append(url_origin + "/" + link['href'])
        logger.info("[END]export urls of catégories from url %s "
                    "of %s catégories", url_origin, len(urls_categories))

    else:
        raise ValueError("005:[extract urls of categories]this error occurs "
                         "when requested page is not accessible")
    return urls_categories


def reforme_url(url, num_page_active):
    url_split = url.split('/')
    url_split = url_split[0:7]
    url_split.append('page-' + str(num_page_active) + ".html")
    url = "/".join(url_split)
    return url


def extract_book_url_by_category(books_to_extract_category_url):
    """
     Extraction des urls des livres d'une catégorie

    :param books_to_extract_category_url
    :type books_to_extract_category_url:str
    :returns
    books_url list

    >>> len(extract_book_url_by_category("https://books.toscrape.com/catalogue/category/books/" \
    "mystery_3/index.html")) > 0
    True

    """

    num_page = 1

    books_url = []
    page = requests.get(books_to_extract_category_url)
    logger.info("[BEGIN]extract_book_url_by_category:%s", books_to_extract_category_url)
    if not page.ok:
        raise ValueError(
            "004:[extract urls of books from category url]this error occurs "
                         "when requested page is not accessible")
    while page.ok:
        try:
            soup = BeautifulSoup(page.content, 'html.parser')
            links = soup.find_all("h3")

            for link in links:
                books_url.append(
                    link.find("a")['href'].replace("../../..",
                                                   extract_domain(
                                                       books_to_extract_category_url)
                                                   + "/catalogue"))
            logger.info("[EN COURS]extract_urls_livre_par_catégorie page %s "
                        "nombre de livres total:%s", num_page, str(len(books_url)))
            num_page += 1
            url_reforme = reforme_url(books_to_extract_category_url, num_page)
            page = requests.get(url_reforme)
            logger.info("[FIN]extract_urls_livre_par_catégorie:%s", url_reforme)

        except AttributeError as extract_error:
            raise ValueError(
                "003:[extraction urls des livres d'une page category]this error occurs "
                "if page has evolved, or if page's url is wrong "
                "et/ou ne concerne pas une page catégorie") from extract_error

    return books_url


def extract_book_datas_by_category(books_to_extract_category_url):
    """
    Extracts datas about books corresponding to the urls transmitted
    :param books_to_extract_category_url: list
    :return: book_to_extract: list
    """
    url_livres = extract_book_url_by_category(books_to_extract_category_url)
    return [extract_book_datas(url) for url in url_livres]


def extract_all(url_origin = DOMAIN):
    """
    Extract book datas of all books
    :param url_origin: str
    :return: extract_books list
    """
    logger.info("[BEGIN]extraction of all books from :%s", url_origin)
    urls_category = extract_urls_category(url_origin)
    extract_books = []
    for url in urls_category:
        extract_books.extend(extract_book_datas_by_category(url))
    logger.info("[FIN]extraction of all books from :%s", url_origin)
    return extract_books


def extract_image(image_url, path, file_name):
    """
    Tdownload the image corresponding to the url_image
    :param image_url: str
    :param path: str
    :param file_name: str
    :return: none
    """
    logger.info("[DEBUT]Download image, path %s file name %s", path, file_name)
    path_exist = os.path.exists(path)
    if not path_exist:
        os.makedirs(path)
    page = requests.get(image_url, stream=True)
    if page.ok:
        page.raw.decode_content = True

        with open(path + file_name, 'wb') as fichier_image:
            shutil.copyfileobj(page.raw, fichier_image)
    logger.info("[END]Download image %s, path %s file name %s", image_url,
                path, file_name)
