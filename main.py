"""
Extract books's datas from website  http://books.toscrape.com/, depending on several
criteria
"""

import argparse

from extract import extract_datas_book
from extract import extract_book_datas_by_category
from extract import extract_all
from export_csv import export_csv
from images import images_download


def main():

    livres = []

    parser = argparse.ArgumentParser(
        description="extract book's datas "
                    "http://books.toscrape.com/")
    parser.add_argument("--csv", action="store_true",
                        help="save datas into csv file")
    parser.add_argument("--all", action="store_true",
                        help="extract all books ")
    parser.add_argument("--url",
                        help="url of the page from which to extract the datas")
    parser.add_argument("--images", action="store_true",
                        help="Save images into data/images")
    parser.add_argument("--impact", choices=['book', 'cat', 'all'],
                        help="Extract book's data with type=book "
                             "or from category with type=cat "
                        )

    args = parser.parse_args()

    if args.url and (args.impact is None):
        parser.error("--url requiert --impact.")

    if args.csv and ((args.impact is None or args.url is None) and not args.all):
        parser.error("--csv requiert --impact et --url, or --all.")

    if args.impact and (args.url is None):
        parser.error("--impact requiert --url.")

    try:
        if args.url and args.impact == 'book':
            livre = extract_datas_book(args.url)
            if livre:
                livres.append(livre)
                if args.csv:
                    export_csv(livres, 'category')
                else:
                    print(livre)
        elif args.url and args.impact == 'cat':
            livres = extract_book_datas_by_category(args.url)
            if livres:
                if args.csv:
                    export_csv(livres, 'category')
                else:
                    print(livres)
        elif args.all:
            livres = extract_all()
            if livres:
                if args.csv:
                    export_csv(livres, 'category')
                else:
                    print(livres)

        if args.images:
            images_download()
    except ValueError as exc:
        print(exc)


if __name__ == '__main__':
    main()
