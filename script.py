import env as env
import requests
from urllib.parse import urlparse

from environs import Env


TOKEN = env.str("BITLY_TOKEN")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def shorten_link(users_link):
    url = "https://api-ssl.bitly.com/v4/shorten"
    body = {
        "long_url": users_link,
        "domain": "bit.ly",
    }
    short_site = requests.post(url, headers=HEADERS, json=body)
    short_site.raise_for_status()
    return short_site.json()["link"]


def count_clicks(short_link):
    parsed_link = urlparse(short_link)
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{parsed_link.netloc}{parsed_link.path}/clicks/summary"
    total_clicks = requests.get(url, headers=HEADERS)
    total_clicks.raise_for_status()
    return total_clicks.json()["total_clicks"]

def check_if_binlink(short_link):
    parsed_link = urlparse(short_link)
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{parsed_link.netloc}{parsed_link.path}"
    info_link = requests.get(url, headers=HEADERS)
    return info_link.ok


if __name__ == "__main__":
    env = Env()
    env.read_env()

    users_link = input("Введите адрес сайта: ")
    if check_if_binlink(users_link):
        try:
            clicks_count = count_clicks(users_link)
            print(f"Количество кликов: {clicks_count}")
        except requests.exceptions.HTTPError:
            print("Ошибка. Неверный ввод ссылки.")
    else:
        try:
            short_link = shorten_link(users_link)
            print(f"Сокращенная сылка :{short_link}")
        except requests.exceptions.HTTPError:
            print("Ошибка. Неверный ввод ссылки.")
