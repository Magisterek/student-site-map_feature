from requests import get
from bs4 import BeautifulSoup
import re

url = "https://estarter.pl/"
# page = get(url)
soup = BeautifulSoup(get(url).content, "html.parser")
cities = soup.find_all("option")
# print(cities) == <optionvalue="/pl/offer/index/id_category/403467/category_name/bialystok">Białystok</option>

city_and_id = {}

city_and_id_pattern = r"\d{6}"

city_pattern = r"^\w+"

for city_option in cities:
    # del <option value="/pl/offer/index/id_category/403467/category_name/ zawsze stała wartość, stąd city[64:]
    id = re.findall(city_and_id_pattern, str(city_option))
    city = re.findall(city_pattern, str(city_option)[64:])
    # check for emptiness 
    if city: # and id
        city_and_id.update({city[0]: id[0]})

kategoria_jedzenie = [
    "frytki",
    "frytek",
    "gołe",
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
    "naleśniki",
    "herbata"
]
kategoria_alkohol = [
    "koktajl",
    "koktajle",
    "alkohol",
    "piwo",
    "piwa",
    "karafka",
    "shot",
    "shotów"
    "shoty",
    "wódka",
    "wódki",
    "kieliszek",
    "bacardi",
    "drink",
    "kamikaze"
]
kategoria_kurierzy = [
    "uber",
    "glovo"
]
kategoria_dostawa_jedzenia = ["glovo", "uber", "dostawa"]

appended_jedzenie = []
appended_alkohol = []
appended_uslugi = []
appended_kurierzy = []

wszystkie_kategorie = [
    "appended_jedzenie",
    "appended_alkohol",
    "appended_uslugi",
    "appended_kurierzy",
]

for city, id in city_and_id.items():
    url = f"https://estarter.pl/pl/offer/index/id_category/{id}/category_name/{city}"
    # page = get(url)
    soup = BeautifulSoup(get(url).content, "html.parser")
    miejsce = soup.find_all("p", class_="card-text")
    coupon = soup.find_all("h4", class_="card-title")
    for x in range(len(miejsce)):
        place = miejsce[x].get_text().replace(",", "").lower()
        rabat = coupon[x].get_text().lower()
        is_already_founded = False
        coupon_title = place.split(" ")
        del coupon_title[-1]  # usuń city z konca tytułu
        opis_oferty = rabat.split(" ")
        if is_already_founded == False:
            for word in coupon_title:  # frytki
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
        # print(coupon[x].get_text().capitalize())
# print(appended_jedzenie)
# print("######################################################################")
# print(appended_alkohol)
# print("######################################################################")
# print(appended_uslugi)

#generuj pliki 
header = "miejsce, kupon\n"
with open("alohol.csv", "w", encoding="utf-8") as f:
    f.write(header)
    for place_coupon in appended_alkohol:
        for k, v in place_coupon.items():
            f.write(f"{k},{v}\n")
with open("jedzenie.csv", "w", encoding="utf-8") as f:
    f.write(header)
    for place_coupon in appended_jedzenie:
        for k, v in place_coupon.items():
            f.write(f"{k},{v}\n")
with open("uslugi.csv", "w", encoding="utf-8") as f:
    f.write(header)
    for place_coupon in appended_uslugi:
        for k, v in place_coupon.items():
            f.write(f"{k},{v}\n")

# for kategoria in wszystkie_kategorie:
# for place_coupon in appended_alkohol:
#     for k,v in place_coupon.items():
#         print(k,v)
