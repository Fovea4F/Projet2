import requests

from bs4 import BeautifulSoup
# Extraction du TITRE du livre

URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

TIMEOUT_REQUEST = 15

page_html = requests.get(URL, timeout=TIMEOUT_REQUEST)

soup = BeautifulSoup(page_html.content, 'html.parser')

selection_article = soup.select("div.product_main h1")
for element in selection_article:
    titre = element.text

informations = {}
informations['Titre'] = titre

# Extraction des donnees du livre : UPC, Price including tax,
# price excluding tax, nr available, reviex ratings

selection_article = soup.select("table.table-striped tr")
# print(selection_article)

for element in selection_article:
    el_type = element.find("th").get_text()
    if el_type != 'Product Type':
        el_valeur = element.find('td').get_text()
        informations[el_type] = el_valeur
print(informations)
