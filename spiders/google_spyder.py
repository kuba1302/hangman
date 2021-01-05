import scrapy
from scrapy.linkextractors import LinkExtractor
import pandas as pd

searched_item = "żubrówka 0.5"


class GoogleSpider(scrapy.Spider):


    name = "google"
    start_urls = [
        'https://www.google.com/search?q=%C5%BCubr%C3%B3wka+0.5'
    ]
    # Prepare empty list and data frame / might change to items later
    df = pd.DataFrame()
    link_list = []
    link_text = []


    def parse(self,response):
        xlink = LinkExtractor()
        for link in xlink.extract_links(response):
            # Throw away all google searches etc. and price comparison sites like ceneo.
            if (len(str(link))>220 or searched_item in link.text) and \
                    'ceneo' not in link.text and 'oferteo' not in link.text and \
                    'Zaloguj sie' not in link.text:
                print(len(str(link)),link.text,link,"\n")
                self.link_list.append(link)
                self.link_text.append(link.text)
        # Find "next page" button with xpath
        next_page =  "https://www.google.com" + str(response.css("a").xpath("@href")[-5].get())
        # limit number of scraped pages.
        page_limit = 5
        page_number = 1

        # Switch page.
        if page_number <= page_limit:
            yield response.follow(next_page, callback=self.parse)
            page_number += 1
        # Put list data into a DataFrame and import it to csv file.
        self.df['links'] = self.link_list
        self.df['link_text'] = self.link_text
        self.df.to_csv('output.csv')
