import bs4
import requests


"""FROM FIlES TO DB CHANGE EVERYTHING"""

class Rhymer:
    def __init__(self, word, syllables, words_to_discard=[]):
        self.word = word
        self.words_to_discard = words_to_discard
        self.syllables = syllables

        if not syllables:
            self.syllables = "I"

        self.rhymes_list = []
        self.url = f"https://www.cronopista.com/onlinedict/index.php?word={self.word}&type=c&silables={self.syllables}&orderBy=R&begining=I&category=I"
        self.request_text = self.request_url(self.url)
        self.soup = bs4.BeautifulSoup(self.request_text, "lxml")

        self.rhyme = self.parsing_the_soup(self.soup)

    def parsing_the_soup(self, soup):
        rhyme = ""
        rhymes_lr_tags = soup.select("div[class=lr] b")

        rhymes_tags = [rhyme.text for rhyme in rhymes_lr_tags]

        for rhyme in rhymes_tags:
            if rhyme not in self.words_to_discard and rhyme != self.word:
                self.rhymes_list.append(rhyme)

        for rhyme in self.rhymes_list:
            if rhyme != self.word and rhyme not in self.words_to_discard:
                return rhyme

    def request_url(self, url):
        headers = {"user-agent": "Chrome/41.0.2272.96"}
        resp = requests.get(url, headers=headers)
        return resp.text


def main():
    input_word = input("palabra a rimar: ")
    input_syll = input("num of syllables: ")
    input_list = input("palabras a excluir separadas por comas: ")

    discard_list = input_list.split(", ")

    rhymer = Rhymer(input_word, input_syll, discard_list)

    print(rhymer.rhymes_list)


if __name__ == "__main__":
    main()
