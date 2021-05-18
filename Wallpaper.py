import lxml
import chardet
import bs4
import os
import pycurl_requests as requests
import random
import string


from bs4 import *


def generate_random_string(Ammount):
    string_returned = "".join(random.choice(string.ascii_letters) for i in range(0, Ammount))
    return string_returned


def get_categories():
    link_holder = []
    base_url = "https://wallpapers.com/"
    req_url = requests.get(base_url)
    soup = BeautifulSoup(req_url.content, "lxml")
    for count, link in enumerate(soup.find_all("a")):
        link_holder.append(link.get("href"))
    return link_holder


def pick_category():
    category_list = get_categories()
    for count, i in enumerate(category_list):
        try:
            print(
                count,
                f"\033[92m{i.split('https://wallpapers.com/', 2)[1].upper().replace('-', ' ')}\033[00m",
            )
        except:
            pass
    chosen_category = input("Enter Category Number: ")
    return category_list[int(chosen_category)]


def scrape_sub_category():
    category = pick_category()
    link_holder = []
    base_url = category
    req_url = requests.get(base_url)
    soup = BeautifulSoup(req_url.content, "lxml")
    for count, link in enumerate(soup.find_all("a", attrs={"class": "caption stretched-link"})):
        print(
            count,
            f"\033[92m{link.get('href').split('https://wallpapers.com/', 2)[1].upper().replace('-', ' ')}\033[00m",
        )
        link_holder.append(link.get("href"))
    if len(link_holder) > 0:
        chosen_category = input("Select Category Number: ")
        return str(link_holder[int(chosen_category)])
    if len(link_holder) <= 0:
        random_name = generate_random_string(10)
        for count, link in enumerate(soup.find_all("img")):
            try:
                link_holder.append(f"https://wallpapers.com{link.get('data-src')}")
            except:
                link_holder.append(f"https://wallpapers.com{link.get('data-src')}")
        try:
            os.mkdir(f"{random_name}")
        except:
            print("Already A Directory")
        for count, i in enumerate(link_holder):
            try:
                image = requests.get(i).content
                with open(f"{random_name}/{count}.jpg", "wb+") as f:
                    f.write(image)
            except:
                print("\033[91mError\033[00m")
        return 0


def main(category):
    base_url = category
    if base_url != 0:
        req_url = requests.get(base_url)
        print(base_url)
        soup = BeautifulSoup(req_url.content, "lxml")
        try:
            os.mkdir(f"{base_url.split('https://wallpapers.com/', 1)[1]}")
        except:
            print("Already A Directory")
        for count, image in enumerate(soup.findAll("img")):
            try:
                image = requests.get(f"https://wallpapers.com{image.get('data-src')}").content
                with open(
                    f"{base_url.split('https://wallpapers.com/', 1)[1]}/{count}.jpg",
                    "wb+",
                ) as f:
                    f.write(image)
            except:
                try:
                    image = requests.get(f"https://wallpapers.com{image.get('src')}").content
                    with open(
                        f"{base_url.split('https://wallpapers.com/', 1)[1]}/{count}.jpg",
                        "wb+",
                    ) as f:
                        f.write(image)
                except:
                    print("\033[91mError\033[00m")

    elif base_url == 0:
        print("Done")


if __name__ == "__main__":
    while 1:
        main(category=scrape_sub_category())