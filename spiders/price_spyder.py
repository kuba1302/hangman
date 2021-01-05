import scrapy
import pandas as pd


# Get clear link
data = pd.read_csv(r'C:/Users/Admin/Desktop/UW/PYTHON/Projekt/price_comparison/price_comparison/output.csv')
data['links'] = data['links'].apply(lambda x: x.split("'")[1])




class PriceSpider(scrapy.Spider):
    name = "price"
    start_urls = [
        data['links'][1]

    ]
