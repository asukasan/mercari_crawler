import time
import urllib.parse
from .mercari_driver import MercariDriver, get_crawler_driver
from .m_configs import  MERCARI_IT_BOOK_URL, MERCARI_DEFAULT_URL
from .evaluation import get_item_evaluation

def main(main_url=MERCARI_IT_BOOK_URL, quantity=50, category_id=674, db_name="mercari_db"):
    driver = get_crawler_driver()
    m_crawler = MercariDriver(driver)
    url = "https://jp.mercari.com/search?category_id=674&t1_category_id=5&t2_category_id=72&t3_category_id=674&keyword=%E5%88%9D%E3%82%81%E3%81%A6%E3%81%A7%E3%82%82%E3%81%99%E3%81%90%E6%8F%8F%E3%81%91%E3%82%8B%21Photoshop%E3%82%B9%E3%83%BC%E3%83%91%E3%83%BC%E3%83%86%E3%82%AF%E3%83%8B%E3%83%83%E3%82%AF"
    m_crawler.move_page(url)
    items_info = m_crawler.get_items_info()
    print(items_info)
    print(driver.current_url)







if __name__ == '__main__':
    main()  