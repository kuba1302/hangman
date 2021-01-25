import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
from price_comparison.price_comparison.spiders.price_spyder import *




process = CrawlerProcess(settings={
    "FEEDS": {
    },
})

spiders = [PriceSpider ,PriceSpider2 ,PriceSpider3 ,PriceSpider4,
           PriceSpider5 ,PriceSpider6 ,PriceSpider7, PriceSpider8,
           PriceSpider9, PriceSpider10]

if __name__ == "__main__":
    for spider in spiders:
        process.crawl(spider)
    process.start()
    while True:
        df = pd.read_csv(r'C:\Users\andrzej.zernaczuk\PycharmProjects\Projekt_Nawaro\price_comparison\price_comparison\price_comparison\spiders\vodka.csv')
        df.dropna()
        df = df[~df['price'].isnull()]
        df.drop(df.loc[df['price'] == 'price'].index, inplace=True)
        df['price'] = df['price'].apply(lambda x: x.replace(",", "."))
        df['price'] = df['price'].str.extract(r'(\d+.\d+)').astype('float')
        checked_vodka = input("What vodka do you want to check?\n")
        check_df = df.loc[df['product'].str.contains("{}".format(checked_vodka), na=False)]
        minimum = check_df.loc[check_df['price'] == check_df['price'].min()]
        print(minimum)
        if_continue = input("Press Y/y to chose another vodka, press N/n to leave \n")
        if if_continue.isupper() == "Y":
            pass
        elif if_continue.isupper() == "N":
            break


    # df.loc[df['product'].str.containssssssdaa", na=False)]

