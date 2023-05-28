""" Programme d'extraction des informations de la Bibliothèque "Books_To_Scrape"
    Il est organisé en mode ETL.
    entrée : (Url) du site ciblé ar les extractions de donnéeset images
    Résultat : Arborescence de dossiers regroupant les fichiers .cvs horodatés ainsi que les images des livres concernés
"""

import re
import requests
import os

from time import strftime, gmtime
from bs4 import BeautifulSoup


def extraction_liste_url_category(url):
        
    """     Cette fonction retourne une liste ('liste_url_category')
            de la liste des urls des catégories
    """

    import re
    import requests 
    from bs4 import BeautifulSoup

    TIMEOUT_REQUEST = 15
    liste_url_category = []
    page_html = requests.get(url, timeout=TIMEOUT_REQUEST)

    soup = BeautifulSoup(page_html.content, 'html.parser')

    selection_html = soup.select('#default > div > div > div > aside > div.side_categories > ul > li > ul')
    if selection_html:
        liste_url_category = []
        for element in selection_html:
            element_attribut = element.find_all('a')
            # print(f"Element_Attribut : {element_attribut}")
            for element in element_attribut:
                el = url + '/' + element.get('href')
                # print(f"url_categorie = {el}")
                liste_url_category.append(el)
    else:
        liste_url_category = []
    
    return liste_url_category


def url_book_par_category(url_category):


    """ Cette fonction définit une liste d'Urls
        pointant sur des description de livres de la même catégorie, dont on souhaite extraire les données.

        En entrée : url_category : variable indiquant l'url de la catégorie
    """
    import requests 
    import re
    from bs4 import BeautifulSoup

    TIMEOUT_REQUEST = 15
    liste_livre_category = []
    
    page_html = ''
    soup = ''
    selection_html_courante = ''

    # url_category = 'https://books.toscrape.com/catalogue/category/books/fiction_10/index.html'

    while url_category :
        page_html = requests.get(url_category, timeout=TIMEOUT_REQUEST)
        soup = BeautifulSoup(page_html.content, 'html.parser')
        selection_html_courante = soup.select('#default > div > div > div > div > section > div:nth-child(2) > ol > li > article.product_pod > h3')
        # selection_html_courante = soup.find_all('default > div > div > div > div > section > div:nth-child(2) > ol > li:nth-child(2) > article')
        # print(f"selection_html_courante : {selection_html_courante}")
        selection_html_suivante = soup.select('#default > div > div > div > div > section > div:nth-child(2) > div > ul > li.next')
        # print(f"selection_html_suivante : {selection_html_suivante}")
        if selection_html_suivante:
            url_tmp = url_category
            # print(f"Selection_url_suivante : {selection_html_suivante}")
            for item in selection_html_suivante:
                element = item.find('a').get('href')
            # print(f"liste des livres : {selection_html}")
            url_category = url_tmp.replace(url_tmp.split('/')[-1], element)
            # print(f"url suivante : {url_category}")
        else:
            url_category = ''

    # print(f"Selection_html_courante : {selection_html_courante}")
        if selection_html_courante:
            for element in selection_html_courante:
                url_book = element.find('a').get('href')
                url_book = url_book.replace('../', '')
                url_book = "https://books.toscrape.com/catalogue/" + url_book
                liste_livre_category.append(url_book)
            # print(f"Liste_livres_par_categorie : {liste_livre_category}")
            # print("---------------------------------")

        # Vérification de page suivante et création du lien vers cette page

        selection_html_suivante = soup.select('#default > div > div > div > div > section > div:nth-child(2) > div > ul > li.next')
        if selection_html_suivante:
            url_tmp = url_category
            # print(f"url_tmp : {url_tmp}")
            # print(f"Selection_url_suivante : {selection_html_suivante}")
            for item in selection_html_suivante:
                element = item.find('a').get('href')
            # print(f"liste des livres : {selection_html}")
                url = url_category.replace(url_category.split('/')[-1], element)
            url_category = url
            # print(f"url suivante : {url_tmp}")
        else:
            url_category = ''

    return liste_livre_category
    # print(f"liste_livres de la catégorie : {liste_livre_category}")


def extraction_donnees_du_livre(url):


    """
        Partie Extraction de (ETL) :
        Récupère toutes les données brutes concernant le livre dont l'url est 
        passée en paramètre.
        Entrée : (url) du livre à explorer
        Sortie : dictionnaire de données au format brut : 
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
    valeur = []
    try:
        # selection_html = soup.select('head > meta:nth-child(4)')
        selection_html = soup.select('#content_inner > article > p')
        for element in selection_html:
            description = element.get_text('p')
            # description =re.sub('\n', '', element.get('content'))
            # description =re.sub('\n', '', element.get('content'))
            product_description = description
    except:
        product_description = ['Pas de donnees']
        # print(f"selection_html : {selection_html}")

    # Extraction de la category
    selection_html = soup.select("#default > div > div > ul > li:nth-child(3) > a")
    if selection_html:
        for element in selection_html:
            category = element.get_text()
    else:
        category = 'Pas de donnee'
    # print(f"categorie : {category}")

    # Extraction de l'image du livre
    #product_gallery > div > div > div
    selection_html = soup.select('#product_gallery > div > div > div > img')
    # print(f"Selection : {selection_html}")
    if selection_html:
        for element in selection_html:
            try:
                url_tmp = element['src']
                url_tmp =  url_tmp.replace('../', '')
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

    print(f" Donnees brutes : {donnees_brutes}")
    return donnees_brutes


def transformation_donnees_brutes(donnees_in):
    
    """
        Partie Transformation de (ETL) :
        Nettoyage des données récupéres afin de rendre leur format utilisable
        Entree : dictionnaire de données brutes issu de la fonction "extraction_donnees_du_livre(url)"
        Sortie : dictionnaire de données "donnees_purgees"
    """
    import re

    donnees_purgees = {}
    
        # print(f"donnees_extraites : \n \n {donnees_brutes}")

        # (E).Transformation.(L) : traitement de mise en forme des données extraites : suppression des champs Tax, Availability et Product type. Mise en format numérique des prix, isolation de la valeur du nombre de reviews, repise en ordre des données en correspondance aux attendus.

    if 'Price (incl. tax)' in donnees_in:
        price_inc = donnees_in.get('Price (incl. tax)')
        price_includ = str(price_inc).replace("£", "")
        price_include_tax = float(price_includ)
    else:
        price_include_tax = None

    if 'Price (excl. tax)' in donnees_in:
        price_exc = donnees_in.get('Price (excl. tax)')
        price_exclud = str(price_exc).replace("£", '')
        price_exclude_tax = float(price_exclud)
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
        # description = re.sub(",", "\",\"", description)
        description = re.sub("\"", "\"\"", description)
        # description = str(donnees_in.get('product_description'))
        product_description = str(description)
    else :
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
    donnees_purgees['price_including_tax'] = price_include_tax
    donnees_purgees['price_excluding_tax'] = price_exclude_tax
    donnees_purgees['number_available'] = available
    donnees_purgees['category'] = category
    donnees_purgees['review_rating'] = number_of_reviews 
    donnees_purgees['image_url'] = image_url
    donnees_purgees['product_page_url'] = product_page_url
    donnees_purgees['product_description'] = product_description


    return donnees_purgees


def racine_arborescence(nom_projet):
    
    """ Création du donnier racine des données aspirées
    """

    import os
    

    os.makedirs(nom_projet, exist_ok=True)

    return None

# ************** Fin de la définition des fonctions ****************


"""
    Programme principal

    Récupération de la liste des catégories
"""
liste_category = []
entetes = ""
nom_projet = 'Books_to_scrape'

# Creation des arborescences de fichiers :

depot_directory = racine_arborescence(nom_projet)

# Deplacement a la racine du projet
os.chdir(nom_projet)
# print(f"Répertoire racine : {os.getcwd()}")
# Creaton du fichier cible
# with open("donnees.csv", "w") as fichier_donnees:
#    pass

liste_category = extraction_liste_url_category('https://books.toscrape.com')
# print(f"liste des catégories : {liste_category}")
# print(f"Liste_url_categories : {liste_category}")
for category in liste_category:
    entetes = ''
    # print(f"Element passé à url_book_par_category : {element}")
    url_livres_par_category = url_book_par_category(category)
    # print(f"Appel url_book_par_category avec : {url_livres_par_category}")

    for url1 in url_livres_par_category:
        # print(f"url unitaire : {url1}")
        # print(f"------------------------------------------")
        # Extraction des données par livre
        donnees_brutes = extraction_donnees_du_livre(url1)
        # print(f"Appel estraction_donnees_brutes avec : {donnees_brutes}")
        # print(f"------------------------------------------")
        # Transformation des données brutes par livre 
        donnees_propres = transformation_donnees_brutes(donnees_brutes)
        # print(f"Donnees_purgees : {donnees_propres}")
        # print(f"------------------------------------------")
        # print(f"Appel transformation_donnees_brutes avec : {donnees_propres}")
        
        # Transformation pour la création de la ligne d'entêtes dans le csv.
        if entetes == '':
            
            # generation du repertoire de depot et du nom du fichier de donnes depuis la categorie.
            nom_dossier = donnees_propres['category']
            # rep_work = os.getcwd()
            # print(f"Rep travail  : {rep_work}")
            if not os.path.exists(nom_dossier):
                os.makedirs(nom_dossier, exist_ok=True)
            os.chdir(nom_dossier)
            rep_work = os.getcwd()
            # print(f"New Rep travail  : {rep_work}")
            # Création du fichier .csv recevant les données associées au livre, dans le répertoire spécitique
            nom_fichier_csv = donnees_propres['category']
            timestamp = strftime("%Y%m%d_%H%M%S")
            nom_fichier_csv = timestamp + '-' + re.sub(' ', '_', nom_fichier_csv) + '.csv'
            # print(f"nom fichier : {nom_fichier}")
            # print(f"------------------------------------------")
            # Ecriture des données collectées pour le livre dans un fichier .csv dûement placé.
            # print(f"nom fichier : {nom_fichier_csv}")
            # print(f"------------------------------------------")
            # with open(nom_fichier_csv, "w") as fichier_donnees:
            #    ecriture = fichier_donnees.write(entetes_vers_csv)
            
            # generation de le ligne d'entête
            for key in donnees_propres:
                entetes = entetes + '"' + str(key) + '"' + ','
                # entetes = entetes + "\"" + str(key) + "\","
                # Chargement des entêtes vers le fichier .csv
                entetes_vers_csv = entetes[:-1] + '\n'  
            with open(nom_fichier_csv, "w", encoding="utf-8") as fichier_donnees:
                ecriture = fichier_donnees.write(entetes_vers_csv)
            
        # Transformation de chaque ligne de donnée afin de formater en .csv et "échaper les caractères identiques au séparateur virgule"
        donnees = ''
        for value in donnees_propres:
            donnees = donnees + '"' + str(donnees_propres[value]) + '"' + ','
        donnees_vers_csv = donnees[:-1] + '\n'
        
        # Load (Chgargement) des données par ligne vers le fichier .csv
        with open(nom_fichier_csv, "a", encoding="utf-8") as fichier_donnees:
            ecriture = fichier_donnees.write(donnees_vers_csv)
        
        # Création du fichier image recevant l'image associée au livre et déposée dans le dossier associé à ce livre. Formatage du nom de fichier sans les caratcères interdits
        title = re.sub(' ', '_', donnees_propres.get('title'))
        # Filtre sur les caractères ne devant pas participer au nom du fichier image
        chars = ["'", "?", "#", "~", ":", "%", "&", "*", "$", "\*", "/", "()",  ")", "=", "\"", ","]
        format_title = title.translate(str.maketrans('', '', ''.join(chars)))
        image_url = donnees_propres.get('image_url')
        sub_nom_fichier_image = re.split('/+', image_url)[-1]
        nom_fichier_image = format_title + '_' + sub_nom_fichier_image
        if not os.path.exists(nom_fichier_image):
            lecture_image = requests.get(image_url, stream=True)
            with open(nom_fichier_image, 'wb') as handle:
                for blk in lecture_image.iter_content(1024):
                    handle.write(blk)

    os.chdir('..')

# Fin des actions
 
