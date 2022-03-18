"""
Fonctionnalités en lien avec l'enregistrement d'image
"""

import csv
import os
from extract import extract_image


def telecharger_images():
    """
    Télécharge les images dont l'url_image est reprise dans les fichiers csv générés par
    l'application et les mémorise dans le répertoire data/images
    :return:
    """
    path = "data"
    files = os.listdir(path)
    for file in files:
        if file.endswith('.csv'):
            with open(path + "/" + file, encoding="utf-8") as fichier_csv:
                dict_reader = csv.DictReader(fichier_csv, delimiter=",")
                for row in dict_reader:
                    url = row['image_url']
                    nom_fichier_a_telecharger = row['upc'] + ".jpg"
                    extract_image(url, "data/images/", nom_fichier_a_telecharger)
