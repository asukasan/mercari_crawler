from crawler.main import main as crawler_main
from crawler.bargain_item_delete import bargain_item_delete
from crawler.m_configs import MERCARI_IT_BOOK_URL
import schedule, time
from crawler.django_model_setup import d_setup
from crawler.custom_date import get_custom_date
from item_management.models import BargainItem


def mercari_crawl():
    crawler_main(MERCARI_IT_BOOK_URL)

def delete_bargain_model():
    bargain_item_delete(custom_date=1)
    
def main():
    schedule.every(3).minutes.do(mercari_crawl)
    schedule.every(12).hours.do(delete_bargain_model)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()    