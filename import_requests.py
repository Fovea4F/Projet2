import requests

from bs4 import BeautifulSoup as bs

URL = "https://www.gov.uk/search/news-and-communications"

ITEM_DESCRIPTION_CLASS = "gem-c-document-list__item-description"
TIMEOUT = 15
TAG = 'p'

page = requests.get(URL, timeout=TIMEOUT)
soup = bs(page.content, 'html.parser')
descriptions = soup.find_all(TAG, class_=ITEM_DESCRIPTION_CLASS)
liste = soup.find_all("p", class_="gem-c-document-list__item-description")
for ligne in liste:
    texte = ligne.get_text()
    print(texte)
    print("\n")