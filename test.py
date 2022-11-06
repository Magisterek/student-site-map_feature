import json


with open("test_json.json", "r", encoding="utf-8") as f:
    data = json.load(f) 
    def check_all_sub(your_category): 
        if your_category in data["all_app"].keys(): 
            for place_coupon in data["all_app"][your_category].values():
                for place, coupon in place_coupon.items():
                    print(place, coupon)
                return True
        return False
        #DONE 

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
    # print(data["categories"]["food_category"]["sweet"])
