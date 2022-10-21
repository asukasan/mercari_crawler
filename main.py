from crawler.main import main as crawler_main
from crawler.m_configs import MERCARI_IT_BOOK_URL

def main():     
    crawler_main(main_url=MERCARI_IT_BOOK_URL, quantity=3)


if __name__ == '__main__':
    main()