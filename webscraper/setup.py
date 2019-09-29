import webscraper.databaseSCR as db
import webscraper.timerSCR as timerSCR
import webscraper.scrapersSCR as scrapersSCR


class Setup:
    __db_connector = db.init_db_connection()
    __product_list = db.get_product_list(__db_connector)
    __xkom_scraper = scrapersSCR.XkomScraper()

    # counter for test purpose only
    counter = 0

    for product in __product_list:
        scraped_price = None
        current_time = timerSCR.get_current_datetime()

        product_id = product[0]
        url = product[2]
        priceCurrent = product[5]
        priceHighest = product[6]
        priceLowest = product[7]
        dateLastChecked = product[9]
        dateHighest = product[10]
        dateLowest = product[11]
        storeId = product[12]
        is_active = product[13]

        # check if product is active
        if is_active == 0:
            continue

        # choose correct scraper
        if storeId == 1:
            scraper = __xkom_scraper

            scraper.set_product_url(url)
            scraped_price = scraper.get_product_price()
        # add another 'elif' statement if new stores will be added

        # check price value
        if scraped_price > priceCurrent:
            db.update_price_current(__db_connector, scraped_price, product_id)
            db.update_date_last_checked(__db_connector, current_time, product_id)
            print('[debug] price_current & date_last_checked updated')

            if scraped_price > priceHighest:
                db.update_price_highest(__db_connector, scraped_price, product_id)
                db.update_date_highest(__db_connector, current_time, product_id)
                print('[debug] price_highest & date_highest updated')

        elif scraped_price < priceCurrent:
            db.update_price_current(__db_connector, scraped_price, product_id)
            db.update_date_last_checked(__db_connector, current_time, product_id)
            print('[debug] price_current & date_last_checked updated')

            if scraped_price < priceLowest:
                db.update_price_lowest(__db_connector, scraped_price, product_id)
                db.update_date_lowest(__db_connector, current_time, product_id)
                print('[debug] price_lowest & date_lowest updated')

        else:
            db.update_date_last_checked(__db_connector, current_time, product_id)
            print('[debug] price_current & date_last_checked updated')

        # For test purpose only
        counter += 1

    # close database connection
    __db_connector.close()

    # For test purpose only
    print('[debug] Amount of updated products: ' + str(counter))
