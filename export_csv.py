"""
Fonctionnalités en lien avec l'exportation d'information au format csv
"""

import csv
import os
from itertools import groupby

from log import logger


def export_csv(elements, regroupement_par):
    """
    Enregistre les elements dans un fichier csv
    :param regroupement_par: str
    :param elements: list
    :return: None
    """

    def key_func(k):
        return k[regroupement_par]

    if len(elements) > 0:
        elements = sorted(elements, key=key_func)

        logger.info("[DEBUT]export: de %s ligne(s) "
                    "dont le premier est : %s", len(elements), elements[0])
        if not os.path.exists("data"):
            os.mkdir("data")

        for key, value in groupby(elements, key_func):

            nom_du_fichier = "data/" + key + ".csv"

            elements_regroupes = list(value)
            en_tete = list(elements_regroupes[0].keys())

            with open(nom_du_fichier, "w", encoding="utf-8") as fichier_csv:
                writer = csv.writer(fichier_csv, delimiter=",")
                writer.writerow(en_tete)
                for element_regroupe in elements_regroupes:
                    ligne = list(element_regroupe.values())
                    writer.writerow(ligne)
        logger.info("[FIN]export")
    else:
        logger.info("[WARNING] Aucun élément à exporter")
