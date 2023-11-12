from crawler.main import main as crawler_main
from crawler.m_configs import MERCARI_IT_BOOK_URL
from logger.utils.custom_logger import Logger
import os
# ログの設定
exec_file_name =  os.path.basename(__file__)[:-3]
log_obj = Logger()
log_obj.read_conf_file('logger/conf/conf.json')
logger = log_obj.get_logger(exec_file_name)

def main():
    try:
        crawler_main(main_url=MERCARI_IT_BOOK_URL, quantity=20, category_id=674, db_name="mercari_db")
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    main()