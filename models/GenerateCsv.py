import csv
import os
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options


class GenerateCsv:
    options = Options()
    options.headless = True
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ('
                             'KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}

    url = 'https://www.extra.com.br/PetShop/cachorro/AlimentosRacoescaes/?Filtro=C2294_C2295_C2301'
    page = url

    def _clean_tags_and_style(self, html):
        for script in html(["script", "style"]):  # remove all javascript and stylesheet code
            script.extract()
        text = html.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        return text

    def _format_price(self, html_value):
        splited = html_value.split(',')
        numeric = ''.join([digit for digit in splited[0] if digit.isdecimal()])
        decimal = ''.join([digit for digit in splited[1] if digit.isdecimal()])
        numeric += '.' + decimal
        return numeric

    def get_pages(self, pages):
        products_list = []
        for i in range(1, pages + 1):
            request = requests.get(self.page, headers=self.HEADERS)
            soup = BeautifulSoup(request.content, 'html.parser')

            product_list_container = soup.find("ul", {"class": "vitrineProdutos"})

            products_list.extend([x for x in product_list_container.find_all('li')])

            self.page = self.url + '&paginaAtual={}'.format(i + 1)


        return self._create_csv(products_list, 'data_{}_pages.csv'.format(pages))

    def _get_description(self, link):
        request = requests.get(link, headers=self.HEADERS)
        page_soup = BeautifulSoup(request.content, 'html.parser')
        result = page_soup.find('div', {'id', 'descricao'})
        return self._clean_tags_and_style(result)

    def _create_csv(self, products_list, filename):
        filepath = os.path.join('output', filename)
        with open(filepath, mode='w') as file:
            file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(['id', 'name', 'price', 'description'])
            for key, product in enumerate(products_list):
                tag_a = product.find('a', {'class', 'link'})
                name = tag_a['title']
                price = self._format_price(product.find('span', {'class', 'price'}).text)
                description = self._get_description(tag_a['href'])
                file_writer.writerow([key + 1, name, price, description])

        return filepath, filename
