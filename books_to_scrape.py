

import requests
import re
import os
from time import strftime

TIMEOUT_REQUEST = 15

# Phase EXTRACT du processus ETL
# Programme d'extraction des informations de la Bibliothèque Books_To_Scrape Il est organise en mode ETL.


def extraction_liste_url_category(url):

    """Cette fonction extrait l'ensemble des categories de livres sur le site.

        Entree
                - URL du site à analyser \n
        Sortie   List \n
                - Liste des URLs des categories de livres sur le site (list) \n
    """
    import requests
    from bs4 import BeautifulSoup

    TIMEOUT_REQUEST = 15
    liste_url_category = []
    page_html = requests.get(url, timeout=TIMEOUT_REQUEST)
    nombre_categories = 0

    soup = BeautifulSoup(page_html.content, 'html.parser')
    chaine = "#default > div > div > div > aside > div.side_categories > ul > li > ul"

    selection_html = soup.select(chaine)
    if selection_html:
        # liste_url_category = []
        for element in selection_html:
            element_attribut = element.find_all('a')
            for element in element_attribut:
                el = f'{url}/' + element.get('href')
                # el = url + '/' + element.get('href')
                liste_url_category.append(el)
    else:
        liste_url_category = []

    return (liste_url_category)


def extraction_url_book_par_category(url_category):

    """ Cette fonction definit une liste d'Urls
        pointant sur des description de livres de la même categorie, dont on souhaite extraire les donnees.

        En entree : url_category , variable indiquant l'url de la categorie
        En sortie : liste de l'URL de chacun des livres appartenant à la categorie
    """
    import requests
    from bs4 import BeautifulSoup

    TIMEOUT_REQUEST = 15
    liste_livre_category = []

    page_html = ''
    soup = ''
    selection_html_courante = ''
    selection_html_suivante = ''

    # url_category = 'https://books.toscrape.com/catalogue/category/books/fiction_10/index.html'

    while url_category:
        page_html = requests.get(url_category, timeout=TIMEOUT_REQUEST)
        soup = BeautifulSoup(page_html.content, 'html.parser')
        selection_html_courante = soup.select('#default > div > div > div > div > section > div:nth-child(2) > ol > li > article.product_pod > h3')
        selection_html_suivante = soup.select('#default > div > div > div > div > section > div:nth-child(2) > div > ul > li.next')
        if selection_html_suivante:
            url_tmp = url_category
            for item in selection_html_suivante:
                element = item.find('a').get('href')
            url_category = url_tmp.replace(url_tmp.split('/')[-1], element)
        else:
            url_category = ''

        if selection_html_courante:
            for element in selection_html_courante:
                url_book = element.find('a').get('href')
                url_book = url_book.replace('../', '')
                url_book = f"https://books.toscrape.com/catalogue/{url_book}"
                # url_book = "https://books.toscrape.com/catalogue/" + url_book
                liste_livre_category.append(url_book)

        # Vérification de page suivante et creation du lien vers cette page

        selection_html_suivante = soup.select('#default > div > div > div > div > section > div:nth-child(2) > div > ul > li.next')
        if selection_html_suivante:
            url_tmp = url_category
            for item in selection_html_suivante:
                element = item.find('a').get('href')
                url = url_category.replace(url_category.split('/')[-1], element)
            url_category = url
        else:
            url_category = ''

    return liste_livre_category


def extraction_donnees_du_livre(url):

    """        Phase EXTRACT du processus ETL :
        Récupère toutes les données brutes concernant le livre dont l'url est
        passée en paramètre.
        Entrée : (url) du livre à explorer
        Sortie : dictionnaire de données au format brut.
    """

    import re
    import requests
    from bs4 import BeautifulSoup

    TIMEOUT_REQUEST = 15

    donnees_brutes = {}
    page_html = ''
    soup = ''
    selection_html = ''
    title = 'nc'
    url_livre = 'nc'

    page_html = requests.get(url, timeout=TIMEOUT_REQUEST)

    soup = BeautifulSoup(page_html.content, 'html.parser')
    selection_html = soup.select('#content_inner > article > div.row > div.col-sm-6.product_main')
    if selection_html:
        for element in selection_html:
            title = element.find('h1').get_text()

    selection_html = soup.select('#content_inner > article > ul > li:nth-child(1) > article > h3')

    url_livre = url

    selection_html = soup.select("table tr")
    if selection_html:
        liste = {}
        for element in selection_html:
            attribut = element.find('th').get_text()
            valeur = element.find('td').get_text()
            liste[attribut] = valeur

    # Extraction de la description du livre
    selection_html = soup.select('#content_inner > article > p')
    if not selection_html:
        product_description = 'nc'
    else:
        for element in selection_html:
            description = element.get_text('p')
            product_description = description

    # Extraction de la category
    selection_html = soup.select("#default > div > div > ul > li:nth-child(3) > a")
    if selection_html:
        for element in selection_html:
            category = element.get_text()
    else:
        category = 'Pas de donnee'

    # Extraction de l'image du livre
    selection_html = soup.select('#product_gallery > div > div > div > img')
    if selection_html:
        for element in selection_html:
            try:
                url_tmp = element['src']
                url_tmp = url_tmp.replace('../', '')
                url_image = 'https://books.toscrape.com/' + url_tmp
            except:
                url_image = 'Pas de donnees'
    else:
        url_image = 'Pas de donnees'

# Alimentation des données de sortie
    donnees_brutes["title"] = title
    donnees_brutes["category"] = category
    donnees_brutes.update(liste)
    donnees_brutes["url_image"] = url_image
    donnees_brutes["product_description"] = product_description
    donnees_brutes['product_page_url'] = url_livre

    return donnees_brutes


def transformation_donnees_brutes(donnees_in):

    """        Phase TRANSFORM du processus ETL :
        Nettoyage des données récupéres afin de rendre leur format utilisable
        Entree : dictionnaire de données brutes issu de la fonction "extraction_donnees_du_livre(url)"
        Sortie : dictionnaire de données "donnees_purgees"
    """
    import re

    donnees_purgees = {}

    # (E).Transformation.(L) : traitement de mise en forme des données extraites : suppression des champs Tax, Availability et Product type. Mise en format numérique des prix, isolation de la valeur du nombre de reviews, repise en ordre des données en correspondance aux attendus.
    # Pour les 2 valeurs de type tarif, suppression de la "currency" et remplacement du point par la virgule

    if 'Price (incl. tax)' in donnees_in:
        price_inc = donnees_in.get('Price (incl. tax)')
        price_includ = str(price_inc).replace(".", ",")
        price_includ = str(price_includ).replace("£", "")
        price_include_tax = price_includ
    else:
        price_include_tax = None

    if 'Price (excl. tax)' in donnees_in:
        price_exc = donnees_in.get('Price (excl. tax)')
        price_exclud = str(price_exc).replace(".", ",")
        price_exclud = str(price_exclud).replace("£", '')
        price_exclude_tax = price_exclud
    else:
        price_exclude_tax = None

    if 'Availability' in donnees_in:
        availability = donnees_in.get('Availability')
        available = str(re.sub(r'\D', "", availability))
    else:
        available = None

    if 'Number of reviews' in donnees_in:
        nbre_review = donnees_in.get('Number of reviews')
        number_of_reviews = int(nbre_review)
    else:
        number_of_reviews = None

    if 'url_image' in donnees_in:
        img_url = donnees_in.get('url_image')
        valeur = str(img_url).replace("../", "")
        image_url = str(valeur)
    else:
        image_url = 'nc'

    if ('UPC' in donnees_in):
        upc = str(donnees_in.get('UPC'))
    else:
        upc = 'nc'

    if ('title' in donnees_in):
        title = str(donnees_in.get('title'))
    else:
        title = 'nc'

    if 'product_description' in donnees_in:
        description = donnees_in.get('product_description')
        description = re.sub("\"", "\"\"", description)
        product_description = str(description)
    else:
        product_description = 'nc'

    if 'category' in donnees_in:
        category = str(donnees_in.get('category'))
    else:
        category = 'nc'

    if 'product_page_url' in donnees_in:
        product_page_url = str(donnees_in.get('product_page_url'))
    else:
        product_page_url = 'nc'

    donnees_purgees = {}

    donnees_purgees['universal_product_code (upc)'] = upc
    donnees_purgees['title'] = title
    donnees_purgees['price_including_tax (£)'] = price_include_tax
    donnees_purgees['price_excluding_tax (£)'] = price_exclude_tax
    donnees_purgees['number_available'] = available
    donnees_purgees['category'] = category
    donnees_purgees['review_rating'] = number_of_reviews
    donnees_purgees['image_url'] = image_url
    donnees_purgees['product_page_url'] = product_page_url
    donnees_purgees['product_description'] = product_description

    return donnees_purgees


def racine_arborescence(nom_projet):

    """Creation du dossier racine des données aspirees"""

    import os

    os.makedirs(nom_projet, exist_ok=True)

    # return err

# ************** Fin de la definition des fonctions  ****************


# **************         Programme principal         ****************
#                      Phase LOAD du process ETL

liste_category = []
entetes = ""
nom_projet = 'Books_to_scrape'

# Creation des arborescences de fichiers :

depot_directory = racine_arborescence(nom_projet)

# Deplacement a la racine du projet
os.chdir(nom_projet)

liste_category = extraction_liste_url_category('https://books.toscrape.com')
print("----------------------------------------")
print(f"{len(liste_category)} categories recensees sur le site.")
print("----------------------------------------")

for category in liste_category:
    entetes = ''
    nom_categorie = str(category.split('/')[-2])
    print(f"Nom de la catégorie traitée : {nom_categorie} , {int(category.split('/')[-2][-1])-1} sur {len(liste_category)}")

    url_livres_par_category = extraction_url_book_par_category(category)
    for url1 in url_livres_par_category:
        # Extraction des données par livre
        donnees_brutes = extraction_donnees_du_livre(url1)
        # Transformation des données brutes par livre
        donnees_propres = transformation_donnees_brutes(donnees_brutes)

        # Transformation pour la création de la ligne d'entêtes dans le csv.
        if entetes == '':

            # generation du repertoire de depot et du nom du fichier de donnes depuis la categorie.
            nom_dossier = donnees_propres['category']
            if not os.path.exists(nom_dossier):
                os.makedirs(nom_dossier, exist_ok=True)
            os.chdir(nom_dossier)
            rep_work = os.getcwd()
            # Création du fichier .csv recevant les données associées au livre, dans le répertoire spécitique
            nom_fichier_csv = donnees_propres['category']
            timestamp = strftime("%Y%m%d_%H%M%S")
            nom_fichier_csv = f'{timestamp}-' + re.sub(' ', '_', nom_fichier_csv) + '.csv'
            # nom_fichier_csv = timestamp + '-' + re.sub(' ', '_', nom_fichier_csv) + '.csv'
            # Ecriture des données collectées pour le livre dans un fichier .csv dûement placé.

            # generation de le ligne d'entête
            for key in donnees_propres:
                entetes = entetes + '"' + str(key) + '"' + ','
                # Chargement des entêtes vers le fichier .csv
                entetes_vers_csv = entetes[:-1] + '\n'
            with open(nom_fichier_csv, "w", encoding="utf-8") as fichier_donnees:
                ecriture = fichier_donnees.write(entetes_vers_csv)

        # Transformation de chaque ligne de donnée afin de formater en .csv et "échaper les caractères identiques au séparateur virgule"
        donnees = str('')
        # donnees = ""
        for value in donnees_propres:
            # donnees = donnees + '"' + str(donnees_propres[value]) + '"' + ','
            donnees = f'{donnees}"{str(donnees_propres[value])}",'
        donnees_vers_csv = donnees[:-1] + '\n'

        # Load (Chgargement) des données par ligne vers le fichier .csv
        with open(nom_fichier_csv, "a", encoding="utf-8") as fichier_donnees:
            ecriture = fichier_donnees.write(donnees_vers_csv)

        # Création du fichier image recevant l'image associée au livre et déposée dans le dossier associé à ce livre. Formatage du nom de fichier sans les caratcères interdits
        title = re.sub(' ', '_', donnees_propres.get('title'))
        # Filtre sur les caractères ne devant pas participer au nom du fichier image
        chars = ["'", "?", "#", "~", ":", "%", "&", "*", "$", "*", "/", "()", ")", "=", "\"", ","]
        format_title = title.translate(str.maketrans('', '', ''.join(chars)))
        image_url = donnees_propres.get('image_url')
        sub_nom_fichier_image = re.split('/+', image_url)[-1]
        nom_fichier_image = f'{format_title}_{sub_nom_fichier_image}'
        # nom_fichier_image = format_title + '_' + sub_nom_fichier_image
        if not os.path.exists(nom_fichier_image):
            lecture_image = requests.get(image_url, stream=True, timeout=TIMEOUT_REQUEST)
            with open(nom_fichier_image, 'wb') as handle:
                for block in lecture_image.iter_content(1024):
                    handle.write(block)

    os.chdir('..')

# Fin des actions
