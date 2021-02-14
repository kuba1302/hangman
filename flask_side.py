from flask import Flask
from flask import render_template
app = Flask(__name__)
import mysql.connector
import pandas as pd
from flask import request


def selecting_alcohol(category, name, capacity):
    global df
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
        df = pd.DataFrame(best_price_list, columns=["ID", "CATEGORY", "DATE","PRICE", "NAME", "STORE NAME"] )
        for i in best_price_list[:5]:
            print(i)
        # return(df)
        if len(best_price_list) == 0:
            print("Wooops! \nThere are no {}-s called {} with {} capacity:(".format(category, name, capacity))
    else:
        print("Wrong category!")

@app.route("/", methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        search = request.form['search']
        search = search.split(",")
        print(search, search[0], search[1], search[2])
        selecting_alcohol(search[0], search[1], search[2])
        return render_template('home.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
    else:
        return render_template('home.html')   

if __name__ == "__main__":
    app.run(debug=True)