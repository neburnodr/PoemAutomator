import requests
import bs4
import re
import os

url = "http://amediavoz.com/indice-A-K.htm"
url2 = "http://amediavoz.com/indice-L-Z.htm"


path = "/home/nebur/Desktop/poemautomator/data"


def getting_the_verses(poet_urls):
    verses_definitive = []

    for url_poet in poet_urls:
        verses_poet = []

        poet_name = url_poet[url_poet.rfind("/") + 1:url_poet.rfind(".")]
        if not os.path.exists(f"{path}/{poet_name}"):
            os.mkdir(f"{path}/{poet_name}")

        print(f"[+] Scraping {url_poet}")

        resp = requests.get(url_poet)
        html = resp.text.replace("<br>", "\n")
        html = html.replace("\n\t\t", " ")

        soup = bs4.BeautifulSoup(html, "lxml")

        titles = soup.select("blockquote blockquote p font a")
        for title in titles:
            title.extract()

        paragraphs = soup.select("blockquote blockquote p")
        for paragraph in paragraphs:
            if "Versión de" in paragraph.text:
                paragraph.extract()

        blockquotes = soup.select("blockquote blockquote")
        poems = ""

        for blockquote in blockquotes:
            block = blockquote.text
            if len(block) > len(poems):
                poems = block

        verses = poems.split("\n")

        verses_clean = [verse.strip("\n\xa0") for verse in verses]

        verses_almost = []
        for verse in verses_clean:
            verse = verse.strip()
            if not verse:
                continue
            if "Reseña" in verse:
                continue
            elif any(char.isnumeric() for char in verse):
                continue
            elif verse == "De ":
                continue
            elif verse == "\xa0":
                continue
            elif "Versión de" in verse:
                continue
            elif len(verse) < 4:
                continue
            else:
                verses_almost.append(verse)

        for verse in verses_almost:
            verse_new = re.sub("\xa0", " ", verse)
            patt = re.compile(" +")
            verse_newest = re.sub(patt, " ", verse_new)

            verses_poet.append(verse_newest)

        verses_definitive.extend(verses_poet)
        with open(f"{path}/{poet_name}/verses_{poet_name}.txt", "w") as f:
            print("\n".join(verses_poet), file=f)

    print("[+] Done", end="\n\n")
    return verses_definitive


def getting_amediavoz_links(urls):
    if not os.path.exists(path):
        os.mkdir(path)

    links = []
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

    for amedia_url in urls:
        resp = requests.get(amedia_url)
        soup = bs4.BeautifulSoup(resp.text, "lxml")

        anchors = soup.select("font a")
        anchors = ["http://amediavoz.com" + anchor["href"][1:] for anchor in anchors]

        for anchor in anchors:
            if (
                anchor.endswith(".htm")
                and anchor not in links
                and anchor not in discarded_urls
            ):
                links.append(anchor)

    return links


def main():
    links = getting_amediavoz_links(url).extend(getting_amediavoz_links(url2))
    verses = getting_the_verses(links)
    print(verses)


if __name__ == "__main__":
    main()
