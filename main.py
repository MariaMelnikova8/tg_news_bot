import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from os import getenv
import os.path
from send_post import telegram_send_message
from time import sleep


def get_cp_data():
    coop_land_url = 'https://coop-land.ru'
    coop_land_response = requests.get(coop_land_url)
    coop_land_soup = BeautifulSoup(coop_land_response.text, features="html.parser")
    coop_land_some_headline = coop_land_soup.find('h2', class_="title").text
    coop_land_description = coop_land_soup.find('div', class_="preview-text").text
    coop_land_source = coop_land_soup.find('div', class_="article-content").find('a')["href"]
    coop_land_picture = coop_land_soup.find('div', class_="image").find('img')["data-src"]
    coop_land_picture_link = coop_land_url + coop_land_picture
    coop_land = [coop_land_some_headline, coop_land_description, coop_land_source, coop_land_picture_link]
    return coop_land


def get_ig_data():
    igromania_url = 'https://www.igromania.ru/news'
    igromania_response = requests.get(igromania_url)
    igromania_soup = BeautifulSoup(igromania_response.text, features="html.parser")
    igromania_some_headline = igromania_soup.find('a', class_="aubli_name").text
    igromania_description = igromania_soup.find('div', class_="aubli_desc").text
    igromania_source = igromania_soup.find('div', class_="aubli_data").find('a')["href"]
    igromania_picture = igromania_soup.find('div', class_="aubl_item").find('img')["src"]
    igromania_picture_link = igromania_url + igromania_picture
    igromania = [igromania_some_headline, igromania_description, igromania_source, igromania_picture_link]
    return igromania


if __name__ == '__main__':
    if not os.path.isfile('last_post.txt'):
        previous_post = open("last_post.txt", "w")
        previous_post.close()
    check = 1

    while True:
        with open("last_post.txt", "r") as previous_post:
            previous_post_content = previous_post.read()

        if 'coop-land' in previous_post_content:
            check = 2
        else:
            check = 1

        load_dotenv()
        tg_id = getenv('tg_id')
        tg_token = getenv('tg_token')

        try:
            if check == 1:
                some_headline, description, source, picture_link = get_cp_data()
            else:
                some_headline, description, source, picture_link = get_ig_data()

            post = f"{some_headline}\n{description}\nСсылка на источник: {source}"

            with open("last_post.txt", "w") as my_file:
                my_file.write(source)

            telegram_send_message(tg_id, post, picture_link, tg_token)
        except:
            print('Возникла ошибка. Пост не был отправлен.')
        sleep(18000)




