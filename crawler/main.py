import urllib.parse

from crawler.notification import notify
from .mercari_driver import MercariDriver, get_crawler_driver
from .m_configs import  MERCARI_IT_BOOK_URL, MERCARI_DEFAULT_URL
from .evaluation import get_item_evaluation
from .filter.item_name import have_prohibit_name


def main(main_url=MERCARI_IT_BOOK_URL, quantity=50):
    driver = get_crawler_driver()
    m_crawler = MercariDriver(driver)

    m_crawler.move_page(main_url)
    latest_item_url_list = m_crawler.get_items_url(quantity=quantity)

    for item_url in latest_item_url_list:

        m_crawler.move_page(item_url)
        item_name, item_price, item_description = m_crawler.get_name_and_price()
        if item_name is None or item_price is None or item_description is None:
            continue
        item_name_encode = urllib.parse.quote(item_name)
        search_item_url = main_url + "&keyword=" + item_name_encode

        m_crawler.move_page(search_item_url)
        #average_price, sales_rate, item_quantity = m_crawler.get_items_info()
        #if average_price is None or sales_rate is None or item_quantity is None:
        #    continue
        #item_score, item_profit = get_item_evaluation(item_price, average_price, sales_rate)

        #if item_score == 0:
        #    continue

        
        #if have_prohibit_name(item_name):
        #    continue

        #notify(item_url, item_name, item_score, item_profit, item_price)

        notify(item_url, item_name, item_price, item_description)

    driver.close()
    driver.quit()        
                
        
if __name__ == '__main__':
    main()  