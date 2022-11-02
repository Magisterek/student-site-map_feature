from requests import get
from bs4 import BeautifulSoup
import re
import os

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
    if city:  # and id
        city_and_id.update({city[0]: id[0]})

food_kawa_herbata_slodkie = {
    "kawiarnia",
    "kawa",
    "kawy",
    "herbata",
    "kawa/herbata",
    "cafe",
    "ciasto",
    "ciastka",
    "ciasta",
    "ciastko",
    "pączek",
    "pączki",
    "czekolada",
    "kołacz",
    "kołacze",
    "naleśniki",
    "naleśnik",
    "żelki",
    "kołacz",
    "kołacza",
    "ice",
    "napój",
    "tea",
    "lody",
    "lodów",
}
food_pizza = {"pizza", "pizzę", "pizzy"}
food_kebab_kebap = {"kebap", "kebab"}
food_burger = {"burger", "burgery", "burgera", "burgers"}

services_delivery = {"glovo", "uber", "dostawa"}
services_tattoo = {"vean", "tattoo", "piercing", "tatuaż", "tatuażu", "tatuaże"}
services_gym = {"cityfit", "fitness"}

food_category = {
    "makaron",
    "bar",
    "posiłek",
    "menu",
    "frytek",
    "lunch",
    "frytki",
    "posiłki",
    "zupa",
    "lemoniada",
    "śniadanie",
    "thai",
    "gołe",
}.union(food_kebab_kebap, food_burger, food_pizza, food_kawa_herbata_slodkie)
alcohol_category = {
    "koktajl",
    "koktajle",
    "alkohol",
    "piwo",
    "piwa",
    "karafka",
    "shot",
    "shotów",
    "shoty",
    "wódka",
    "wódki",
    "kieliszek",
    "prosecco",
    "bacardi",
    "drink",
    "kamikaze",
    "pub",
    "wina",
    "wino",
}
services_category = set().union(services_delivery, services_tattoo, services_gym)

food_subcategories = [
    food_kawa_herbata_slodkie,
    food_pizza,
    food_kebab_kebap,
    food_burger,
]
services_subcategories = [services_delivery, services_tattoo, services_gym]

# main categories for append
app_food = []
app_alcohol = []
app_services = []

# subcategories for append
app_food_kawa_herbata_slodkie = []
app_food_pizza = []
app_food_kebab_kebap = []
app_food_burger = []

app_services_delivery = []
app_services_tattoo = []
app_services_gym = []

# all subcategories for append
all_app_subcategory_food = [
    app_food_kawa_herbata_slodkie,
    app_food_pizza,
    app_food_kebab_kebap,
    app_food_burger,
]
all_app_subcategory_services = [
    app_services_delivery,
    app_services_tattoo,
    app_services_gym,
]
all_app_main_category = [app_food, app_alcohol, app_services]

def check_all_sub(all_app):
    for subcategory in all_app:
        if subcategory:
            for place_coupon in subcategory:
                for place, coupon in place_coupon.items():
                    print(place, coupon)
            return True
    return False

def check_category(app_category):
    if app_category:
        for place_coupon in app_category:
            for place, coupon in place_coupon.items():
                print(place, coupon)
        return True
    return False

def check_for_subcategory(word, subcategories, appsubcategory):
    i = 0
    for subcategory in subcategories:
        if word in subcategory:
            appsubcategory[i].append({place.title(): coupon.capitalize()})
            return True
        i += 1
    return False

def write_to_file(new_file_name,category):
    with open(new_file_name+".csv", "w", encoding="utf-8") as f:
        f.write(header)
        for place_coupon in category:
            for place, coupon in place_coupon.items():
                f.write(f"{place},{coupon}\n")

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
        coupon_description = coupon.split(" ")
        del coupon_title[-1]  # usuń miasto z konca tytułu
        if word_is_not_founded:
            for word in coupon_title:
                if word in food_category:
                    word_is_not_founded = False
                    if check_for_subcategory(
                        word, food_subcategories, all_app_subcategory_food
                    ):
                        break
                    else:
                        app_food.append({place.title(): coupon.capitalize()})
                        break
                elif word in alcohol_category:
                    word_is_not_founded = False
                    app_alcohol.append({place.title(): coupon.capitalize()})
                    break
                elif word in services_category:
                    word_is_not_founded = False
                    if check_for_subcategory(
                        word, services_subcategories, all_app_subcategory_services
                    ):
                        break
                    else:
                        app_services.append({place.title(): coupon.capitalize()})
                        break
        if word_is_not_founded:
            for word in coupon_description:
                if word in food_category:
                    word_is_not_founded = False
                    if check_for_subcategory(
                        word, food_subcategories, all_app_subcategory_food
                    ):
                        break
                    else:
                        app_food.append({place.title(): coupon.capitalize()})
                        break
                elif word in alcohol_category:
                    word_is_not_founded = False
                    app_alcohol.append({place.title(): coupon.capitalize()})
                    break
                elif word in services_category:
                    word_is_not_founded = False
                    if check_for_subcategory(
                        word, services_subcategories, all_app_subcategory_services
                    ):
                        break
                    else:
                        app_services.append({place.title(): coupon.capitalize()})
                        break
        if word_is_not_founded:
            app_services.append({place.title(): coupon.capitalize()})

# generate files
header = "place, coupon\n"
files_names_main_category = ["food", "alcohol", "services"]
files_names_food_subcategory = [
    "food_kawa_herbata_slodkie",
    "food_pizza",
    "food_kebab_kebap",
    "food_burger",
]
files_names_services_subcategory = [
    "services_delivery",
    "services_tattoo",
    "services_gym",
]

get_path = os.getcwd()
folder_name = "csv_files"
path_for_files = os.path.join(get_path, folder_name)
try:
    os.makedirs(path_for_files)
except FileExistsError:
    pass

def write_all(all_app, file_name):
    i = 0
    for subcategory in all_app:
        if subcategory:
            with open(
                os.path.join(path_for_files, file_name[i] + ".csv"),
                "w",
                encoding="utf-8",
            ) as f:
                f.write(header)
                for place_coupon in subcategory:
                    for place, coupon in place_coupon.items():
                        f.write(f"{place},{coupon}\n")
        i += 1

write_all(all_app_subcategory_food, files_names_food_subcategory)
write_all(all_app_subcategory_services, files_names_services_subcategory)
write_all(all_app_main_category, files_names_main_category)