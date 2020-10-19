import requests
import bs4
import re
import os

amediavoz_urls = ["http://amediavoz.com/indice-A-K.htm",
                  "http://amediavoz.com/indice-L-Z.htm",
                  "http://amediavoz.com"]

path = "/home/nebur/Desktop/poemautomator/data"

discarded_urls = [
    "http://amediavoz.com/mediavoz.htm",
    "http://amediavoz.com/poetas.htm",
    "http://amediavoz.com/sensual.htm",
    "http://amediavoz.com/ventanas.htm",
    "http://amediavoz.com/tucuerpo.htm",
    "http://amediavoz.com/traducciones.htm",
    "http://amediavoz.com/poesiadeoro.htm",
    "http://amediavoz.com/index.htm",
    "http://amediavoz.com/indice-A-K.htm",
    "http://amediavoz.com/indice-L-Z.htm",
]


def getting_the_verses(poet_urls):
    verses_definitive = []

    for url_poet in poet_urls:
        verses_poet = []
        poet_name = url_poet[url_poet.rfind("/") + 1:url_poet.rfind(".")]

        try:
            with open(f"{path}/amediavoz/{poet_name}/verses_{poet_name}.txt") as f:
                print(f"[+] Retrieving verses from {poet_name} from file")
                verses_poet = f.read().split("\n")
                verses_definitive.extend(verses_poet)

        except FileNotFoundError:
            resp = requests.get(url_poet)

            if resp.status_code != 200:
                print(f"[-] ERROR {resp.status_code}: Not scraping {url_poet}")
                continue

            html = resp.text.replace("<br>", "\n")
            html = html.replace("\n\t\t", " ")
            html = html.replace("\n\t", " ")

            soup = bs4.BeautifulSoup(html, "lxml")

            if soup.title.text == "This site is temporarily unavailable":
                print(f"[-] ERROR: The site {url_poet} is temporarily unavailable")
                continue

            print(f"[+] Scraping {url_poet}")

            try:
                os.mkdir(f"{path}/amediavoz/{poet_name}")
            except FileExistsError:
                pass

            longest_block = ""
            blockquotes = soup.select("blockquote")
            for block in blockquotes:
                if len(block) > len(longest_block):
                    longest_block = block

            tables = longest_block.select("table")
            for table in tables:
                table.extract()

            emphasized = longest_block.select("p font em")
            for elem in emphasized:
                elem.extract()

            cursives = longest_block.select("p font i")
            for elem in cursives:
                elem.extract()

            fonts = longest_block.select("p font")

            for font in fonts:
                if (font.a
                        or font.img):
                    font.extract()
                    continue

                try:
                    size = font['size']
                    if size != "2":
                        font.extract()

                    elif "©" in font.text:
                        font.extract()

                    elif re.match("(Puedes +escucharl[a|o])", font.text):
                        font.extract()

                    elif "Versión de" in font.text:
                        font.extract()

                    elif re.match("(Puedes +visitarl[a|oe] en)", font.text):
                        font.extract()

                    elif "Volver a:" in font.text:
                        font.extract()

                except KeyError:
                    font.extract()
                    continue

            verses = []
            fonts = longest_block.select("p font")
            for font in fonts:
                verse = font.text.strip(" \xa0\n\t")
                verses.extend(verse.split("\n"))

            for verse in verses:
                verse = verse.strip()

                if not verse or len(verse) < 6:
                    continue

                elif verse.upper() == verse:
                    verse = verse.capitalize()

                patt = re.compile(" +")
                verse = re.sub("\xa0", " ", verse)
                verse = re.sub(patt, " ", verse)
                verses_poet.append(verse)

            verses_definitive.extend(verses_poet)

            with open(f"{path}/amediavoz/{poet_name}/verses_{poet_name}.txt", "w") as f:
                print("\n".join(verses_poet), file=f)

    print("[+] Done\n")
    return verses_definitive


def getting_amediavoz_links(urls):
    print("[+] Getting the poets-urls from amediavoz.com")

    if not os.path.exists(f"{path}/amediavoz"):
        os.mkdir(f"{path}/amediavoz")

    poets_urls = []
    for amedia_url in urls:
        resp = requests.get(amedia_url)
        soup = bs4.BeautifulSoup(resp.text, "lxml")

        anchors = soup.select("font a")
        anchors = ["http://amediavoz.com" + anchor["href"][1:] for anchor in anchors]

        for anchor in anchors:
            if (
                    anchor.endswith(".htm")
                    and anchor not in poets_urls
                    and anchor not in discarded_urls
            ):
                poets_urls.append(anchor)

    print("[+] Done\n")
    return poets_urls


def main():
    links = getting_amediavoz_links(amediavoz_urls)
    verses = getting_the_verses(links)
    print(verses)


if __name__ == "__main__":
    main()
