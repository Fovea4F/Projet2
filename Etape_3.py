import requests
import re

from bs4 import BeautifulSoup



"""def extraction_donnees_du_livre(url):




    # Récupère toutes les données brutes concernant le livre dont l'url est 
    # passée en paramètre


    import requests
    import re

    from bs4 import BeautifulSoup

    # url = "https://books.toscrape.com/catalogue/the-death-of-humanity-and-the-case-for-life_932/index.html"

    TIMEOUT_REQUEST = 15

    donnees = {}

    page_html = requests.get(url, timeout=TIMEOUT_REQUEST)

    soup = BeautifulSoup(page_html.content, 'html.parser')

    selection_html = soup.select('#content_inner > article > ul > li:nth-child(1) > article > h3')
    # print(f"Selection_html : {selection_html}")
    title = 'nc'
    url_livre = 'nc'
    if selection_html:
        detail_livre = {}
        for element in selection_html:
            extrait = element.find('a')
            title = extrait.get('title')
            url_livre = extrait.get('href')

    selection_html = soup.select("table tr")

    if selection_html:
        liste = {}
        for element in selection_html:
            attribut = element.find('th').get_text()
            valeur = element.find('td').get_text()
            liste[attribut] = valeur
    # print(f"Liste = {liste}")

# Extraction de la description du livre
    selection_html = soup.select('#content_inner > article > p')
    valeur = []
    if selection_html:
        for element in selection_html:
            description = element.get_text()
            product_description = repr(description)
            # product_description = description
    else:
        product_description = ['Pas de donnees']

# Extraction de la category
    selection_html = soup.select("#default > div > div > ul > li:nth-child(3) > a")
    if selection_html:
        for element in selection_html:
            category = element.get_text()
    else:
        category = 'Pas de donnee'
    # print(f"categorie : {category}")

    # Extraction de l'image du livre
    selection_html = soup.select('#content_inner > article > ul > li:nth-child(1) > article > div.image_container > a > img')
    # print(f"Selection : {selection_html}")
    if selection_html:
        for element in selection_html:
            try:
                (element['src'])
                url_image = element['src']
            except:
                url_image = 'Pas de donnees'
    else:
        url_image = 'Pas de donnees'
    # print(f"URL image : {url_image}")

    # Alimentation des données de sortie
    donnees["title"] = title
    donnees["category"] = category
    donnees.update(liste)
    donnees["url_image"] = url_image
    donnees["product_description"] = product_description

    return donnees

"""
"""
def extraction_liste_url_category(url):
 
    """
        # Cette fonction retourne une liste ('liste_url_categories')
        # de la liste des urls de catégories
"""

import requests 
import re

from bs4 import BeautifulSoup

TIMEOUT_REQUEST = 15

url = 'https://books.toscrape.com'

page_html = requests.get(url, timeout=TIMEOUT_REQUEST)

soup = BeautifulSoup(page_html.content, 'html.parser')

selection_html = soup.select('#default > div > div > div > aside > div.side_categories > ul > li > ul')
if selection_html:
    liste_url_category = []
    for element in selection_html:
        element_attribut = element.find_all('a')
        print(f"Element_Attribut : {element_attribut}")
        for element in element_attribut:
            el = url + '/' + element.get('href')
            print(f"url_categorie = {el}")
            liste_url_category.append(el)
else:
    liste_url_category = []
            # el = element_valeur.get('href')
        # print(f"Liste_url_categories = {liste_url_categories}")
        # url_complete = element.get('href')
        # category = re.sub(r'\s', "", element.get_text())
        # liste_url_par_page_category.update({url_complete: category})
# print(f"Liste des url_categories : {liste_url_category}")

# return liste_url_categories
"""

"""
def : url_book_par_category(url_category):

import requests 
import re

from bs4 import BeautifulSoup

TIMEOUT_REQUEST = 15
# url = 'https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'
    
liste_livre_category = []

while url :
    page_html = requests.get(url, timeout=TIMEOUT_REQUEST)
    soup = BeautifulSoup(page_html.content, 'html.parser')
    selection_html_courante = soup.select('#default > div > div > div > div > section > div:nth-child(2) > ol > li > article.product_pod > h3')
   # print(f"Selection_html_courante : {selection_html_courante}")
    if selection_html_courante:
        for element in selection_html_courante:
            url_book = element.find('a').get('href')
            url_book = url_book.replace('../', '')
            url_book = "https://books.toscrape.com/catalogue/" + url_book
            liste_livre_category.append(url_book)
        # print(f"Liste_livres_par_categorie : {liste_livre_category}")

    # Vérification de page suivante et création du lien vers cette page

    selection_html_suivante = soup.select('#default > div > div > div > div > section > div:nth-child(2) > div > ul > li.next')
    if selection_html_suivante:
        # print(f"Selection_url_suivante : {selection_html_suivante}")
        for item in selection_html_suivante:
            element = item.find('a').get('href')
        # print(f"liste des livres : {selection_html}")
            url = url.replace(url.split('/')[-1], element)
        # print(f"url suivante : {url}")
    else:
        url = ''
# print(f"Liste_url_par categorie : {liste_livre_category}")      
# return liste_livre_category


"""
# def transformation_donnees_brutes(donnees_brutes):
    
    # Transformation des données récupérées 
from datetime import date, time, datetime
import re

donnees_brutes = {'title': "Sophie's World", 'category': 'Philosophy', 'UPC': 'bd261725b99f5983', 'Product Type': 'Books', 'Price (excl. tax)': '£58.11', 'Price (incl. tax)': '£58.11', 'Tax': '£0.00', 'Availability': 'In stock (16 available)', 'Number of reviews': '0', 'url_image': '../../media/cache/65/71/6571919836ec51ed54f0050c31d8a0cd.jpg', 'product_description': '"Do you believe human life is inherently valuable? Unfortunately, in the secularized age of state-sanctioned euthanasia and abortion-on-demand, many are losing faith in the simple value of human life. To the disillusioned, human beings are a cosmic accident whose intrinsic value is worth no more than other animals.The Death of Humanity explores our culture\'s declining respe Do you believe human life is inherently valuable? Unfortunately, in the secularized age of state-sanctioned euthanasia and abortion-on-demand, many are losing faith in the simple value of human life. To the disillusioned, human beings are a cosmic accident whose intrinsic value is worth no more than other animals.The Death of Humanity explores our culture\'s declining respect for the sanctity of human life, drawing on philosophy and history to reveal the dark road ahead for society if we lose our faith in human life. ...more"'}

    # print(f"donnees_extraites : \n \n {donnees_brutes}")

    # E.Transformation.L : traitement de mise en forme des données extraites : suppression des champs Tax, Availability et Product type. Mise en format numérique des prix, isolation de la valeur du nombre de reviews, repise en ordre des données en correspondance aux attendus.

price_inc = donnees_brutes.get('Price (incl. tax)')
#print(f"prix incl : {price_inc}")
price_includ = str(price_inc).replace("£", "")
price_include_tax = price_includ
price_exc = donnees_brutes.get('Price (excl. tax)')
price_exclud = str(price_exc).replace("£", '')
price_exclude_tax = price_exclud
#print(f"Taxe Exclud : {price_exclude_tax}")
availability = donnees_brutes.get('Availability')
#print(f"Availability : {availability}")
available = (re.sub(r'\D', "", availability))
nbre_review = donnees_brutes.get('Number of reviews')
number_of_reviews = nbre_review
img_url = donnees_brutes.get('image_url')
valeur = str(img_url).replace("../", "")
# image_url = URL_BASE + '/' + str(valeur)
image_url = str(valeur)

donnees_purgees = {}
print(f"Boucle donnees brutes / purges: {donnees_purgees} / {donnees_purgees}")
# donnees_purgees['product_page_url'] = 'A ajouter'
donnees_purgees['universal_product_code (upc)'] = donnees_brutes.get('UPC')
donnees_purgees['title'] = donnees_brutes.get('title')
donnees_purgees['price_including_tax'] = price_include_tax
donnees_purgees['price_excluding_tax'] = price_exclude_tax
donnees_purgees['number_available'] = available
donnees_purgees['product_description'] = donnees_brutes.get('product_description')
donnees_purgees['category'] = donnees_brutes.get('category')
donnees_purgees['review_rating'] = number_of_reviews 
donnees_purgees['image_url'] = image_url
"""
return donnees_purgees


"""

# ************** Fin de la définition des fonctions ****************



""" Programme principal

    Récupération de la liste des catégories


liste_category = []
entetes = ""

# Creaton du fichier cible
fichier = open("donnees.csv", "w")


liste_category = extraction_liste_url_category('https://books.toscrape.com')
print(f"Liste_url_categories : {liste_category}")
for element in liste_category:
    print(f"Element_liste_categorie : {element}")
    url_livres = url_book_par_categorie(element)
    print(f"Liste livres_category : {url_livres}")

# Transformation

    for url in url_livres:
        print(f"url unitaire : {url}")
        # Extraction des données par livre
        donnees_brutes = extraction_unitaire_donnees_livre(url)
        print(f"Donnees_brutes : {donnees_brutes}")
        # Transformation des données brutes par livre 
        donnees_purgees = transformation_donnees_brutes(donnees_brutes)
        print(f"Donnes_purgees : {donnees_purgees}")
        
        # Transformation pour la création de la ligne d'entêtes dans le csv.
        if entetes == '':
            for key in donnees_purgees:
                entetes = entetes + "\"" + str(key) + "\","
                # Chargement des entêtes vers le fichier .csv
                entetes_vers_csv = entetes[:-1] + '\n'
            fichier.write(entetes_vers_csv)
            
            # Transformation de chaque ligne de donnée afin de formater en .csv
            donnees = ''
            for value in donnees_purgees:
                donnees = donnees + "\"" + donnees_purgees[value] + "\","
            donnees_vers_csv = donnees[:-1] + '\n'
            
            # Load (Chgargement) des données par ligne vers le fichier .csv
        fichier.write(donnees_vers_csv)


# Fin des actions 

fichier.close()
"""

# print(f"Donnees_vers_csv : {entetes_vers_csv}")

# print(f"Donnees_vers_csv : {donnees_vers_csv}")

# Creation du fichier de données cible

# Ecriture des données dans le fichier : Entête + informations
