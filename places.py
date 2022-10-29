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
    "burgers",
    "sniadanie",
    "czekolada",
    "kebab",
    "cafe",
    "Ciasto",
    "ciastko",
    "ciasta",
    "bistro",
    "kołacza",
    "kołacz",
    "pączek",
    "naleśniki"
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
    "kieliszek",
    "bacardi",
]
kategoria_dostawa_jedzenia = ["glovo", "uber", "dostawa"]
tablica_slownikow = []


appended_jedzenie = []
appended_alkohol = []
appended_uslugi = []
appended_kurier = []

header = "miejsce, kupon"
print(header)
for miasto, kod in miasto_kod.items():
    url = f"https://estarter.pl/pl/offer/index/id_category/{kod}/category_name/{miasto}"
    strona = get(url)
    soup = BeautifulSoup(strona.content, "html.parser")
    miejsce = soup.find_all("p", class_="card-text")
    kupon = soup.find_all("h4", class_="card-title")
    for x in range(len(miejsce)):
        place = miejsce[x].get_text().replace(",", "").lower()
        rabat = kupon[x].get_text().lower()
        is_already_founded = False
        tytul_oferty = place.split(" ")
        del tytul_oferty[-1]  # usuń miasto z konca tytułu
        opis_oferty = rabat.split(" ")
        if is_already_founded == False:
            for word in tytul_oferty:  # frytki
                if word in kategoria_jedzenie:  # jedzenie w tytule
                    is_already_founded = True
                    appended_jedzenie.append({place.title(): rabat.capitalize()})
                elif word in kategoria_alkohol:  # alkohol w tytule
                    is_already_founded = True
                    appended_alkohol.append({place.title(): rabat.capitalize()})
        if is_already_founded == False:
            for word in opis_oferty:
                if word in kategoria_jedzenie:  # jedzenie w opisie
                    is_already_founded = True
                    appended_jedzenie.append({place.title(): rabat.capitalize()})
                elif word in kategoria_alkohol:  # alohol w opisie
                    is_already_founded = True
                    appended_alkohol.append({place.title(): rabat.capitalize()})
        if is_already_founded == False:  # usługi
            is_already_founded = True
            appended_uslugi.append({place: rabat})

        # print(rabat)
        # print(miejsce[x].get_text().replace(",", ""), end=",")
        # print(kupon[x].get_text().capitalize())
print(appended_jedzenie)
print("######################################################################")
print(appended_alkohol)
print("######################################################################")
print(appended_uslugi)
