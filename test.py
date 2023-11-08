from tests.sale_item_test import main as crawler_main
from crawler.m_configs import MERCARI_IT_BOOK_URL

def main():     
    crawler_main(main_url=MERCARI_IT_BOOK_URL, quantity=20, category_id=674, db_name="mercari_db")


if __name__ == '__main__':
    main()