from requests import get
from bs4 import BeautifulSoup
import re

####################################################################################
# wszystkie miasta wraz z ich kodem do zmiany url
url = "https://estarter.pl/"
strona = get(url)
soup = BeautifulSoup(strona.content, "html.parser")
miasta = soup.find_all("option")
# print(miasta) # <optionvalue="/pl/offer/index/id_category/403467/category_name/bialystok">Białystok</option>
miasto_kod = {}

# pattern na kod
kod_pattern = r"\d{6}"
# pattern na miasto
miasto_pattern = r"^\w+"

####################################################################################
for opcja in miasta:
    # del <option value="/pl/offer/index/id_category/403467/category_name/ zawsze stała wartość, stąd opcja[64:]
    kod = re.findall(kod_pattern, str(opcja))
    miasto = re.findall(miasto_pattern, str(opcja)[64:])
    # print(kod, miasto)
    if (
        miasto and kod
    ):  # celem tego jest pozbycie sie pustych tablic (pierwszy wiersz i wiersz w połowie)
        miasto_kod.update({miasto[0]: kod[0]})
# print(miasto_kod)

####################################################################################
# miasto_kod = {"Poznań" :"403417"}
kategoria_jedzenie = [
    "frytki",
    "lemoniada",
    "kawa",
    "kawy",
    "pizza",
    "pizzę",
    "burger",
    "burgery",
    "burgera",
    "sniadanie",
    "czekolada",
    "kebab",
    "cafe",
    "ciastko",
    "ciasta",
]
kategoria_alkohol = [
    "koktajl",
    "koktajle",
    "alkohol",
    "piwo",
    "piwa",
    "karafka",
    "shot",
    "shoty",
    "wódka",
    "wódki",
]

kategoria_dostawa_jedzenia = ["glovo", "uber"]
tablica_slownikow = []


appended_jedzenie = []

header = "miejsce, kupon"
print(header)
for miasto, kod in miasto_kod.items():
    url = f"https://estarter.pl/pl/offer/index/id_category/{kod}/category_name/{miasto}"
    strona = get(url)
    soup = BeautifulSoup(strona.content, "html.parser")
    miejsce = soup.find_all("p", class_="card-text")
    kupon = soup.find_all("h4", class_="card-title")
    for x in range(len(miejsce)):
        place = miejsce[x].get_text().replace(",", "")
        rabat = kupon[x].get_text().capitalize()
        czy_znalazlo = False
        print(place)
        for word in place: # word okazało sie charem
            # print(word)
            word = str(word)[24:]
            print(word)

            if (czy_znalazlo == False) and (word in kategoria_jedzenie):
                czy_znalazlo = True
                # appended_jedzenie.append({str(place): str(rabat)})
        for word in kupon:
            word = str(word)[24:]
            if (czy_znalazlo == False) and (word in kategoria_jedzenie):
                czy_znalazlo = True
                # appended_jedzenie.append({str(place): str(rabat)})

        # print(rabat)
        # print(miejsce[x].get_text().replace(",", ""), end=",")
        # print(kupon[x].get_text().capitalize())
print(appended_jedzenie)
print("end")
