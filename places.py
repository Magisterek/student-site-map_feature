from requests import get
from bs4 import BeautifulSoup
import re
# wszystkie miasta wraz z ich kodem do zmiany url 
url ="https://estarter.pl/"
strona = get(url)
soup = BeautifulSoup(strona.content, "html.parser")
miasta = soup.find_all("option")
# print(miasta) # <optionvalue="/pl/offer/index/id_category/403467/category_name/bialystok">Białystok</option>
miasto_kod = {}
for opcja in miasta:
    kod = str(re.findall(r'\d{6}', str(opcja)))
    miasto = str(re.findall(r'^category_name(/*)"$', str(opcja)))
    miasto_kod.update({kod:miasto})
print(miasto_kod)
    # miasto_kod.update({"kod[0]":""})
# print(miasto_kod)
# kod_miasto = {"Poznań" :"403417"}

# url = "https://estarter.pl/pl/offer/index/id_category/403417/category_name/poznan"
# strona = get(url)
# soup = BeautifulSoup(strona.content, "html.parser")
# miejsce = soup.find_all("p", class_="card-text")
# kupon = soup.find_all("h4", class_="card-title")
# header = "miejsce, kupon"
# print(header)
# for x in range(len(miejsce)):
#     print(miejsce[x].get_text().replace(",", ""), end = ",")
#     print(kupon[x].get_text().capitalize()