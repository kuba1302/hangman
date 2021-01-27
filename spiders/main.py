import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
from price_comparison.price_comparison.spiders.price_spyder import *
import string
from sqlalchemy import create_engine
import mysql.connector

process = CrawlerProcess(settings={
    "FEEDS": {
        "vodka.csv": {"format": "csv"},
    },
})

spiders = [PriceSpider ,PriceSpider2 ,PriceSpider3 ,PriceSpider4,
           PriceSpider5 ,PriceSpider6 ,PriceSpider7, PriceSpider8,
           PriceSpider9, PriceSpider10]

def crawling():
    for spider in spiders:
        process.crawl(spider)
        process.start()

# Put your location of \spiders folder
df = pd.read_csv(r'C:\Users\Admin\Desktop\UW\PYTHON\Projekt\price_comparison\price_comparison\spiders\vodka.csv')
df.dropna()
df = df[~df['price'].isnull()]
df.drop(df.loc[df['price'] == 'price'].index, inplace=True)
df['price'] = df['price'].apply(lambda x: x.replace(",", "."))
df['price'] = df['price'].apply(lambda x: x.replace("zł", ""))
df['price'] = df['price'].apply(lambda x: x.translate({ord(c): None for c in string.whitespace}))
df['price'] = df['price'].astype(str).str.replace(u'\xa0', '')
df['price'] = df['price'].str.extract(r'(\d+.\d+)').astype('float')
df = df.reset_index(drop=True)


def making_tables():
    hostname = "localhost"
    dbname = "price_comparison"
    uname = "admin1"
    pwd = "price_comparison_project"
    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                           .format(host=hostname, db=dbname, user=uname, pw=pwd), echo=True)
    alcohol_names = ["vodka", "wine", "whisky", "liqueur", "tequila", "rum", "gin", "brandy", "cognac", "champagne"]
    alco_list = []
    for name in alcohol_names:
        vars()[name] = df.loc[df['category'] == '{}'.format(name)]
        alco_list.append(vars()[name])

    for i in range(10):
        alco_list[i].to_sql(alcohol_names[i], con = engine, if_exists = 'append')




def selecting_alcohol(category, name, capacity):
    best_price_list = []
    mydb = mysql.connector.connect(
        host="localhost",
        user="admin1",
        password="price_comparison_project",
        database="price_comparison"
    )
    alcohol_names = ["vodka", "wine", "whisky", "liqueur", "tequila", "rum", "gin", "brandy", "cognac", "champagne"]
    if category in alcohol_names:
        my_cursor = mydb.cursor()
        order1 ="SELECT * FROM {} WHERE product LIKE '%{}%' AND product LIKE '%{}%' ORDER BY price".format(category,name,capacity)
        my_cursor.execute(order1)
        for i in my_cursor:
            best_price_list.append(i)
        my_cursor = mydb.cursor()
        order2 = "SELECT * FROM {} WHERE product LIKE '%{}%' AND product LIKE '%{}%' ORDER BY price".format(category, name, (str(int(float(capacity) * 1000))))
        my_cursor.execute(order2)
        for i in my_cursor:
            best_price_list.append(i)
        best_price_list = sorted(best_price_list, key=lambda x: x[-3], reverse=False)
        for i in best_price_list[:5]:
            print(i)
        if len(best_price_list) == 0:
            print("Wooops! \nThere are no {}-s called {} with {} capacity:(".format(category, name, capacity))
    else:
        print("Wrong category!")


selecting_alcohol('vodka', 'zubrowka', '0.5')



# df.to_sql('alcohol', con = engine, if_exists = 'append')



# 
# df.to_sql('users', engine, index=False)


# if __name__ == "__main__":
#     # for spider in spiders:
#     #     process.crawl(spider)
#     # process.start()
#     while True:
#         df = pd.read_csv(r'C:\Users\Admin\Desktop\UW\PYTHON\Projekt\price_comparison\price_comparison\spiders\vodka.csv')
#         df.dropna()
#         df = df[~df['price'].isnull()]
#         df.drop(df.loc[df['price'] == 'price'].index, inplace=True)
#         df['price'] = df['price'].apply(lambda x: x.replace(",", "."))
#         df['price'] = df['price'].apply(lambda x: x.replace("zł", ""))
#         df['price'] = df['price'].apply(lambda x: x.translate({ord(c): None for c in string.whitespace}))
#         df['price'] = df['price'].astype(str).str.replace(u'\xa0', '')
#         df['price'] = df['price'].str.extract(r'(\d+.\d+)').astype('float')
        # checked_vodka = input("What vodka do you want to check?\n")
        # check_df = df.loc[df['product'].str.contains("{}".format(checked_vodka), na=False)]
        # minimum = check_df.loc[check_df['price'] == check_df['price'].min()]
        # print(minimum)
        # if_continue = input("Press Y/y to chose another vodka, press N/n to leave \n")
        # if if_continue.isupper() == "Y":
        #     pass
        # elif if_continue.isupper() == "N":
        #     break


    # df.loc[df['product'].str.containssssssdaa", na=False)]

