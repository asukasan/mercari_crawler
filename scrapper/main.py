from scrapper.notification import notify
from .mercari_driver import MercariDriver, get_scrapper_driver
from .m_configs import  MERCARI_IT_BOOK_URL, QUANTITY


def main(main_url=MERCARI_IT_BOOK_URL, quantity=QUANTITY):
    driver = get_scrapper_driver()
    m_scrapper = MercariDriver(driver)

    m_scrapper.move_page(main_url)
    latest_item_url_list = m_scrapper.get_items_url(quantity=quantity)

    for item_url in latest_item_url_list:

        m_scrapper.move_page(item_url)
        item_name, item_price, item_description = m_scrapper.get_name_and_price()
        if item_name is None or item_price is None or item_description is None:
            continue

        notify(item_url, item_name, item_price, item_description)

    driver.close()
    driver.quit()        
                
        
if __name__ == '__main__':
    main()  