from bs4 import BeautifulSoup
import requests
main_url = "https://fr.wikipedia.org/wiki/Hello_world"
req = requests.get(main_url)
soup = BeautifulSoup(req.text, "html.parser")

# Finding the main title tag.
title = soup.find('title')
print(title.get_text(separator='|'))
