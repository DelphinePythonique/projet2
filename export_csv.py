"""
Features related to exporting information in csv format
"""

import csv
import os
from itertools import groupby

from log import logger


def export_csv(elements, grouped_by):
    """
    Save items to a csv file
    :param grouped_by: str
    :param elements: list
    :return: None
    """

    def find_grouping_field_value(k): #for exemple grouping_field_value's value
        return k[grouped_by]

    if len(elements) > 0:
        elements = sorted(elements, key=find_grouping_field_value)

        logger.info("[BEGIN]export: of %s line(s) "
                    "the first is : %s", len(elements), elements[0])
        if not os.path.exists("data"):
            os.mkdir("data")

        for grouping_field_value, value in groupby(elements, find_grouping_field_value):

            file_name = f"data/{grouping_field_value}.csv"

            grouped_elements = list(value)
            en_tete = list(grouped_elements[0].keys())

            with open(file_name, "w", encoding="utf-8", newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=",")
                writer.writerow(en_tete)
                for grouped_element in grouped_elements:
                    line = list(grouped_element.values())
                    writer.writerow(line)
        logger.info("[END]export")
    else:
        logger.info("[WARNING] no element to export")
