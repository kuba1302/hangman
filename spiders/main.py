from scrapy.crawler import CrawlerProcess
import pandas as pd
from price_comparison.price_comparison.spiders.price_spyder import *
import string
from sqlalchemy import create_engine
import mysql.connector

process = CrawlerProcess(settings={
    "FEEDS": {
        "alcohol.csv": {"format": "csv"},
    },
})

spiders = [PriceSpider ,PriceSpider2 ,PriceSpider3 ,PriceSpider4,
           PriceSpider5 ,PriceSpider6 ,PriceSpider7, PriceSpider8,
           PriceSpider9, PriceSpider10]

def crawling():
    for spider in spiders:
        process.crawl(spider)
    process.start()

def preparring_data():
    global df
    df = pd.read_csv('alcohol.csv')
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
    # Put details of your database here
    hostname = "localhost"
    dbname = "price_test"
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
    # Put details of your database here
    mydb = mysql.connector.connect(
        host="localhost",
        user="admin1",
        password="price_comparison_project",
        database="price_test"
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



def should_scrap():
    loop = True
    while loop:
        shall_crawl = input("Should I scrap all websites? \n Press Y for yes, N for no ").upper()
        if shall_crawl == "Y":
            crawling()
            loop = False
        elif shall_crawl == "N":
            loop = False
            pass
        else:
            print("Wops!\nYour input was incorrect!")


def should_add_database():
    loop = True
    while loop:
        shall_crawl = input("Should I add scraped data to database? \n Press Y for yes, N for no ").upper()
        if shall_crawl == "Y":
            making_tables()
            loop = False
        elif shall_crawl == "N":
            loop = False
            pass
        else:
            print("Wops!\nYour input was incorrect!")

def find_alcohol():
    alcohol_names = ["vodka", "wine", "whisky", "liqueur", "tequila", "rum", "gin", "brandy", "cognac", "champagne"]
    loop = True
    while loop:
        print("Lets find cheapest version of your alcohol!")
        print("Possible categories:")
        print(', '.join(alcohol_names))
        category1 = input("What category of alcohol do you chose? ")
        name1 = input("What is the name of the alcohol? ")
        capacity1 = input("What is the capacity of the alcohol?\n Write it in liters, for example 0.5 ")
        selecting_alcohol(category1, name1, capacity1)
        shall_crawl = input("Do you want to find another one?\nPress Y for yes, N for no ").upper()
        if shall_crawl == "Y":
            pass
        elif shall_crawl == "N":
            break
        else:
            print("Wops!\nYour input was incorrect!, lets find another alcohol!")


if __name__ == "__main__":
    should_scrap()
    preparring_data()
    should_add_database()
    find_alcohol()
    print("Thank you for using our program!")
