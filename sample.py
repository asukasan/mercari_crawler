from crawler.main import main as crawler_main
from crawler.m_configs import MERCARI_IT_BOOK_URL
import schedule, time
from crawler.django_model_setup import d_setup
from crawler.custom_date import get_custom_date

def main():
    crawler_main(main_url=MERCARI_IT_BOOK_URL, quantity=20, category_id=674, db_name="mercari_db")


if __name__ == '__main__':
    main()