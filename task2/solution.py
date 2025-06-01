from collections import defaultdict
import requests
from bs4 import BeautifulSoup
import csv


BASE_URL = "https://ru.wikipedia.org"
CATEGORY_URL = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"


def get_soup(url):
    """Загружает страницу и возвращает объект BeautifulSoup"""
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def count_animals(url):
    """Подсчитываем количество животных с учётом пагинации"""

    count = defaultdict(int)
    while True:
        soup = get_soup(url)
        category_divs = soup.find_all('div', class_='mw-category-group')
        if not category_divs:
            break

        for div in category_divs:
            li_tags = div.find_all('li')
            for animal in li_tags:
                name = animal.find('a').text
                if len(name):
                    first_letter = name[0].upper()
                    count[first_letter] += 1

        next_link = soup.find(
            'a', string=lambda text: text and 'следующая страница' in text.lower())
        if next_link:
            url = BASE_URL + next_link.get('href')
        else:
            break

    return count


def write_results_to_csv(results):
    """Записывает результаты в CSV-файл."""

    with open("beasts.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for letter, count in sorted(results.items()):
            writer.writerow([letter, count])


def main():
    results = count_animals(CATEGORY_URL)
    write_results_to_csv(results)
    print("Результаты записаны в beasts.csv")


if __name__ == "__main__":
    main()
