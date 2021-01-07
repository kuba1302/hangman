import scrapy
import pandas as pd
from ..items import PriceComparisonItem
from datetime import date


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
    page_number = 2
    start_urls = [
        'http://www.amarone.pl/index.php/alkohole/wodki'
    ]

    def parse(self,response):
        items = PriceComparisonItem()

        all_vodkas = response.css("div.spacer")
        for vodka in all_vodkas:
            items['product'] = vodka.css("div.vm-product-descr-container-0 h2").extract()
            items['price'] = vodka.css("span.PricesalesPrice::text").extract()
            items['store_name'] = 'Amarone'
            items['date'] = self.today



# BLOKI
# //*[@id="bd_results"]/div[6]/div[30]/div[1]/div
# //*[@id="bd_results"]/div[6]/div[30]/div[2]/div
#
# CENA
# //*[@id="productPrice7102"]/div/span[2]
# //*[@id="productPrice7102"]/div/span[2]
# //*[@id="productPrice7099"]/div/span[2]
# //*[@id="productPrice7098"]/div/span[2]
# //*[@id="productPrice7098"]/div/span[2]
# //*[@id="productPrice7096"]/div/span[2]
#response.css("span.PricesalesPrice::text").extract()

# NAZWA
# //*[@id="bd_results"]/div[6]/div[30]/div[1]/div/div[3]/h2/a
# //*[@id="bd_results"]/div[6]/div[30]/div[2]/div/div[3]/h2/a
