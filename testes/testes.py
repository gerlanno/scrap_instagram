from googlesearch import search

import sys


# pesquisa do google, salvas num set, evitando resultados duplicados
def pesquisa(query, results):
    resultados = set()
    for url in search(query, pause=3, start=0, stop=results, lang="pt-br"):
        print(url)
    return resultados


pesquisa('site:instagram.com intext:(88) "Cartório"', 1)