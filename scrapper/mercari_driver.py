import urllib.parse
import time
import random
import os
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager



from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from .m_configs import GET_NEXT_BUTTON_SCRIPT,\
                    MERCARI_DEFAULT_URL,\
                    GET_ITEM_NAME, GET_ITEM_PRICE, GET_ITEM_DESCRIPTION, QUANTITY, GET_ITEM_SOLD
                    

exec_file_name =  os.path.basename(__file__)[:-3]





def get_scrapper_driver():
    op = Options()
    op.add_argument("--disable-gpu")
    op.add_argument("--disable-extensions")
    op.add_argument("--proxy-server='direct://'")
    op.add_argument("--proxy-bypass-list=*")
    op.add_argument("--start-maximized")
    op.add_argument('headless')
    # op.add_argument("--headless")
    # op.add_argument('--user-agent=hogehoge')
    #Iniciar navegador habitual (las cookies se pueden utilizar tal cual)
    #driver = webdriver.Chrome(options=op)
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=op)

    return driver

def custom_time_sleep():
    sec = 4 + random.uniform(0.1, 1)
    time.sleep(sec)


class MercariDriver():

    def __init__(self, driver):
        self.driver = driver

    def move_page(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )
        custom_time_sleep()

    def get_items_url(self, url=None, page=1, quantity=QUANTITY):
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
        # Unir rutas relativas con la ruta base
        joined_url_list = []
        for url in url_list:
            absolute_url = urllib.parse.urljoin(MERCARI_DEFAULT_URL, url)
            joined_url_list.append(absolute_url)
        return joined_url_list  

   
    def get_next_button(self):
        next_button = self.driver.execute_script(GET_NEXT_BUTTON_SCRIPT)
        return next_button
    
    def get_name_and_price(self):
        try:
            try:
                sold_exist = self.driver.execute_script(GET_ITEM_SOLD)

            except:
                sold_exist = None

            name = self.driver.execute_script(GET_ITEM_NAME)
            price = self.driver.execute_script(GET_ITEM_PRICE)
            description = self.driver.execute_script(GET_ITEM_DESCRIPTION)


            #print("name: ", name)
            #print("price: ", price)
        except:
            print('No se pudo obtener el nombre y el precio.')
            print(self.driver.current_url)
            print(traceback.print_exc())
            return (None, None, None)   
 
        price = price.replace(",", "")
        price = int(price)
        #check if sold_exist is False
        if sold_exist is None:
            return (name, price, description)
        else:
            return (None, None, None)
