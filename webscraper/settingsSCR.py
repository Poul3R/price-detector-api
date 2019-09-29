import sys
import json

if __name__ == "__main__":
    print("'settingsCR.py' should not be use as external file. To use it run 'setup.py'.")
    sys.exit()

"""
    STORE SCRAPER SETTINGS SECTION
    (Change scraper parameters only in this section)
"""

# DATABASE CONFIG
__db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "price-detector-database"
}

# SCRAPER CONFIG (NOT USED YET)
__frequency = 1

# X-kom SCRAPER CLASSES
__h1_name = "wu42cx-5 dsttQT"
__div_price = "y67i6l-4 cFNHuG"

"""
    END OF SETTINGS SECTION
"""


def get_db_config():
    return __db_config


def get_xkom_name_classes():
    return __h1_name


def get_xkom_price_classes():
    return __div_price
