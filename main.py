from requests import get
from bs4 import BeautifulSoup
import re
import os
import json


def city_id():
    url = "https://estarter.pl/"
    soup = BeautifulSoup(get(url).content, "html.parser")
    cities = soup.find_all("option")
    city_and_id_pattern = r"\d{6}"
    city_pattern = r"^\w+"
    for city_option in cities:
        id = re.findall(city_and_id_pattern, str(city_option))
        city = re.findall(city_pattern, str(city_option)[64:])
        # check for emptiness
        if city:  # and id
            city_and_id.update({city[0]: id[0]})

def check_category(your_category):
    if your_category in data["table"]["to_append"].keys():
        for array_of_places in data["table"]["to_append"][your_category].values():
            for place_coupon in array_of_places:
                for place, coupon in place_coupon.items():
                    print(place, coupon)
        return True
    return False

def check_all_subcategories():
    for key in data["table"]["to_append"].keys():
        check_category(key)

def search_for_subcategory(word):
    for category in data["categories"]:
        for subcategory in data["categories"][category]:
            if word in data["categories"][category][subcategory]:
                data["table"]["to_append"][category][subcategory].append(
                    {place.title(): coupon.capitalize()}
                )
                return True
    return False

def write_all():
        header = "miejsce, kupon\n"
        get_path = os.getcwd()
        folder_name = "csv_files"
        path_for_files = os.path.join(get_path, folder_name)

        try:
            os.makedirs(path_for_files)
        except FileExistsError:
            pass

        for category in data["table"]["to_append"]:
            for subcategory in data["table"]["to_append"][category]:
                with open(
                    os.path.join(
                        path_for_files,
                        data["table"]["with_file_name"][category][subcategory] + ".csv",
                    ),
                    "w",
                    encoding="utf-8"
                ) as f:
                    f.write(header)
                    for place_coupon in data["table"]["to_append"][category][
                        subcategory
                    ]:
                        for place, coupon in place_coupon.items():
                            f.write(f"{place},{coupon}\n")

city_and_id = {}
city_id()

with open("data_structure.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    for city, id in city_and_id.items():
        url = (
            f"https://estarter.pl/pl/offer/index/id_category/{id}/category_name/{city}"
        )
        soup = BeautifulSoup(get(url).content, "html.parser")
        place_option = soup.find_all("p", class_="card-text")
        coupon_option = soup.find_all("h4", class_="card-title")
        for x in range(len(place_option)):
            place = place_option[x].get_text().replace(",", "").lower()
            coupon = coupon_option[x].get_text().lower()
            word_is_not_found = True
            coupon_title = place.split(" ")
            coupon_description = coupon.split(" ")
            del coupon_title[-1]  # remove city name from title
            if word_is_not_found:
                for word in coupon_title:
                    if search_for_subcategory(word):
                        word_is_not_found = False
                        break
            if word_is_not_found:
                for word in coupon_description:
                    if search_for_subcategory(word):
                        word_is_not_found = False
                        break
            if word_is_not_found:
                data["table"]["to_append"]["services"]["others"].append(
                    {place.title(): coupon.capitalize()}
                )
    write_all()
