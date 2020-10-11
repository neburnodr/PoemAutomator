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

    for poet_url in poet_urls:
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
        verses.extend(getting_the_verses(poem_url))


if __name__ == "__main__":
    main()
