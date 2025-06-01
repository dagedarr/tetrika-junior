import unittest
from unittest.mock import patch
from collections import defaultdict
from task2.solution import count_animals
from bs4 import BeautifulSoup


class TestAnimalCounter(unittest.TestCase):
    @patch('task2.solution.get_soup')
    def test_count_animals_single_page(self, mock_get_soup):
        # Подделываем HTML-страницу
        html = """
        <div class="mw-category-group">
            <ul>
                <li><a href="/wiki/Акула" title="Акула">Акула</a></li>
                <li><a href="/wiki/Барсук" title="Барсук">Барсук</a></li>
                <li><a href="/wiki/Аист" title="Аист">Аист</a></li>
            </ul>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        mock_get_soup.return_value = soup

        result = count_animals("https://example.com")
        expected = defaultdict(int, {'А': 2, 'Б': 1})
        self.assertEqual(dict(result), dict(expected))

    @patch('task2.solution.get_soup')
    def test_count_animals_with_pagination(self, mock_get_soup):
        # Первая страница
        html1 = """
        <div class="mw-category-group">
            <ul>
                <li><a href="/wiki/Акула" title="Акула">Акула</a></li>
            </ul>
        </div>
        <a href="/next" title="следующая страница">следующая страница</a>
        """
        # Вторая страница
        html2 = """
        <div class="mw-category-group">
            <ul>
                <li><a href="/wiki/Барсук" title="Барсук">Барсук</a></li>
            </ul>
        </div>
        """
        soup1 = BeautifulSoup(html1, "html.parser")
        soup2 = BeautifulSoup(html2, "html.parser")

        mock_get_soup.side_effect = [soup1, soup2]

        result = count_animals("https://example.com")
        expected = defaultdict(int, {'А': 1, 'Б': 1})
        self.assertEqual(dict(result), dict(expected))


if __name__ == '__main__':
    unittest.main()
