import bs4
import requests
import os

"""Variable to hold the parsed lines"""
verses = []

"""strings to exclude"""
roman_numerals = [
    "I",
    "II",
    "III",
    "IV",
    "V",
    "VI",
    "VII",
    "VIII",
    "IX",
    "X",
    "XI",
    "XII",
    "XIII",
    "XIV",
    "XV",
    "XVI",
    "XVII",
    "XVIII",
    "XIX",
    "XX",
    "XXI",
    "XXII",
    "XXIII",
    "XXIV",
    "XXV",
]

"""Path to poems"""
path = "/home/nebur/Desktop/poemautomator/data/buscapoemas"

"""List of poets to exclude"""
exclude_poets = [
    "https://www.buscapoemas.net/poeta/Alfonso-X-el-Sabio.htm",
    "https://www.buscapoemas.net/poeta/Francisco-de-Rojas-Zorrilla.htm",
    "https://www.buscapoemas.net/poeta/Fray-Luis-de-León.htm",
    "https://www.buscapoemas.net/poeta/Diego-de-Torres-y-Villarroel.htm",
    "https://www.buscapoemas.net/poeta/Cristóbal-de-Castillejo.htm",
    "https://www.buscapoemas.net/poeta/Bartolomé-de-Argensola.htm",
    "https://www.buscapoemas.net/poeta/Baltasar-del-Alcázar.htm",
    "https://www.buscapoemas.net/poeta/Gonzalo-de-Berceo.htm",
    "https://www.buscapoemas.net/poeta/Gutierre-de-Cetina.htm",
    "https://www.buscapoemas.net/poeta/Jorge-Manrique.htm",
    "https://www.buscapoemas.net/poeta/Juan-Boscán.htm",
    "https://www.buscapoemas.net/poeta/Juan-Ruiz-Arcipreste-de-Hita.htm",
    "https://www.buscapoemas.net/poeta/Juan-de-Tassis-y-Peralta.htm",
    "https://www.buscapoemas.net/poeta/Marqués-de-Santillana.htm",
    "https://www.buscapoemas.net/poeta/San-Juan-de-la-Cruz.htm",
    "https://www.buscapoemas.net/poeta/Tirso-de-Molina.htm",
    "https://www.buscapoemas.net/poeta/José-Antonio-Ramos-Sucre.htm",
]


def getting_the_verses(poem_url, poet_path):
    """filtering the lines and the tags"""
    poem_name = poem_url[34:]
    poem_name = poem_name[:poem_name.find("/")]

    resp = requests.get(poem_url)
    soup = bs4.BeautifulSoup(resp.text, "lxml")

    poem = soup.select("#poema_contenedor_poema")[0]

    verses_poem = []
    for elem in poem:
        if isinstance(elem, bs4.element.NavigableString):
            if str(elem) not in roman_numerals and str(elem).upper() != str(elem):
                verso = str(elem).replace("\xa0", " ").strip()
                verses_poem.append(verso)

    with open(f"{path}/{poet_path}/{poem_name}.txt", "w") as f:
        print("\n".join(verses_poem), file=f)

    return verses_poem


def getting_poets(buscapoemas_url):
    """parsing the POET-URLS"""

    if not os.path.exists(path):
        os.mkdir(path)

    resp = requests.get(buscapoemas_url)
    soup = bs4.BeautifulSoup(resp.text, "lxml")
    anchors = soup.select("li a")
    hrefs = [anchor["href"] for anchor in anchors]
    links = [href for href in hrefs if "/poeta/" in href]
    poet_urls = set(links)

    return poet_urls


def getting_poems(poet_url, poet_path):
    """parsing the POEM-URLS"""

    try:
        os.mkdir(f"{path}/{poet_path}")
    except FileExistsError:
        pass

    resp = requests.get(poet_url)
    soup = bs4.BeautifulSoup(resp.text, "lxml")
    poem_anchors = soup.select(".slot_poema_autor")
    poem_urls = [tag.a["href"] for tag in poem_anchors]

    return poem_urls


def main():
    url = "https://www.buscapoemas.net/poetas.html"
    alt = input("alternative url? [Y/N]")
    if alt.capitalize() == "Y":
        url = input("URL to input: ")

    poem_urls = getting_poems(url)

    verses = []
    for poem_url in poem_urls:
        print("[+] Extracting {}".format(poem_url))
        verses.extend(getting_the_verses(poem_url))


if __name__ == "__main__":
    main()
