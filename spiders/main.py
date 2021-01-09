import scrapy
from scrapy.crawler import CrawlerProcess

from price_comparison.price_comparison.spiders.price_spyder import *




process = CrawlerProcess(settings={
    "FEEDS": {
        "vodka.csv": {"format": "csv"},
    },
})

spiders = [PriceSpider,PriceSpider2,PriceSpider3,PriceSpider4,PriceSpider5,PriceSpider6,PriceSpider7,PriceSpider8,PriceSpider9,PriceSpider10]

if __name__ == "__main__":
    for spider in spiders:
        process.crawl(spider)
    process.start()
    df = pd.read_csv(r'C:\Users\Admin\Desktop\UW\PYTHON\Projekt\price_comparison\price_comparison\spiders\vodka.csv')
    df.dropna()
    df = df[~df['price'].isnull()]
    df.drop(df.loc[df['price'] == 'price'].index, inplace=True)
    df['price'] = df['price'].apply(lambda x: x.replace(",", "."))
    df['price'] = df['price'].str.extract(r'(\d+.\d+)').astype('float')
    # df.loc[df['product'].str.contains("Beluga", na=False)]

