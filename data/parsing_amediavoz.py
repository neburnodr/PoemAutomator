import requests
import bs4
import re

url = "http://amediavoz.com/indice-A-K.htm"
url2 = "http://amediavoz.com/indice-L-Z.htm"


def getting_the_verses(links):
    verses_definitive = []

    for link in links:

        print(f"[+] Scraping {link}")

        resp = requests.get(link)
        html = resp.text.replace("<br>", "\n")
        html = html.replace("\n\t\t", " ")

        soup = bs4.BeautifulSoup(html, 'lxml')

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
            verse_new = re.sub("\xa0", ' ', verse)
            patt = re.compile(" +")
            verse_newest = re.sub(patt, ' ', verse_new)
            verses_definitive.append(verse_newest)

    print("[+] Done", end="\n\n")
    return verses_definitive


def getting_amediavoz_links(urls):
    links = []
    discarded_urls = ["http://amediavoz.com/mediavoz.htm",
                      "http://amediavoz.com/poetas.htm",
                      "http://amediavoz.com/sensual.htm",
                      "http://amediavoz.com/ventanas.htm",
                      "http://amediavoz.com/tucuerpo.htm",
                      "http://amediavoz.com/traducciones.htm",
                      "http://amediavoz.com/poesiadeoro.htm",
                      "http://amediavoz.com/index.htm",
                      "http://amediavoz.com/indice-A-K.htm",
                      "http://amediavoz.com/indice-L-Z.htm"
                      ]

    for url in urls:
        resp = requests.get(url)
        soup = bs4.BeautifulSoup(resp.text, 'lxml')

        anchors = soup.select("font a")
        anchors = ['http://amediavoz.com' + anchor['href'][1:] for anchor in anchors]

        for anchor in anchors:
            if anchor.endswith(".htm") and anchor not in links and anchor not in discarded_urls:
                links.append(anchor)

    return links


def main():
    links = getting_amediavoz_links(url).extend(getting_amediavoz_links(url2))
    verses = getting_the_verses(links)

    '''
    saving?
    saving_the_verses(verses)'''

if __name__ == "__main__":
    main()
