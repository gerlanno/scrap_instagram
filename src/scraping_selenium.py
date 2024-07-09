from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse, parse_qs
from model import InstagramUser, inserir_dados
from time import sleep
import re

chrome_options = Options()
# chrome_options.add_argument("--incognito")  # Navegação anonima

chrome_options.set_capability(
    "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


def scrap_instagram(urls):
    """
    Percorrer uma lista de perfis do instagram e fazer a raspagem dos dados. 
    """
    lista_perfis = []
    try:
        driver.get("https://www.instagram.com")
        wait = WebDriverWait(driver, 10)
        form_login = wait.until(EC.visibility_of_element_located((By.ID, "loginForm")))
        username = form_login.find_element(By.NAME, "username")
        username.clear()
        username.send_keys("gerlannoteste")
        password = form_login.find_element(By.NAME, "password")
        password.send_keys("testespython")
        form_login.find_element(By.CSS_SELECTOR, "._acap").click()
        sleep(5)

    except Exception as e:
        pass
    for url in urls:
        telefones = ""
        link_bio = ""
        email = ""

        driver.get(url)

        try:
            # checar se existe a opção de expandir o texto da bio do instagram e clicar nele
            botao_mais = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/section[4]/div/span/span/div/span",
                    )
                )
            )
            botao_mais.click()

        except Exception as e:
            print(f"erro ao expandir a bio")

        finally:
            # captura o texto da bio do instagram, para extrair os numeros de telefone e email.
            bio = driver.find_element(
                By.XPATH,
                "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/section[4]/div/span/div/span",
            )
            telefones = extrair_numeros_telefone(bio.text)
            email = extrair_emails(bio.text)

            try:
                # checa se existe links no perfil do instagram.
                site = driver.find_element(
                    By.XPATH,
                    "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/section[4]/div/div[3]/div/a",
                )

                link_bio = get_url(site.get_attribute("href"))

            except Exception as e:
                # Se acaso o perfil tiver a opção "profissão" preenchida, o xpath dos links mudam
                print("Erro buscando a div[3], buscando a div[4]")

                try:
                    site = driver.find_element(
                        By.XPATH,
                        "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/section[4]/div/div[4]/div/a",
                    )
                    link_bio = get_url(site.get_attribute("href"))

                except Exception as e:
                    try:
                        # terceira opção de capturar links, quando o perfil tem mais de um link cadastrado, eles são exibidos em uma caixa de dialogo flutuante.
                        links = driver.find_element(
                            By.CSS_SELECTOR,
                            "div._ap3a:nth-child(2)",
                        )
                        links.click()
                        # Aguardar a caixa de dialogo dos links abrir
                        dialog_box = wait.until(
                            EC.visibility_of_element_located(
                                (
                                    By.XPATH,
                                    "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/div/div",
                                )
                            )
                        )

                        # Encontrar todos links na caixa de dialogo
                        links_in_dialog = dialog_box.find_elements(By.TAG_NAME, "a")

                        # Extrair as URLs dos links
                        link_urls = [
                            link.get_attribute("href") for link in links_in_dialog
                        ]
                        # Extrair o redirecionamento das urls instagram e concatenar todos os links existentes.
                        link_bio = " ".join(get_url(link) for link in link_urls)

                    except Exception as e2:
                        print(f"nenhum link localizado, {e2}")

                    print(f"Erro: {e}")

            lista_perfis.append(
                InstagramUser(
                    username=get_usernames(url),
                    url_perfil=url,
                    telefone=telefones,
                    website=link_bio,
                    email=email,
                )
            )
            print(f"{url} - {telefones} - {link_bio} - {email}")
        sleep(2)
    inserir_dados(lista_perfis)
    driver.quit()


# Extrair números de telefones das strings a partir de uma expressão regular.
def extrair_numeros_telefone(texto):
    # (85) 9.9999-9999, (85) 9-9999-9999, 85 9 9999-9999
    padrao = re.compile(r"\(?\d{2}\)?\s?\d{1}[-.\s]?\d{4}[-.\s]?\d{4}")
    numeros_telefone = padrao.findall(texto)

    return formatar_numero(numeros_telefone[0] if numeros_telefone else "")


# padronizar os números de telefone, deixando sem espaços nem caracteres especiais
def formatar_numero(numero):
    numero_formatado = ""
    for char in numero:
        if char.isnumeric():
            numero_formatado += char

    return f"55{numero_formatado}" if numero else ""


# captura a url final, retirando o redirecionamento do instagram.
def get_url(redirect_url):
    parsed_url = urlparse(redirect_url)
    query_params = parse_qs(parsed_url.query)
    final_url = query_params.get("u", [None])[0]
    return final_url


# função para capturar emails contidos no texto da bio.
def extrair_emails(texto):
    padrao = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    email = padrao.findall(texto)
    return email[0] if email else ""


# retornar somente o nome de usuario da url.
def get_usernames(url):
    username = url.split("https://www.instagram.com/")
    return username[1]
