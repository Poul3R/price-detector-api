import mysql.connector
from mysql.connector import errorcode
import webscraper.settingsSCR as settingsSCR
import sys

if __name__ == "__main__":
    print("'databaseSCR.py' should not be use as external file. To use it run 'setup.py'.")
    sys.exit()

__db_config = settingsSCR.get_db_config()


def init_db_connection():
    try:
        mydb = mysql.connector.connect(**__db_config)

        return mydb

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Wrong username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not exist")
        else:
            print(err)

        return None


def update_price_current(mydbData, priceData, idData):
    cursor = mydbData.cursor()

    try:
        cursor.execute("UPDATE `core_productmodel` SET `priceCurrent` = %s WHERE `id` = %s" % (priceData, idData))
        mydbData.commit()
        cursor.close()
    except mysql.connector.errorcode as err:
        print(err)


def update_price_highest(mydbData, priceData, idData):
    cursor = mydbData.cursor()

    try:
        cursor.execute("UPDATE `core_productmodel` SET `priceHighest` = %s WHERE `id` = %s" % (priceData, idData))
        mydbData.commit()
        cursor.close()
    except mysql.connector.errorcode as err:
        print(err)


def update_price_lowest(mydbData, priceData, idData):
    cursor = mydbData.cursor()

    try:
        cursor.execute("UPDATE `core_productmodel` SET `priceLowest` = %s WHERE `id` = %s" % (priceData, idData))
        mydbData.commit()
        cursor.close()
    except mysql.connector.errorcode as err:
        print(err)


def update_date_last_checked(mydbData, dateData, idData):
    cursor = mydbData.cursor()

    try:
        cursor.execute('UPDATE `core_productmodel` SET `dateLastChecked` = "%s" WHERE `id` = %s' % (dateData, idData))
        mydbData.commit()
        cursor.close()
    except mysql.connector.errorcode as err:
        print(err)


def update_date_highest(mydbData, dateData, idData):
    cursor = mydbData.cursor()

    try:
        cursor.execute('UPDATE `core_productmodel` SET `dateHighest` = "%s" WHERE `id` = %s' % (dateData, idData))
        mydbData.commit()
        cursor.close()
    except mysql.connector.errorcode as err:
        print(err)


def update_date_lowest(mydbData, dateData, idData):
    cursor = mydbData.cursor()

    try:
        cursor.execute('UPDATE `core_productmodel` SET `dateLowest` = "%s" WHERE `id` = %s' % (dateData, idData))
        mydbData.commit()
        cursor.close()
    except mysql.connector.errorcode as err:
        print(err)


def get_product_list(mydbData):
    query = "SELECT * FROM `core_productmodel`"
    cursor = mydbData.cursor()

    try:
        cursor.execute(query)
        product_list = cursor.fetchall()

        return product_list

    except mysql.connector.errorcode as err:
        print(err)


"""
    FOR TEST PURPOSE ONLY
"""
# db_conn = init_db_connection()
# var1 = 333
# var2 = "2012-10-09 15:40:20.708953"
# id = 1

# update_price_lowest(db_conn, var1, id) --works
# update_price_highest(db_conn, var1, id) --works
# update_price_current(db_conn, var1, id) --works

# update_date_lowest(db_conn, var2, id) --works
# update_date_highest(db_conn, var2, id) --works
# update_date_last_checked(db_conn, var2, id) --works
