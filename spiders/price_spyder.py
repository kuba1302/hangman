import scrapy
from ..items import PriceComparisonItem
from datetime import date
import unicodedata


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
        items['store_name'] = 'Foczka Alkohole'
        items['date'] = self.today
        items['category'] = self.categories["type"][self.instance]

        i = 1
        for alcohol in response.xpath("//*[@id='main']/div/ul/li"):
            items['product'] = alcohol.xpath("//*[@id='main']/div/ul/li[{}]/div[2]/a[1]/h3//text()".format(i)).extract()
            price = alcohol.css("bdi::text").extract()
            items['price'] = price
            i += 1
            yield items

        next_page = self.base_url + self.categories["url"][self.instance] + "/page/" + str(self.page_number)

        if self.page_number <= int(self.categories['pages'][self.instance]):
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)
        elif self.instance < (len(self.categories["pages"]) - 1):
            self.page_number = 2
            self.instance += 1
            next_page = self.base_url + self.categories["url"][self.instance]
            yield response.follow(next_page, callback=self.parse)


class PriceSpider2(scrapy.Spider):

    name = "hurtowo"
    today = date.today().strftime("%d/%m/%Y")
    start_urls = ['https://alkoholehurtowo.pl/kategoria-produktu/rodzaje-alkoholi/wodki/']
    base_url = 'https://alkoholehurtowo.pl/kategoria-produktu/'
    categories = {"url": ["wodki", "wina", "whiskey", "rumy", "wina-musujace"],
                  "type": ["vodka", "wine", "whisky", "rum", "champagne"],
                  "pages": [5, 8, 4, 1, 2]
                  }
    instance = 0
    page_number = 2

    def parse(self, response):
        items = PriceComparisonItem()
        items['store_name'] = 'Alkohole Hurtowo'
        items['date'] = self.today
        items['category'] = self.categories["type"][self.instance]

        i = 1
        while i <= 9:
            items['product'] = response.xpath(
                '//*[@id="woo-products-wrap"]/ul/li[{}]/div/div[2]/h3/a/text()'.format(i)).extract()
            price = response.xpath(
                '//*[@id="woo-products-wrap"]/ul/li[{}]/div/div[2]/div/div[1]/h4/span/text()'.format(i)).extract()
            items['price'] = price
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
    today = date.today().strftime("%d/%m/%Y")
    start_urls = ['http://www.amarone.pl/index.php/alkohole/wodki']
    base_url = 'http://www.amarone.pl/index.php/'
    categories = {"url": ["alkohole/wodki", "wina/wina-kolor", "whisky/whisky1", "alkohole/rumy",
                          "alkohole/wszystkie-alkohole-3/likiery", "alkohole/wszystkie-alkohole-3/gin",
                          "alkohole/cognac/brandy", "alkohole/cognac/armaniak-2", "wina/wina-mussujace/wina-musujace"],
                  "type": ["vodka", "wine", "whisky", "rum", "liqueur", "gin", "brandy", "cognac", "champagne"],
                  "pages": [12, 4, 18, 3, 7, 2, 4, 2, 2]
                  }
    instance = 0
    page_number = 99

    def parse(self, response):
        items = PriceComparisonItem()
        items['store_name'] = 'Amarone'
        items['date'] = self.today
        items['category'] = self.categories["type"][self.instance]
        all_alcohols = response.css("div.spacer")
        for alcohol in all_alcohols:
            items['product'] = alcohol.css("h2.product-title a::text").extract()
            price = alcohol.css("span.PricesalesPrice::text").extract()
            items['price'] = price
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


class PriceSpider4(scrapy.Spider):

    name = 'zagrosze'
    today = date.today().strftime("%d/%m/%Y")
    start_urls = ['https://alkoholezagrosze.pl/43-wodki-czyste']
    base_url = 'https://alkoholezagrosze.pl/'
    categories = {"url": ["19-wodka", "13-wina", "18-whisky-bourbon", "20-rum-cachaca", "24-likiery", "58-brandy",
                          "14-szampany"],
                  "type": ["vodka", "wine", "whisky", "rum", "liqeur", "brandy", "champagne"],
                  "pages": [5, 7, 3, 1, 1, 1, 1]
                  }
    instance = 0
    page_number = 2

    def parse(self, response):
        items = PriceComparisonItem()
        items['store_name'] = 'Alkohole za grosze'
        items['date'] = self.today
        items['category'] = self.categories["type"][self.instance]
        all_alcohols = response.css("div.border_inside")
        for alcohol in all_alcohols:
            items['product'] = alcohol.css("a.product-name::text").extract()
            price = alcohol.css("span.product-price::text").extract()
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
    today = date.today().strftime("%d/%m/%Y")
    start_urls = ['https://alkohol-online.pl/17-wodka']
    base_url = 'https://alkohol-online.pl/'
    categories = {
        "url": ["17-wodka", "34-wytrawne", "21-whisky", "25-rum", "44-likiery", "20-brandy", "31-szampany",
                "36-polwytrawne", "37-slodkie", "38-polslodkie", "22-gin", "23-tequila"],
        "type": ["vodka", "wine", "whisky", "rum", "liqeur", "brandy", "champagne", "wine", "wine", "wine", "gin",
                 "tequila"],
        "pages": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        }
    instance = 0
    page_number = 2

    def parse(self, response):
        items = PriceComparisonItem()
        items['store_name'] = 'Alkohol online'
        items['date'] = self.today
        items['category'] = self.categories["type"][self.instance]

        all_alcohols = response.css("div.product-container")
        for alcohol in all_alcohols:
            product = alcohol.css("span.product-name a::text").extract()
            product[0] = product[0].strip()
            price = alcohol.css("span.product-price::text").extract()
            price[0] = unicodedata.normalize("NFKD", price[0])
            price[0] = price[0].replace("zł", "")
            price[0] = price[0].strip()
            items['price'] = price[0].replace(" ", "")
            del price[1]
            items['product'] = product
            items['price'] = price
            yield items

        next_page = self.base_url + self.categories["url"][self.instance] + "#/page-" + str(self.page_number)

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
    start_urls = ['https://hurtowniaalkoholi.pl/products/list/category/W%C3%B3dki']
    base_url = 'https://hurtowniaalkoholi.pl/products/list/category/'
    categories = {
        "url": ["Wódki", "Wino/country/Bułgaria/msg/Bułgaria", "Whisky", "Rum", "Likiery", "Brandy",
                "Szampany+-+wina+musuj%25C4%2585ce", "Wino/country/Chile/msg/Chile", "Wino/country/Gruzja/msg/Gruzja",
                "Wino/country/Polska/msg/Polska", "Gin", "Tequila"],
        "type": ["vodka", "wine", "whisky", "rum", "liqeur", "brandy", "champagne", "wine", "wine", "wine", "gin",
                 "tequila"],
        "pages": [9, 1, 4, 2, 4, 1, 1, 1, 1, 1, 1, 1]
    }
    instance = 0
    page_number = 2

    def parse(self, response):
        items = PriceComparisonItem()
        items['store_name'] = 'Hurtownia alkoholi'
        items['date'] = self.today
        items['category'] = self.categories["type"][self.instance]
        all_alcohols = response.css("div.col-md-8")
        for alcohol in all_alcohols:
            items['product'] = alcohol.css("a.href_fix h4::text").extract()
            price = alcohol.css("span.cena-brutto::text").extract()
            items['price'] = price
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


class PriceSpider7(scrapy.Spider):

    name = 'alkohole_swiata'
    today = date.today().strftime("%d/%m/%Y")
    start_urls = ['https://www.alkoholeswiata24.pl/listaProduktow.php?vfcca3803ad=1&kat=101']
    base_url = 'https://www.alkoholeswiata24.pl/listaProduktow.php?vfcca3803ad='
    categories = {
        "url": ["101", "98", "93", "72", "91", "85", "68", "b64", "70", "89"],
        "type": ["vodka", "wine", "whisky", "liqueur", "tequila", "rum", "gin", "brandy", "cognac", "champagne"],
        "pages": [60, 58, 57, 12, 3, 17, 5, 8, 5, 5]
        }
    instance = 0
    page_number = 2

    def parse(self, response):
        items = PriceComparisonItem()
        items['store_name'] = 'Alkohole Swiata'
        items['date'] = self.today
        items['category'] = self.categories["type"][self.instance]

        all_alcohols = response.css("div.col-smx-6")
        for alcohol in all_alcohols:
            items['product'] = alcohol.css("h3.productName a::attr(title)").extract()
            items['price'] = alcohol.css("span.price::text").extract()
            yield items

        next_page = self.base_url + str(self.page_number) + '&kat=' + self.categories["url"][self.instance]

        if self.page_number <= int(self.categories['pages'][self.instance]):
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)
        elif self.instance < (len(self.categories["pages"]) - 1):
            self.page_number = 2
            self.instance += 1
            next_page = self.base_url + '1&kat=' + self.categories["url"][self.instance]
            yield response.follow(next_page, callback=self.parse)


class PriceSpider8(scrapy.Spider):

    name = 'propaganda'
    today = date.today().strftime("%d/%m/%Y")
    start_urls = ['https://propaganda24h.pl/pl/c/WODKI/4']
    base_url = 'https://propaganda24h.pl/pl/c/'
    categories = {
        "url": ["WODKI/4", "WINA/3", "WHISKY-BOURBON/5", "LIKIERY-NALEWKI/6", "TEQUILA/15", "RUM/14", "GIN/13",
                "BRANDY/47", "KONIAKI/11", "SZAMPANY/16"],
        "type": ["vodka", "wine", "whisky", "liqueur", "tequila", "rum", "gin", "brandy",
                 "brandy", "champagne"],
        "pages": [9, 6, 15, 5, 2, 5, 2, 1, 2, 3]
    }
    instance = 0
    page_number = 2

    def parse(self, response):
        items = PriceComparisonItem()
        items['store_name'] = 'Propaganda24'
        items['date'] = self.today
        items['category'] = self.categories["type"][self.instance]

        all_alcohols = response.css("div.product-main-wrap")
        for alcohol in all_alcohols:
            items['product'] = alcohol.css("span.productname::text").extract()
            price = alcohol.css("div.price em::text").extract()
            price[0] = unicodedata.normalize("NFKD", price[0])
            price[0] = price[0].replace("zł", "")
            items['price'] = price[0].replace(" ", "")
            yield items

        next_page = self.base_url + self.categories["url"][self.instance] + "/" + str(self.page_number)

        if self.page_number <= int(self.categories['pages'][self.instance]):
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)
        elif self.instance < (len(self.categories["pages"]) - 1):
            self.page_number = 2
            self.instance += 1
            next_page = self.base_url + self.categories["url"][self.instance]
            yield response.follow(next_page, callback=self.parse)


class PriceSpider9(scrapy.Spider):

    name = 'forfiter'
    today = date.today().strftime("%d/%m/%Y")
    start_urls = ['https://www.forfiterexclusive.pl/wodka/']
    base_url = 'https://www.forfiterexclusive.pl/'
    categories = {
        "url": ["wodka", "wino", "wino-musujace", "whisky", "likier", "tequila", "rum", "gin", "brandy",
                "koniak", "szampan"],
        "type": ["vodka", "wine", "champagne", "whisky", "liqueur", "tequila", "rum", "gin", "brandy",
                 "cognac", "champagne"],
        "pages": [27, 25, 6, 34, 17, 5, 12, 10, 6, 8, 7]
    }
    instance = 0
    page_number = 2

    def parse(self, response):
        items = PriceComparisonItem()
        items['store_name'] = 'Forfiter'
        items['date'] = self.today
        items['category'] = self.categories["type"][self.instance]

        all_alcohols = response.css("div.product-item-info.type1")
        for alcohol in all_alcohols:
            product = alcohol.css("a.product-item-link::text").extract()
            items['product'] = product[0].strip()
            price = alcohol.css("span.price::text").extract()
            items['price'] = price
            yield items

        next_page = self.base_url + self.categories["url"][self.instance] + '/?p=' + str(self.page_number)

        if self.page_number <= int(self.categories['pages'][self.instance]):
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)
        elif self.instance < (len(self.categories["pages"]) - 1):
            self.page_number = 2
            self.instance += 1
            next_page = self.base_url + self.categories["url"][self.instance]
            yield response.follow(next_page, callback=self.parse)


class PriceSpider10(scrapy.Spider):

    name = 'smaczajama'
    today = date.today().strftime("%d/%m/%Y")
    start_urls = ['https://smaczajama.pl/pl/c/Wodka/92']
    base_url = 'https://smaczajama.pl/pl/c/'
    categories = {
        "url": ["Wodka/92", "Wino/76", "Whisky/90", "Likier/86", "Tequila/98", "Rum/87", "Gin/106", "Brandy/89",
                "Koniak/104", "Szampan/85"],
        "type": ["vodka", "wine", "whisky", "liqueur", "tequila", "rum", "gin", "brandy", "cognac", "champagne"],
        "pages": [21, 55, 38, 14, 3, 11, 5, 4, 5, 6]
        }
    instance = 0
    page_number = 2

    def parse(self, response):
        items = PriceComparisonItem()
        items['store_name'] = 'Smacza jama'
        items['date'] = self.today
        items['category'] = self.categories["type"][self.instance]

        all_alcohols = response.css("div.product-inner-wrap")
        for alcohol in all_alcohols:
            product = alcohol.css("span.productname::text").extract()
            items['product'] = product[0].strip()
            price = alcohol.css("div.price em::text").extract()
            price[0] = unicodedata.normalize("NFKD", price[0])
            price[0] = price[0].replace("zł", "")
            items['price'] = price[0].replace(" ", "")
            yield items

        next_page = self.base_url + self.categories["url"][self.instance] + "/" + str(self.page_number)

        if self.page_number <= int(self.categories['pages'][self.instance]):
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)
        elif self.instance < (len(self.categories["pages"]) - 1):
            self.page_number = 2
            self.instance += 1
            next_page = self.base_url + self.categories["url"][self.instance]
            yield response.follow(next_page, callback=self.parse)
