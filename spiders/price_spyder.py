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

