"""
Script d'extraction des livres du site http://books.toscrape.com/, en fonction de plusieurs
critères
"""

import argparse

from extract import extract_info_livre
from extract import extract_info_livres_par_categorie
from extract import extract_all
from export_csv import export_csv
from images import telecharger_images

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
                export_csv(livres, 'category')
            else:
                print(livre)
    elif args.url and args.impact == 'cat':
        livres = extract_info_livres_par_categorie(args.url)
        if livres:
            if args.csv:
                export_csv(livres, 'category')
            else:
                print(livres)
    elif args.url and args.impact == 'tout':
        livres = extract_all(args.url)
        if livres:
            if args.csv:
                export_csv(livres, 'category')
            else:
                print(livres)

    if args.images:
        telecharger_images()
except ValueError as exc:
    print(exc)
