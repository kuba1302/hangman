import scrapy
import pandas as pd
from ..items import PriceComparisonItem


# Get clear link
# data = pd.read_csv(r'C:/Users/Admin/Desktop/UW/PYTHON/Projekt/price_comparison/price_comparison/output.csv')
# data['links'] = data['links'].apply(lambda x: x.split("'")[1])


class PriceSpider(scrapy.Spider):
    name = "foczka"
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
            items['store_name'] = 'foczkaalkohole'
            yield items

        next_page = response.xpath("//*[@id='main']/div/nav[2]/ul/li[6]/a").attrib['href']

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


class PriceSpider2(scrapy.Spider):
    name = "hurtowo"
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
            items['store_name'] = 'alkoholehurtowo'
            i += 1
            yield items


        next_page = 'https://alkoholehurtowo.pl/kategoria-produktu/rodzaje-alkoholi/wodki/page/{}/'.format(self.page_number)

        if self.page_number <= 5:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)

# //*[@id="woo-products-wrap"]/ul/li[1]
# //*[@id="woo-products-wrap"]/ul/li[2]
#
# NAZWA
# //*[@id="woo-products-wrap"]/ul/li[1]/div/div[2]/h3/a
# //*[@id="woo-products-wrap"]/ul/li[2]/div/div[2]/h3/a
# //*[@id="woo-products-wrap"]/ul/li[1]/div/div[2]/h3/a
#
#
# CENA
# //*[@id="woo-products-wrap"]/ul/li[1]/div/div[2]/div/div[1]/h4/span
# //*[@id="woo-products-wrap"]/ul/li[2]/div/div[2]/div/div[1]/h4/span

#
# while True:
#        try:
#            items['price'] = response.xpath('//*[@id="woo-products-wrap"]/ul/li[{}]/div/div[2]/div/div[1]/h4/span/text()'.format(i)).extract()
#            items['product'] = response.xpath('//*[@id="woo-products-wrap"]/ul/li[{}]/div/div[2]/h3/a/text()'.format(i)).extract()
#            i += 1
#
#            yield items
#        except:
#            return False
#            break
