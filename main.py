from crawler.main import main as crawler_main
from crawler.m_configs import MERCARI_IT_BOOK_URL, QUANTITY

def main():     
    crawler_main(main_url=MERCARI_IT_BOOK_URL, quantity=QUANTITY)


if __name__ == '__main__':
    main()