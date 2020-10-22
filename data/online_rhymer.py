import bs4
import requests
from typing import List

"""FROM FIlES TO DB CHANGE EVERYTHING"""


class Rhymer:
    def __init__(self, word: str, rhy_type: str = "c", syllables: int = "I", words_to_discard: List = None) -> None:
        self.word = word
        self.rhy_type = rhy_type
        self.syllables = syllables
        self.first_letter = find_first_letter(word)
        self.words_to_discard = words_to_discard

    def getting_cronopista(self) -> List:
        word_type = self.getting_word_type()

        url = f"""https://www.cronopista.com/onlinedict/index.php?
                  word={self.word}
                  &type={self.rhy_type}
                  &silables={self.syllables}
                  &orderBy=R
                  &begining={self.first_letter}
                  &category={word_type}"""

        headers = {"user-agent": "Chrome/41.0.2272.96"}

        resp = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(resp.text, "lxml")

        rhymes_list = self.parsing_the_soup(soup)
        return rhymes_list

    def parsing_the_soup(self, soup: bs4.BeautifulSoup) -> List:
        rhymes = []
        rhymes_tags = soup.select("div[class=lr] b")
        rhymes_text = [rhyme.text for rhyme in rhymes_tags]

        for rhyme in rhymes_text:
            if rhyme not in self.words_to_discard and rhyme != self.word:
                rhymes.append(rhyme)

        return rhymes

    def getting_word_type(self) -> str:
        resp = requests.get(f"https://www.buscapalabra.com/categoria-gramatical-tiempo-verbal.html?palabra={self.word}")
        soup = bs4.BeautifulSoup(resp.text, "lxml")

        type_word = soup.select("h3[class=catgram]")

        for type_word in type_word:

            if "Nombre" in type_word.text or "Adjetivo" in type_word.text:
                return "0"

            if "Verbo" in type_word.text:
                return "1"

        return "I"


def find_first_letter(word):
    if word[0] in "aeiouAEIOUáéíóúÁÉÍÓÚhH":
        return "true"
    else:
        return "false"


def main():
    input_word = input("palabra a rimar: ")
    input_syll = int(input("num of syllables: "))
    input_list = input("palabras a excluir separadas por comas: ")

    discard_list = input_list.split(", ")

    rhymer = Rhymer(input_word, syllables=input_syll, words_to_discard=discard_list)

    print(rhymer.getting_cronopista())


if __name__ == "__main__":
    main()
