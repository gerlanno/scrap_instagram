from os import sep
import re
from time import sleep
from googlesearch import search
from scraping_selenium import scrap_instagram
from model import inicializar_bd
import sys


# pesquisa do google, salvas num set, evitando resultados duplicados
def pesquisa(query, results):
    resultados = set()
    for url in search(query, pause=3, start=10, num=results, lang="pt-br"):
        resultados.add(adjust_url(url))
    return resultados


# Ajusta as url, para a pagina inicial do profile
def adjust_url(url):
    partes = 4
    url_partes = url.rsplit("/")
    url_truncada = "/".join(url_partes[:partes])

    return url_truncada


# pesquisa = pesquisa('site:instagram.com intext:(88) "Cartório"')

# print(pesquisa)
# scrap_instagram(pesquisa)
# get_usernames(pesquisa('site:instagram.com intext:(88) "Cartório"'))

try:

    query = sys.argv[1].lower()

    max_results = int(sys.argv[2])

    inicializar_bd()

    scrap_instagram(pesquisa(query, max_results))

except ValueError as e:
    print(f"o argumento de resultados precisa ser um numero inteiro: {e}")
