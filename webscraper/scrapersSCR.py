from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import webscraper.timerSCR as timerSCR
import webscraper.settingsSCR as settingsSCR
import sys

if __name__ == "__main__":
    print("'scrapersSCR.py' should not be use as external file. To use it run 'setup.py'.")
    sys.exit()


def extract_price_value(data):
    price_val = data

    if ',' in price_val:
        price_val = price_val.replace(',', '.')

    if ' ' in price_val:
        price_val = price_val.replace(' ', '')

    if 'z' in price_val:
        price_val = price_val.replace('z', '')

    if 'ł' in price_val:
        price_val = price_val.replace('ł', '')

    return float(price_val)


class XkomScraper:
    __productUrl = None
    __client = None
    __soup_page = None

    __name_classes = settingsSCR.get_xkom_name_classes()
    __price_classes = settingsSCR.get_xkom_price_classes()

    def set_product_url(self, url_data):
        self.__productUrl = url_data
        self.__set_soup_page()

    def __set_soup_page(self):
        self.__client = urlopen(self.__productUrl)
        html_source = self.__client.read()
        self.__soup_page = soup(html_source, 'html.parser')
        self.__client.close()

    def get_product_name(self):
        product_name = self.__soup_page.find("h1", {"class": self.__name_classes}).string
        return product_name

    def get_product_price(self):
        product_price = self.__soup_page.find("div", {"class": self.__price_classes}).string

        price_value = extract_price_value(product_price)

        return price_value

    def get_final_data(self):
        current_price = self.get_product_price()
        name = self.get_product_name()
        current_date = timerSCR.get_current_datetime()
        return {"currentPrice": current_price, "name": name, "currentDate": current_date}


"""
    FOR TEST PURPOSE ONLY
"""
# x = XkomScraper()
# x.set_product_url('https://www.x-kom.pl/p/469997-notebook-laptop-156-fujitsu-lifebook-a357-i3-6006u-4gb-500-win10p.html')
# name = x.get_product_name()
# price = x.get_product_price()
# print(name)
# print(price)
