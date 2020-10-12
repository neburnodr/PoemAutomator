import bs4
import requests

"""Variable to hold the parsed lines"""
verses = []

"""strings to exclude"""
roman_numerals = ["I", "II", "III", "IV", "V",
                  "VI", "VII", "VIII", "IX", "X",
                  "XI", "XII", "XIII", "XIV", "XV",
                  "XVI", "XVII", "XVIII", "XIX", "XX",
                  "XXI", "XXII", "XXIII", "XXIV", "XXV",]


"""filtering the lines and the tags"""
def getting_the_verses(url):
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text, "lxml")

    poem = soup.select("#poema_contenedor_poema")[0]

    verses_poem = []
    for elem in poem:
        if isinstance(elem, bs4.element.NavigableString):
            if str(elem) not in roman_numerals and str(elem).upper() != str(elem):
                verso = str(elem).replace("\xa0", " ").strip()
                verses_poem.append(verso)

    return verses_poem


"""parsing the POET-URLS"""
def getting_poets(url):
    print("[+] Scraping buscapoemas.net", end="\n\n")

    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text, "lxml")
    anchors = soup.select("li a")
    hrefs = [anchor["href"] for anchor in anchors]
    links = [href for href in hrefs if "/poeta/" in href]
    poet_urls = set(links)
    return poet_urls


"""parsing the POEM-URLS"""
def getting_poems(url):
    poet_urls = getting_poets(url)
    poem_urls = []

    exclude_poets = ["https://www.buscapoemas.net/poeta/Alfonso-X-el-Sabio.htm",
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
                     ]

    for poet_url in poet_urls:
        if poet_url not in exclude_poets:
            print("[+] Scraping {}".format(poet_url))

            resp = requests.get(poet_url)
            soup = bs4.BeautifulSoup(resp.text, "lxml")
            poem_anchors = soup.select(".slot_poema_autor")
            poem_urls.extend([tag.a["href"] for tag in poem_anchors])

    return poem_urls


"""Main programm"""
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
