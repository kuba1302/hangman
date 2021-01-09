import scrapy
from ..items import PriceComparisonItem
from datetime import date
import logging
import pandas as pd
import unicodedata


# Get clear link
# data = pd.read_csv(r'C:/Users/Admin/Desktop/UW/PYTHON/Projekt/price_comparison/price_comparison/wujec_cwel.csv')
# data['links'] = data['links'].apply(lambda x: x.split("'")[1])

# gituwa
class PriceSpider(scrapy.Spider):
    name = "foczka"
    today = date.today().strftime("%d/%m/%Y")
    page_number = 2
    start_urls = [
        'https://www.foczkaalkohole.pl/kategoria-produktu/wodka/'

    ]

    def parse(self, response):
        items = PriceComparisonItem()

        items['store_name'] = 'Foczka Alkohole'
        items['date'] = self.today

        i = 1
        for vodka in response.xpath("//*[@id='main']/div/ul/li"):
            items['product'] = vodka.xpath("//*[@id='main']/div/ul/li[{}]/div[2]/a[1]/h3//text()".format(i)).extract()
            price = vodka.css("bdi::text").extract()
            if len(price)>0:
                price[0] = unicodedata.normalize("NFKD", price[0])
                price[0] = price[0].replace("zł", "")
                items['price'] = price[0].replace(" ", "")
            else:
                items['price'] = price

            i += 1
            yield items

        next_page = 'https://www.foczkaalkohole.pl/kategoria-produktu/wodka/page/{}/'.format(self.page_number)

        if self.page_number <= 5:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)


# gituwa
class PriceSpider2(scrapy.Spider):
    name = "hurtowo"
    today = date.today().strftime("%d/%m/%Y")
    page_number = 2
    start_urls = [
        'https://alkoholehurtowo.pl/kategoria-produktu/rodzaje-alkoholi/wodki/'

    ]

    def parse(self, response):
        items = PriceComparisonItem()

        items['store_name'] = 'Alkohole Hurtowo'
        items['date'] = self.today

        i = 1
        while i <= 9:
            items['product'] = response.xpath('//*[@id="woo-products-wrap"]/ul/li[{}]/div/div[2]/h3/a/text()'.format(i)).extract()
            price = response.xpath('//*[@id="woo-products-wrap"]/ul/li[{}]/div/div[2]/div/div[1]/h4/span/text()'.format(i)).extract()
            if len(price) > 0:
                price[0] = unicodedata.normalize("NFKD", price[0])
                price[0] = price[0].replace("zł", "")
                items['price'] = price[0].replace(" ", "")
            else:
                items['price'] = price

            i += 1
            yield items

        next_page = 'https://alkoholehurtowo.pl/kategoria-produktu/rodzaje-alkoholi/wodki/page/{}/'.format(self.page_number)

        if self.page_number <= 5:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)


# gituwa
class PriceSpider3(scrapy.Spider):

    name = 'amarone'
    today = date.today().strftime("%d/%m/%Y")
    page_number = 99
    start_urls = [
        'http://www.amarone.pl/index.php/alkohole/wodki'
    ]

    def parse(self, response):
        items = PriceComparisonItem()

        items['store_name'] = 'Amarone'
        items['date'] = self.today

        all_vodkas = response.css("div.spacer")
        for vodka in all_vodkas:
            items['product'] = vodka.css("h2.product-title a::text").extract()
            price = vodka.css("span.PricesalesPrice::text").extract()
            if len(price) > 0:
                price[0] = unicodedata.normalize("NFKD", price[0])
                price[0] = price[0].replace("zł", "")
                items['price'] = price[0].replace(" ", "")
            else:
                items['price'] = price

            yield items

        next_page = "http://www.amarone.pl/index.php/alkohole/wodki?start={}".format(self.page_number)

        if self.page_number <= 1089:
            self.page_number += 99
            yield response.follow(next_page, callback=self.parse)


# gituwa
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
            price = vodka.css("span.product-price::text").extract()
            price[0] = unicodedata.normalize("NFKD", price[0])
            price[0] = price[0].replace("zł", "")
            items['price'] = price[0].replace(" ", "")
            yield items

        next_page = 'https://alkoholezagrosze.pl/43-wodki-czyste?p=' + str(self.page_number)

        if self.page_number <= 5:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)


# gituwa
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
            product[0] = product[0].strip()
            price = vodka.css("span.product-price::text").extract()
            price[0] = unicodedata.normalize("NFKD", price[0])
            price[0] = price[0].replace("zł", "")
            price[0] = price[0].strip()
            items['price'] = price[0].replace(" ", "")
            del price[1]

            items['product'] = product
            items['price'] = price

            yield items


# gituwa
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
            price = vodka.css("span.cena-brutto::text").extract()
            price[0] = unicodedata.normalize("NFKD", price[0])
            price[0] = price[0].replace("zł", "")
            items['price'] = price[0].replace(" ", "")

            yield items

        next_page = 'https://hurtowniaalkoholi.pl/products/list/category/W%C3%B3dki/page/' + str(self.page_number)

        if self.page_number <= 9:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)


# gituwa
class PriceSpider7(scrapy.Spider):

    name = 'alkohole_swiata'
    today = date.today().strftime("%d/%m/%Y")
    page_number = 2
    start_urls = [
        'https://www.alkoholeswiata24.pl/listaProduktow.php?vfcca3803ad=1&kat=103'
    ]

    def parse(self, response):
        items = PriceComparisonItem()

        items['store_name'] = 'Alkohole Swiata'
        items['date'] = self.today

        all_vodkas = response.css("div.col-smx-6")
        for vodka in all_vodkas:
            items['product'] = vodka.css("h3.productName a::attr(title)").extract()
            items['price'] = vodka.css("span.price::text").extract()

            yield items

        next_page = 'https://www.alkoholeswiata24.pl/listaProduktow.php?vfcca3803ad=' + str(self.page_number) + '&kat=103'

        if self.page_number <= 29:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)


# gituwa
class PriceSpider8(scrapy.Spider):

    name = 'propaganda'
    today = date.today().strftime("%d/%m/%Y")
    page_number = 2
    start_urls = [
        'https://propaganda24h.pl/pl/c/CZYSTE/27'
    ]

    def parse(self, response):
        items = PriceComparisonItem()

        items['store_name'] = 'Propaganda24'
        items['date'] = self.today

        all_vodkas = response.css("div.product-main-wrap")
        for vodka in all_vodkas:
            items['product'] = vodka.css("span.productname::text").extract()
            price = vodka.css("div.price em::text").extract()
            price[0] = unicodedata.normalize("NFKD", price[0])
            price[0] = price[0].replace("zł", "")
            items['price'] = price[0].replace(" ", "")

            yield items

        next_page = 'https://propaganda24h.pl/pl/c/CZYSTE/27/' + str(self.page_number)

        if self.page_number <= 6:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)


# gituwa
class PriceSpider9(scrapy.Spider):

    name = 'forfiter'
    today = date.today().strftime("%d/%m/%Y")
    page_number = 2
    start_urls = [
        'https://www.forfiterexclusive.pl/wodka/czysta/'
    ]

    def parse(self, response):
        items = PriceComparisonItem()

        items['store_name'] = 'Forfiter'
        items['date'] = self.today

        all_vodkas = response.css("div.product-item-info")
        for vodka in all_vodkas:
            product = vodka.css("a.product-item-link::text").extract()
            items['product'] = product[0].strip()
            price = vodka.css("span.price::text").extract()
            price[0] = unicodedata.normalize("NFKD", price[0])
            price[0] = price[0].replace("zł", "")
            items['price'] = price[0].replace(" ", "")

            yield items

        next_page = 'https://www.forfiterexclusive.pl/wodka/czysta/?p=' + str(self.page_number)

        if self.page_number <= 17:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)


# gituwa
class PriceSpider10(scrapy.Spider):

    name = 'smaczajama'
    today = date.today().strftime("%d/%m/%Y")
    page_number = 2
    start_urls = [
        'https://smaczajama.pl/pl/c/Wodka/92'
    ]

    def parse(self, response):
        items = PriceComparisonItem()

        items['store_name'] = 'Smacza jama'
        items['date'] = self.today

        all_vodkas = response.css("div.product-inner-wrap")
        for vodka in all_vodkas:
            product = vodka.css("span.productname::text").extract()
            items['product'] = product[0].strip()
            price = vodka.css("div.price em::text").extract()
            price[0] = unicodedata.normalize("NFKD", price[0])
            price[0] = price[0].replace("zł", "")
            items['price'] = price[0].replace(" ", "")

            yield items

        next_page = 'https://smaczajama.pl/pl/c/Wodka/92/' + str(self.page_number)

        if self.page_number <= 20:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)
