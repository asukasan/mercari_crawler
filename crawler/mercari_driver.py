import urllib.parse
import time
import re
import random
import os
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from logger.utils.custom_logger import Logger
from .m_configs import GET_NEXT_BUTTON_SCRIPT,\
                    ITEM_PRICE_SCRIPT, GET_ITEM_QUANTITY_SCRIPT,\
                    GET_SALES_RATE_SCRIPT, MERCARI_DEFAULT_URL,\
                    GET_ITEM_NAME, GET_ITEM_PRICE, GET_ITEM_DESCRIPTION
                    
# ログの設定
exec_file_name =  os.path.basename(__file__)[:-3]
log_obj = Logger()
log_obj.read_conf_file('logger/conf/conf.json')
logger = log_obj.get_logger(exec_file_name)





def get_crawler_driver():
    op = Options()
    op.add_argument("--disable-gpu")
    op.add_argument("--disable-extensions")
    op.add_argument("--proxy-server='direct://'")
    op.add_argument("--proxy-bypass-list=*")
    op.add_argument("--start-maximized")
    # op.add_argument("--headless")
    # op.add_argument('--user-agent=hogehoge')
    #いつも使っているブラウザを起動する(クッキーをそのまま使用できる)
    driver = webdriver.Chrome(options=op)
    return driver

def custom_time_sleep():
    sec = 4 + random.uniform(0.1, 1)
    time.sleep(sec)


class MercariDriver():
    """
    最終的にはitem単体とitems_infoを比較して利益がどのくらい出せるかを知りたい
    情報を抽出
    
    """
    def __init__(self, driver):
        self.driver = driver

    def move_page(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )
        custom_time_sleep()

    def get_items_url(self, url=None, page=1, quantity=50):
        url_list = []
        if url is not None:
            self.move_page(url)
        for p in reversed(range(page)):
            soup = BeautifulSoup(self.driver.page_source, features="html.parser")
            li_list = soup.find_all("li", attrs={'data-testid': 'item-cell'})[:quantity]
            for li in li_list:
                url_list.append(li.a['href'])
            
            if p != 0:
                next = self.get_next_button()
                if next is not None:
                    next.click()
                    custom_time_sleep()
        url_list =  self.join_mercari_url(url_list)
        return url_list

    def join_mercari_url(self, url_list):
        # メルカリのサイトは相対パスでリンクをとっているために、joinする
        joined_url_list = []
        for url in url_list:
            absolute_url = urllib.parse.urljoin(MERCARI_DEFAULT_URL, url)
            joined_url_list.append(absolute_url)
        return joined_url_list  

    def get_items_sold_average_price(self, url=None, page=1):
        sold_price_list = []
        if url is not None:
            self.move_page(url)        
        for p in reversed(range(page)):
            try:
                price_list = self.driver.execute_script(ITEM_PRICE_SCRIPT)
                price_list = self.arrange_price_list(price_list)
                sold_price_list += price_list
            except:
                logger.error('priceを取得できませんでした。')
                logger.error(self.driver.current_url)
                logger.error(traceback.print_exc())
                return None
            if p != 0:
                next = self.get_next_button()
                if next is not None:
                    next.click()
                    custom_time_sleep()
        if len(sold_price_list) == 0:
            return 0            
        average_price = int(sum(sold_price_list) / len(sold_price_list))            
        return average_price

    def arrange_price_list(self, price_list):
        # 価格の中のカンマをなくす(4,700→4700)
        arrange_price_list = []
        for price in price_list:
            after_price = price.replace(",", "")
            after_price = int(after_price)
            arrange_price_list.append(after_price)
        return arrange_price_list 

    def get_sales_rate(self, url=None, page=1):
        if url is not None:
            self.move_page(url)
        sales_rate_list = []
        for p in reversed(range(page)):
            try:
                s_rate = self.driver.execute_script(GET_SALES_RATE_SCRIPT)
            except:
                logger.error('sales_rateを取得できませんでした。')
                logger.error(self.driver.current_url)
                logger.error(traceback.print_exc())
                return None
            sales_rate_list.append(s_rate)
            if p != 0:
                next = self.get_next_button()
                if next is not None:
                    next.click()
                    custom_time_sleep()
        sales_rate = int(sum(sales_rate_list) / len(sales_rate_list))
        return sales_rate

    def get_item_quantity(self, url=None):
        if url is not None:
            self.move_page(url) 
        try:
            item_quantity_text = self.driver.execute_script(GET_ITEM_QUANTITY_SCRIPT)
        except:
            logger.error("item_quantityを取得できませんでした。")
            logger.error(self.driver.current_url)
            logger.error(traceback.print_exc())
            return None
        if item_quantity_text is None:
            return None    
        item_quantity_blank_position = re.search("件", item_quantity_text)
        try:
            item_quantity = item_quantity_text[:item_quantity_blank_position.start()] 
        except:
            logger.error("item_quantityを取得できませんでした。")
            logger.error(self.driver.current_url)
            logger.error(traceback.print_exc())
            return None      
        if item_quantity == '999+':
            item_quantity = 999
        else:
            item_quantity = int(item_quantity)     
        return item_quantity

    def get_items_info(self, url=None, page=1):
        average_price_list = []
        sales_rate_list = []
        item_quantity_list = []
        if url is not None:
            self.move_page(url)
        for p in reversed(range(page)):
            #Noneだった時の処理

            price = self.get_items_sold_average_price()
            rate = self.get_sales_rate()
            quantity = self.get_item_quantity()
            

            if (price is None) or (rate is None) or (quantity is None):
                return None, None, None

            average_price_list.append(price)
            sales_rate_list.append(rate)
            item_quantity_list.append(quantity)

            if p != 0:
                next_button = self.get_next_button()
                if next_button is not None:
                    next_button.click()
                else:
                    break

        average_price = int(sum(average_price_list) / len(average_price_list))
        sales_rate = int(sum(sales_rate_list) / len(sales_rate_list))
        item_quantity = int(sum(item_quantity_list) / len(item_quantity_list))
                
        return average_price, sales_rate, item_quantity

    def get_next_button(self):
        next_button = self.driver.execute_script(GET_NEXT_BUTTON_SCRIPT)
        return next_button
    
    def get_name_and_price(self):
        try:
            name = self.driver.execute_script(GET_ITEM_NAME)
            price = self.driver.execute_script(GET_ITEM_PRICE)
            description = self.driver.execute_script(GET_ITEM_DESCRIPTION)


            #print("name: ", name)
            #print("price: ", price)
        except:
            logger.error('nameとpriceを取得できませんでした。')
            logger.error(self.driver.current_url)
            logger.error(traceback.print_exc())
            return (None, None)   
 
        price = price.replace(",", "")
        price = int(price)
        return (name, price, description)
