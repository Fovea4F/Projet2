import requests

from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"

TIMEOUT_REQUEST = 15

page_html = requests.get(URL, timeout=TIMEOUT_REQUEST)

soup = BeautifulSoup(page_html.content, 'html.parser')

# le lien partiel de chaque livre est inclu dans une suite de balises
# <article class="product_pod"><h"> 20 articles par page
# Création d'une liste de liens complets pour accéder à l'URL de chaque
#  livre sur 1 page.

selection_article = soup.select("article.product_pod h3")

liste_liens_par_page = []
for element in selection_article:
    lien = element.find("a")
    link = lien["href"]
    liste_liens_par_page.append(URL + link)
print(liste_liens_par_page)
