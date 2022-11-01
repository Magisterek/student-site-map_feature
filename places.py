from requests import get
from bs4 import BeautifulSoup
import re

url = "https://estarter.pl/"
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

food_category = [
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
    "herbata",
    "kawa/herbata"
]
alcohol_category = [
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

subcategory_food_kawa_herbata_slodkie = ["Kawiarnia","kawa","kawy","herbata","kawa/herbata","cafe","ciasto","ciastka","ciasta","pączek","pączki","czekolada","kołacz","kołacze","naleśniki","naleśnik"]
subcategory_food_pizza = ["pizza","pizzę","pizzy"]
subcategory_food_kebab_kebap = ["kebap","kebab"]
subcategory_food_burger = ["burger","burgery","burgera","burgers"]

subcategory_uslugi_kurierzy = ["glovo", "uber", "dostawa"]
subcategory_uslugi_kurs_y = ["kurs","kursy"]
subcategory_uslugi_tattoo = ["tattoo","piercing","tatuaż"]
subcategory_uslugi_silownia= ["citifit","siłownia"] #citifit


appended_jedzenie = []
appended_alkohol = []
appended_uslugi = []
appended_kurierzy = []

app_subcategory_food_kawa_herbata_slodkie = []
app_subcategory_food_pizza = []
app_subcategory_food_kebab_kebap = []
app_subcategory_food_burger = []

app_subcategory_uslugi_kurierzy = []
app_subcategory_uslugi_kurs_y = []
app_subcategory_uslugi_tattoo = []
app_subcategory_uslugi_silownia= [] #citifit

wszystkie_kategorie = [
    "appended_jedzenie",
    "appended_alkohol",
    "appended_uslugi",
    "appended_kurierzy",
]

for city, id in city_and_id.items():
    url = f"https://estarter.pl/pl/offer/index/id_category/{id}/category_name/{city}"
    soup = BeautifulSoup(get(url).content, "html.parser")
    place_option = soup.find_all("p", class_="card-text")
    coupon_option = soup.find_all("h4", class_="card-title")
    for x in range(len(place_option)):
        place = place_option[x].get_text().replace(",", "").lower()
        coupon = coupon_option[x].get_text().lower()
        word_is_not_founded = True
        coupon_title = place.split(" ")
        del coupon_title[-1]  # usuń city z konca tytułu
        offer_description = coupon.split(" ")
        if word_is_not_founded:
            for word in coupon_title:  # frytki
                #JEDZENIE
                if word in food_category:  # jedzenie w tytule
                    word_is_not_founded = False
                    # subcategory_is_not_founded = True
                    if word in subcategory_food_kawa_herbata_slodkie:
                        # subcategory_is_not_founded = False
                        app_subcategory_food_kawa_herbata_slodkie.append({place.title(): coupon.capitalize()})
                    elif word in subcategory_food_pizza:  
                        # subcategory_is_not_founded = False
                        app_subcategory_food_pizza.append({place.title(): coupon.capitalize()})
                    elif word in subcategory_food_kebab_kebap:  
                        # subcategory_is_not_founded = False
                        app_subcategory_food_kebab_kebap.append({place.title(): coupon.capitalize()})
                    elif word in subcategory_food_burger:  
                        # subcategory_is_not_founded = False
                        app_subcategory_food_burger.append({place.title(): coupon.capitalize()})
                    #dodaj do ogólnego jak nie ma podkategorii          
                    appended_jedzenie.append({place.title(): coupon.capitalize()})
                #ALKHOL
                elif word in alcohol_category:  # alkohol w tytule
                    word_is_not_founded = False
                    appended_alkohol.append({place.title(): coupon.capitalize()})
        if word_is_not_founded:
            for word in offer_description:
                if word in food_category:  # jedzenie w tytule
                    word_is_not_founded = False
                    # subcategory_is_not_founded = True
                    if word in subcategory_food_kawa_herbata_slodkie:
                        # subcategory_is_not_founded = False
                        app_subcategory_food_kawa_herbata_slodkie.append({place.title(): coupon.capitalize()})
                    elif word in subcategory_food_pizza:  
                        # subcategory_is_not_founded = False
                        app_subcategory_food_pizza.append({place.title(): coupon.capitalize()})
                    elif word in subcategory_food_kebab_kebap:  
                        # subcategory_is_not_founded = False
                        app_subcategory_food_kebab_kebap.append({place.title(): coupon.capitalize()})
                    elif word in subcategory_food_burger:  
                        # subcategory_is_not_founded = False
                        app_subcategory_food_burger.append({place.title(): coupon.capitalize()})
                    #dodaj do ogólnego jak nie ma podkategorii          
                    else:
                        appended_jedzenie.append({place.title(): coupon.capitalize()})

                elif word in alcohol_category:  # alohol w opisie
                    word_is_not_founded = False
                    appended_alkohol.append({place.title(): coupon.capitalize()})
        if word_is_not_founded:  # usługi
            if word in subcategory_uslugi_kurierzy:
                        # subcategory_is_not_founded = False
                        app_subcategory_uslugi_kurierzy.append({place.title(): coupon.capitalize()})
            elif word in subcategory_uslugi_kurs_y:  
                # subcategory_is_not_founded = False
                app_subcategory_uslugi_kurs_y.append({place.title(): coupon.capitalize()})
            elif word in subcategory_uslugi_tattoo:  
                # subcategory_is_not_founded = False
                app_subcategory_uslugi_tattoo.append({place.title(): coupon.capitalize()})
            elif word in subcategory_uslugi_silownia:  
                # subcategory_is_not_founded = False
                app_subcategory_uslugi_silownia.append({place.title(): coupon.capitalize()})
            #dodaj do ogólnego jak nie ma podkategorii          
            else:
                appended_uslugi.append({place.title(): coupon})






        #     # word_is_not_founded = False | nie trzeba sprawdzać
        #     appended_uslugi.append({place: coupon})
# podkategorie jedzenia 
    # subcategory_food_kawa_herbata_slodkie = []
    # subcategory_food_pizza = []
    # subcategory_food_kebab_kebap = []
    # subcategory_food_burger = []

    # subcategory_uslugi_kurierzy = []
    # subcategory_uslugi_kurs_y = []
    # subcategory_uslugi_tattoo = []
    # subcategory_uslugi_silownia= [] #citifit
# for x in range(len(appended_jedzenie)):
#     print(appended_jedzenie[x])


        # print(coupon)
        # print(place_option[x].get_text().replace(",", ""), end=",")
        # print(coupon[x].get_text().capitalize())
#generuj pliki 
header = "miejsce, kupon\n"
# Podstawowe katrgorie 
with open("alkohol.csv", "w", encoding="utf-8") as f:
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

with open("kawa_herbata.csv", "w", encoding="utf-8") as f:
    f.write(header)
    for place_coupon in app_subcategory_food_kawa_herbata_slodkie:
        for k, v in place_coupon.items():
            f.write(f"{k},{v}\n")

with open("pizza.csv", "w", encoding="utf-8") as f:
    f.write(header)
    for place_coupon in app_subcategory_food_pizza:
        for k, v in place_coupon.items():
            f.write(f"{k},{v}\n")

with open("kebab.csv", "w", encoding="utf-8") as f:
    f.write(header)
    for place_coupon in app_subcategory_food_kebab_kebap:
        for k, v in place_coupon.items():
            f.write(f"{k},{v}\n")

with open("burger.csv", "w", encoding="utf-8") as f:
    f.write(header)
    for place_coupon in app_subcategory_food_burger:
        for k, v in place_coupon.items():
            f.write(f"{k},{v}\n")

with open("kurierzy.csv", "w", encoding="utf-8") as f:
    f.write(header)
    for place_coupon in app_subcategory_uslugi_kurierzy:
        for k, v in place_coupon.items():
            f.write(f"{k},{v}\n")

with open("kursy.csv", "w", encoding="utf-8") as f:
    f.write(header)
    for place_coupon in app_subcategory_uslugi_kurs_y:
        for k, v in place_coupon.items():
            f.write(f"{k},{v}\n")

with open("tattoo.csv", "w", encoding="utf-8") as f:
    f.write(header)
    for place_coupon in app_subcategory_uslugi_tattoo:
        for k, v in place_coupon.items():
            f.write(f"{k},{v}\n")

with open("silownia.csv", "w", encoding="utf-8") as f:
    f.write(header)
    for place_coupon in app_subcategory_uslugi_silownia:
        for k, v in place_coupon.items():
            f.write(f"{k},{v}\n")

# for kategoria in wszystkie_kategorie:s
# for place_coupon in appended_alkohol:
#     for k,v in place_coupon.items():
#         print(k,v)
