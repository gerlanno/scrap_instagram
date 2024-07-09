from time import sleep
from bs4 import BeautifulSoup
import json
import httpx
from urllib.request import urlopen
import re
from datetime import time

def scrap_insta(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    bio = soup.findAll("span", attrs={"class": "_ap3a"})
    print(bio)

client = httpx.Client(
    headers={
        # this is internal ID of an instegram backend app. It doesn't change often.
        "x-ig-app-id": "936619743392459",
        # use browser-like features
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
    }
)


def scrape_user(username: str):

    """Scrape Instagram user's data"""
    result = client.get(
        f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
    )
    data = json.loads(result.content)
    return data["data"]["user"]

def show_data(user_list):
    for user in user_list:
        data = scrape_user(user)
        print(f"{extrair_numeros_telefone(data.get("biography"))}, {data.get("external_url")}, {data.get("full_name")}")
        sleep(3)

# regex para obter os números de telefones nas strings da bio
def extrair_numeros_telefone(texto):
    padroes = [
        re.compile(
            r"\(?\d{2}\)?\s?\d{1}\s?\d{4}[-.\s]?\d{4}"
        ),  # (85) 9 9999-9999, 85 9 9999-9999,
        re.compile(r"\(?\d{2}\)?\s?\d{4}[-.\s]?\d{4}"),  # (85) 9999-9999, 85 9999-9999,
        re.compile(r"\d{4}[-.\s]?\d{4}"),  # 9999-9999, 9999.9999, 9999 9999,
        re.compile(
            r"\(?\d{2}\)?\s?\d{1}\s?\d{5}[-.\s]?\d{4}"
        ),  # (85) 9 99999-9999, 85 9 99999-9999,
    ]
    numeros_telefone = []
    for padrao in padroes:
        numeros_telefone.extend(padrao.findall(texto))

    return formatar_numero(numeros_telefone)


# padronizar os números de telefone, deixando sem espaços nem caracteres especiais
def formatar_numero(lista):
    formated_list = []
    for i, num in enumerate(lista):
        numero = ""
        for char in num:
            if char.isnumeric():
                numero += char
        formated_list.append(numero)
    return formated_list
