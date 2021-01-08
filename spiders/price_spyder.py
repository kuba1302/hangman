import scrapy
from ..items import PriceComparisonItem
from datetime import date
import logging
import pandas as pd


# Get clear link
# data = pd.read_csv(r'C:/Users/Admin/Desktop/UW/PYTHON/Projekt/price_comparison/price_comparison/output.csv')
# data['links'] = data['links'].apply(lambda x: x.split("'")[1])


class PriceSpider(scrapy.Spider):
    name = "foczka"
    today = date.today().strftime("%d/%m/%Y")
    page_number = 2
    start_urls = [
        'https://www.foczkaalkohole.pl/kategoria-produktu/wodka/'

    ]

    def parse(self, response):

        items = PriceComparisonItem()
        i = 1
        for vodka in response.xpath("//*[@id='main']/div/ul/li"):
            price = vodka.css("bdi::text").extract()
            product = vodka.xpath("//*[@id='main']/div/ul/li[{}]/div[2]/a[1]/h3//text()".format(i)).extract()
            i += 1

            items['product'] = product
            items['price'] = price
            items['store_name'] = 'Foczka Alkohole'
            items['date'] = self.today
            yield items

        next_page = 'https://www.foczkaalkohole.pl/kategoria-produktu/wodka/page/{}/'.format(self.page_number)

        if self.page_number <= 5:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)


class PriceSpider2(scrapy.Spider):
    name = "hurtowo"
    today = date.today().strftime("%d/%m/%Y")
    page_number = 2
    start_urls = [
        'https://alkoholehurtowo.pl/kategoria-produktu/rodzaje-alkoholi/wodki/'

    ]

    def parse(self, response):
        items = PriceComparisonItem()
        i = 1
        while i <= 9:
            items['price'] = response.xpath(
                '//*[@id="woo-products-wrap"]/ul/li[{}]/div/div[2]/div/div[1]/h4/span/text()'.format(i)).extract()
            items['product'] = response.xpath('//*[@id="woo-products-wrap"]/ul/li[{}]/div/div[2]/h3/a/text()'.format(i)).extract()
            items['store_name'] = 'Alkohole Hurtowo'
            items['date'] = self.today
            i += 1
            yield items

        next_page = 'https://alkoholehurtowo.pl/kategoria-produktu/rodzaje-alkoholi/wodki/page/{}/'.format(self.page_number)

        if self.page_number <= 5:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)


class PriceSpider3(scrapy.Spider):

    name = 'amarone'
    today = date.today().strftime("%d/%m/%Y")
    page_number = 99
    start_urls = [
        'http://www.amarone.pl/index.php/alkohole/wodki'
    ]

    def parse(self, response):
        items = PriceComparisonItem()

        all_vodkas = response.css("div.spacer")
        for vodka in all_vodkas:
            items['product'] = vodka.css("div.vm-product-descr-container-0 h2").extract()
            items['price'] = vodka.css("span.PricesalesPrice::text").extract()
            items['store_name'] = 'Amarone'
            items['date'] = self.today

        next_page = "http://www.amarone.pl/index.php/alkohole/wodki?start={}".format(self.page_number)

        if self.page_number <= 891:
            self.page_number += 99
            yield response.follow(next_page, callback=self.parse)


class PriceSpider4(scrapy.Spider):

    name = 'zagrosze'
    today = date.today().strftime("%d/%m/%Y")
    page_number = 2
    start_urls = [
        'https://alkoholezagrosze.pl/43-wodki-czyste'
    ]

    def parse(self, response):
        items = PriceComparisonItem()

        items['store_name'] = 'Alkohole za grosze'
        items['date'] = self.today

        all_vodkas = response.css("div.border_inside")
        for vodka in all_vodkas:
            items['product'] = vodka.css("a.product-name::text").extract()
            items['price'] = vodka.css("span.product-price::text").extract()

            yield items

        next_page = 'https://alkoholezagrosze.pl/43-wodki-czyste?p=' + str(self.page_number)

        if self.page_number <= 5:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)


class PriceSpider5(scrapy.Spider):

    name = 'alkohol_online'
    today = date.today().strftime("%d/%m/%Y")
    start_urls = [
        'https://alkohol-online.pl/18-czysta-biala?id_category=18&n=110'
    ]

    def parse(self, response):
        items = PriceComparisonItem()

        items['store_name'] = 'Alkohol online'
        items['date'] = self.today

        all_vodkas = response.css("div.product-container")
        for vodka in all_vodkas:
            product = vodka.css("span.product-name a::text").extract()
            price = vodka.css("span.product-price::text").extract()

            product[0] = product[0].strip()
            price[0] = price[0].strip()
            del price[1]

            items['product'] = product
            items['price'] = price

            yield items


class PriceSpider6(scrapy.Spider):

    name = 'hurtownia_alkoholi'
    today = date.today().strftime("%d/%m/%Y")
    page_number = 2
    start_urls = [
        'https://hurtowniaalkoholi.pl/products/list/category/W%C3%B3dki'
    ]

    def parse(self, response):
        items = PriceComparisonItem()

        items['store_name'] = 'Hurtownia alkoholi'
        items['date'] = self.today

        all_vodkas = response.css("div.col-md-8")
        for vodka in all_vodkas:
            items['product'] = vodka.css("a.href_fix h4::text").extract()
            items['price'] = vodka.css("span.cena-brutto::text").extract()

            yield items

        next_page = 'https://hurtowniaalkoholi.pl/products/list/category/W%C3%B3dki/page/' + str(self.page_number)

        if self.page_number <= 9:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)
