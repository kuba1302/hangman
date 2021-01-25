import scrapy
from ..items import PriceComparisonItem
from datetime import date
import logging
import pandas as pd
import unicodedata
from time import sleep

class PriceSpider(scrapy.Spider):
    name = "foczka"
    today = date.today().strftime("%d/%m/%Y")

    start_urls = ['https://www.foczkaalkohole.pl/kategoria-produktu/wodka/']
    base_url = 'https://www.foczkaalkohole.pl/kategoria-produktu/'
    categories = {"url": ["wodka", "wino", "whisky", "likiery", "tequila", "rum", "gin", "koniaki"],
                  "type": ["vodka", "wine", "whisky", "liqueur", "tequila", "rum", "gin", "brandy"],
                  "pages": [5, 6, 4, 2, 1, 1, 1, 1]
                  }
    instance = 0
    page_number = 2

    def parse(self, response):
        items = PriceComparisonItem()
        print("Checking foczkaalkohole...")
        items['store_name'] = 'Foczka Alkohole'
        items['date'] = self.today
        items['category'] = self.categories["type"][self.instance]

        i = 1
        for alcohol in response.xpath("//*[@id='main']/div/ul/li"):
            items['product'] = alcohol.xpath("//*[@id='main']/div/ul/li[{}]/div[2]/a[1]/h3//text()".format(i)).extract()
            price = alcohol.css("bdi::text").extract()
            items['price'] = price
            # if len(price)>0:
            #     price[0] = unicodedata.normalize("NFKD", price[0])
            #     price[0] = price[0].replace("zł", "")
            #     items['price'] = price[0].replace(" ", "")
            # else:
            #     items['price'] = price

            i += 1
            yield items

        next_page = self.base_url + self.categories["url"][self.instance] + "/page/" + str(self.page_number)

        if self.page_number <= int(self.categories['pages'][self.instance]):
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)
        elif self.instance <= 2:
            self.instance += 1
            self.page_number = 2
            next_page = self.base_url + self.categories["url"][self.instance]
            yield response.follow(next_page, callback=self.parse)


class PriceSpider2(scrapy.Spider):
    name = "hurtowo"
    today = date.today().strftime("%d/%m/%Y")
    categories = {"url": ["wodki", "wina", "whiskey", "rumy", "wina-musujace"],
                  "type": ["vodka", "wine", "whisky", "rum", "champagne"],
                  "pages": [5, 8, 4, 1, 2]
                  }
    base_url = 'https://alkoholehurtowo.pl/kategoria-produktu/'
    instance = 0
    max_instance = len(categories['pages'])
    page_number = 2
    start_urls = [
        'https://alkoholehurtowo.pl/kategoria-produktu/rodzaje-alkoholi/wodki/'
    ]

    def parse(self, response):
        items = PriceComparisonItem()
        print("Checking alkoholehurtowo...")
        items['store_name'] = 'Alkohole Hurtowo'
        items['date'] = self.today
        items['category'] = self.categories["type"][self.instance]

        i = 1
        while i <= 9:
            items['product'] = response.xpath('//*[@id="woo-products-wrap"]/ul/li[{}]/div/div[2]/h3/a/text()'.format(i)).extract()
            price = response.xpath('//*[@id="woo-products-wrap"]/ul/li[{}]/div/div[2]/div/div[1]/h4/span/text()'.format(i)).extract()
            items['price'] = price
            # if len(price) > 0:
            #     price[0] = unicodedata.normalize("NFKD", price[0])
            #     price[0] = price[0].replace("zł", "")
            #     items['price'] = price[0].replace(" ", "")
            # else:
            #     items['price'] = price

            i += 1
            yield items

        next_page = self.base_url + self.categories["url"][self.instance] + "/page/" + str(self.page_number)

        if self.page_number <= int(self.categories['pages'][self.instance]):
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)
        elif self.instance < (len(self.categories["pages"]) - 1):
            self.instance += 1
            self.page_number = 2
            next_page = self.base_url + self.categories["url"][self.instance]
            yield response.follow(next_page, callback=self.parse)

class PriceSpider3(scrapy.Spider):

    name = 'amarone'
    base_url = 'http://www.amarone.pl/index.php/'
    today = date.today().strftime("%d/%m/%Y")
    categories = {"url": ["alkohole/wodki", "wina/wina-kolor", "whisky/whisky1", "alkohole/rumy","alkohole/wszystkie-alkohole-3/likiery",
                          "alkohole/wszystkie-alkohole-3/gin", "alkohole/cognac/brandy", "alkohole/cognac/armaniak-2"
                          , "wina/wina-mussujace/wina-musujace"],
                  "type": ["vodka", "wine", "whisky", "rum", "liqueur", "gin", "brandy", "cognac", "champagne"],
                  "pages": [12, 4, 18, 3, 7, 2, 4, 2, 2]
                  }
    page_number = 99
    instance = 0
    max_instance = len(categories['pages'])
    start_urls = [
        'http://www.amarone.pl/index.php/alkohole/wodki'
    ]

    def parse(self, response):
        items = PriceComparisonItem()
        print("Checking amarone...")
        items['store_name'] = 'Amarone'
        items['date'] = self.today
        items['category'] = self.categories["type"][self.instance]
        all_vodkas = response.css("div.spacer")
        for vodka in all_vodkas:
            items['product'] = vodka.css("h2.product-title a::text").extract()
            price = vodka.css("span.PricesalesPrice::text").extract()
            items['price'] = price
            # if len(price) > 0:
            #     price[0] = unicodedata.normalize("NFKD", price[0])
            #     price[0] = price[0].replace("zł", "")
            #     items['price'] = price[0].replace(" ", "")
            # else:
            #     items['price'] = price

            yield items

        next_page = self.base_url + self.categories["url"][self.instance] + "?start=" + str(self.page_number)

        if self.page_number <= int(self.categories['pages'][self.instance]) * 99:
            self.page_number += 99
            yield response.follow(next_page, callback=self.parse)
        elif self.instance < (len(self.categories["pages"]) - 1):
            self.instance += 1
            self.page_number = 2
            next_page = self.base_url + self.categories["url"][self.instance]
            yield response.follow(next_page, callback=self.parse)

class PriceSpider4(scrapy.Spider):#w trakcie

    name = 'zagrosze'
    today = date.today().strftime("%d/%m/%Y")
    page_number = 2
    start_urls = [
        'https://alkoholezagrosze.pl/43-wodki-czyste'
    ]
    categories = {"url": ["19-wodka", "13-wina", "18-whisky-bourbon", "20-rum-cachaca", "24-likiery", "58-brandy", "14-szampany"],
                  "type": ["vodka", "wine", "whisky", "rum", "liqeur", "brandy", "champagne"],
                  "pages": [5, 7, 3, 1, 1, 1, 1]
                  }
    instance = 0
    max_instance = len(categories['pages'])
    base_url = 'https://alkoholezagrosze.pl/'

    def parse(self, response):
        items = PriceComparisonItem()
        print("Checking zagrosze...")
        items['store_name'] = 'Alkohole za grosze'
        items['date'] = self.today
        items['category'] = self.categories["type"][self.instance]
        all_vodkas = response.css("div.border_inside")
        for vodka in all_vodkas:
            items['product'] = vodka.css("a.product-name::text").extract()
            price = vodka.css("span.product-price::text").extract()
            # price[0] = unicodedata.normalize("NFKD", price[0])
            # price[0] = price[0].replace("zł", "")
            # items['price'] = price[0].replace(" ", "")
            items['price'] = price
            yield items

        next_page = self.base_url + self.categories["url"][self.instance] + "?p=" + str(self.page_number)

        if self.page_number <= int(self.categories['pages'][self.instance]):
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)
        elif self.instance < (len(self.categories["pages"]) - 1):
            self.instance += 1
            self.page_number = 2
            next_page = self.base_url + self.categories["url"][self.instance]
            yield response.follow(next_page, callback=self.parse)

class PriceSpider5(scrapy.Spider):

    name = 'alkohol_online'
    page_number = 2
    today = date.today().strftime("%d/%m/%Y")
    start_urls = [
        'https://alkohol-online.pl/17-wodka'
    ]
    categories = {
        "url": ["17-wodka", "34-wytrawne", "21-whisky", "25-rum", "44-likiery", "20-brandy", "31-szampany",  "36-polwytrawne", "37-slodkie", "38-polslodkie", "22-gin", "23-tequila"],
        "type": ["vodka", "wine", "whisky", "rum", "liqeur", "brandy", "champagne", "wine", "wine", "wine" ,"gin", "tequila"],
        "pages": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        }
    #[4, 1, 3, 1, 2, 1, 1, 1, 1, 1, 1, 1]
    instance = 0
    max_instance = len(categories['pages'])
    base_url = 'https://alkohol-online.pl/'


    def parse(self, response):
        sleep(2)
        items = PriceComparisonItem()
        print("Checking alkohol online...")
        items['store_name'] = 'Alkohol online'
        items['date'] = self.today
        items['category'] = self.categories["type"][self.instance]
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
        next_page = self.base_url + self.categories["url"][self.instance] + "#/page-" + str(self.page_number)
        print("next_page:", next_page)
        if self.page_number <= int(self.categories['pages'][self.instance]):
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)
        elif self.instance < (len(self.categories["pages"]) - 1):
            self.instance += 1
            self.page_number = 2
            next_page = self.base_url + self.categories["url"][self.instance]
            yield response.follow(next_page, callback=self.parse)


class PriceSpider6(scrapy.Spider):

    name = 'hurtownia_alkoholi'
    today = date.today().strftime("%d/%m/%Y")
    page_number = 2
    start_urls = [
        'https://hurtowniaalkoholi.pl/products/list/category/W%C3%B3dki'
    ]
    categories = {
        "url": ["Wódki", "Wino/country/Bułgaria/msg/Bułgaria", "Whisky", "Rum", "Likiery", "Brandy", "Szampany+-+wina+musuj%25C4%2585ce",
                "Wino/country/Chile/msg/Chile", "Wino/country/Gruzja/msg/Gruzja", "Wino/country/Polska/msg/Polska", "Gin", "Tequila"],
        "type": ["vodka", "wine", "whisky", "rum", "liqeur", "brandy", "champagne", "wine", "wine", "wine", "gin",
                 "tequila"],
        "pages": [9, 1, 4, 2, 4, 1, 1, 1, 1, 1, 1, 1]
    }
    instance = 0
    max_instance = len(categories['pages'])
    base_url = 'https://hurtowniaalkoholi.pl/products/list/category/'

    def parse(self, response):
        items = PriceComparisonItem()
        print("Checking hurtownia alkoholi...")
        items['store_name'] = 'Hurtownia alkoholi'
        items['date'] = self.today
        items['category'] = self.categories["type"][self.instance]
        all_vodkas = response.css("div.col-md-8")
        for vodka in all_vodkas:
            items['product'] = vodka.css("a.href_fix h4::text").extract()
            price = vodka.css("span.cena-brutto::text").extract()
            items['price'] = price
            # price[0] = unicodedata.normalize("NFKD", price[0])
            # price[0] = price[0].replace("zł", "")
            # items['price'] = price[0].replace(" ", "")

            yield items


        next_page = self.base_url + self.categories["url"][self.instance] + "/page/" + str(self.page_number)

        if self.page_number <= int(self.categories['pages'][self.instance]):
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)
        elif self.instance < (len(self.categories["pages"]) - 1):
            self.instance += 1
            self.page_number = 2
            next_page = self.base_url + self.categories["url"][self.instance]
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
        print("Checking alkohole swiata...")
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
        print("Checking propaganda24...")
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
        print("checking forfiter...")
        items['store_name'] = 'Forfiter'
        items['date'] = self.today

        all_vodkas = response.css("div.product-item-info")
        for vodka in all_vodkas:
            product = vodka.css("a.product-item-link::text").extract()
            items['product'] = product[0].strip()
            price = vodka.css("span.price::text").extract()
            # price[0] = unicodedata.normalize("NFKD", price[0])
            # price[0] = price[0].replace("zł", "")
            # items['price'] = price[0].replace(" ", "")
            items['price'] = price

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
        print("checking smoczajama...")
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
