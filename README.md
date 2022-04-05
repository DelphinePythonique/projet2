# project #2: Using Python Basics for Market Analysis

## Goals: 
Ultimately, our goal will be to track book prices at
[Book To Scrape](http://books.toscrape.com/), an online bookstore
. 

version: 1.7.2

## Summary

[Install](#install)

[Use](#use)

[Todo](TODO.md)

[Changelog](CHANGELOG.md)

------------
### <a name="install"></a>Install

This setup is for a development environment.

Prerequisite:

- \>= python3,9

Through a terminal(Debian linux) or Powershell(Windows) : 

Position yourself in the local directory in which you want to position the sources of the application
``` bash
 cd [path_to_source_directory]
```
-  Clone the repository via the clone command in ssh mode
[ssh](https://docs.github.com/en/authentication/connecting-to-github-with-ssh), via la commande suivante

``` bash
 git clone git@github.com:DelphinePythonique/projet2.git
```

- Position yourself in the project directory, create a virtual environment

``` bash
 cd projet2
 python -m venv env
```
- Activate virtual environment

   If OS is Debian Linux: 
``` bash
 source env/bin/activate
```
   If OS is Windows:
``` bash
 .\env\Scripts\activate
```
- Install the python packages useful for the script
``` bash
 pip install -r requirements.txt 
```

### <a name="use"></a>Uses

#### Extract book's datas 
Enter the following command
``` bash
 python main.py --url=[book's url] --impact=book
```
Add option --csv to generate a csv file in the data directory
``` bash
 python main.py --url=[book's url] --impact=book --csv
```

#### Extract a category's books's data  
Enter the following command
``` bash
 python main.py --url=[category's url] --impact=cat
```
Add option --csv to generate a csv file in the data directory
``` bash
 python main.py --url=[category's url] --impact=cat --csv
```
#### Extraction all books's datas 
Enter the following command
``` bash
 python main.py --all
```
Add option --csv to generate a csv file in the data directory per category

``` bash
 python main.py --all --csv
```

#### Download et save book's image in data/images directory
*Before to execute this command, you must ensure to have download csv files;
indeed, this command is based on the images's urls present in the files.*
Enter the following command
``` bash
 python main.py --images
```
File's format is  [book's upc].jpg
