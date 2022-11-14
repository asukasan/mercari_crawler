from scrapper.main import main as scrapper_main
from scrapper.m_configs import MERCARI_IT_BOOK_URL, QUANTITY

def main():     
    scrapper_main(main_url=MERCARI_IT_BOOK_URL, quantity=QUANTITY)


if __name__ == '__main__':
    main()