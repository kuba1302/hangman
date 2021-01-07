import scrapy
from scrapy.linkextractors import LinkExtractor
import pandas as pd
from ..items import PriceComparisonItem
from scrapy.crawler import CrawlerProcess

searched_item = "żubrówka 0.5"


class GoogleSpider(scrapy.Spider):


    # Number of scraped sites
    i = 0
    name = "google"
    start_urls = [
        'https://www.google.com/search?q=%C5%BCubr%C3%B3wka+0.5'
    ]
    # Prepare empty list and data frame / might change to items later
    # df = pd.DataFrame()
    # link_list = []
    # link_text = []


    def parse(self,response):

        items = PriceComparisonItem()
        xlink = LinkExtractor()
        for link in xlink.extract_links(response):
            # Throw away all google searches etc. and price comparison sites like ceneo.
            if (len(str(link))>220 or searched_item in link.text) and \
                    'ceneo' not in link.text and 'oferteo' not in link.text and \
                    'Zaloguj sie' not in link.text:
                print(self.i,link,"\n")
                items['link'] = link
                items['link_text'] = link.text
                self.i += 1

                yield items
        # Find "next page" button with xpath
        next_page =  "https://www.google.com" + str(response.css("a").xpath("@href")[-5].get())
        # limit number of scraped pages.
        # Switch page.
        if self.i <= 20:
            yield response.follow(next_page, callback=self.parse)

