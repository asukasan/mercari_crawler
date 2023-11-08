import time
import urllib.parse

from crawler.notification import notify
from crawler.mercari_driver import MercariDriver, get_crawler_driver
from crawler.m_configs import  MERCARI_IT_BOOK_URL, MERCARI_DEFAULT_URL
from crawler.evaluation import get_item_evaluation
from crawler.filter.item_name import have_prohibit_name
from crawler.django_model_setup import d_setup
d_setup(db_name="mercari_db")
from item_management.models import BargainItem


def main(main_url=MERCARI_IT_BOOK_URL, quantity=20, category_id=674, db_name="mercari_db"):
    driver = get_crawler_driver()
    m_crawler = MercariDriver(driver)

    # セール品のテスト
    sales_item_url = "https://jp.mercari.com/item/m72033784573"
    m_crawler.move_page(sales_item_url)
    is_sales_item = m_crawler.get_is_sales()
    if is_sales_item:
        print("セール品テスト1完了")

    #セール品でないもののテスト
    not_sales_item_url = "https://jp.mercari.com/item/m69957210334"
    m_crawler.move_page(not_sales_item_url)
    is_sales_item = m_crawler.get_is_sales()
    if not is_sales_item:
        print("セール品テスト2完了")

    driver.close()
    driver.quit()        
                
        
if __name__ == '__main__':
    main()  