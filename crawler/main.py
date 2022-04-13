from crawler.evaluations import get_item_evaluation
from .mercari_driver import MercariDriver, get_crawler_driver
from .m_configs import  MERCARI_DEFAULT_URL
import time
import re
import os
import sys
from .django_model_setup import d_setup
from .custom_date import get_custom_date
from .notification import notify
import urllib.parse
d_setup(db_name="mercari_db")
from item_management.models import BargainItem, BookCategory, Item


def main(main_url, quantity=20, category_id=674, db_name="mercari_db"):
    driver = get_crawler_driver()
    m_crawler = MercariDriver(driver)
    m_crawler.move_page(MERCARI_DEFAULT_URL)
    custom_date = get_custom_date()
    latest_item_url_list = m_crawler.get_items_url(main_url,  quantity=quantity)
    new_latest_item_url_list = get_new_latest_item_url_list(latest_item_url_list)


    for item_url in new_latest_item_url_list:
        m_crawler.move_page(item_url)
        item_name, item_price = m_crawler.get_name_and_price()
        if item_name is None:
            print('item_name Error')
            continue
        if item_price is None:
            print('item_price Error')
            continue
        try:
            items_info = Item.objects.get(name = item_name)
        except Item.DoesNotExist:
            items_info = None 
        url_item_name = urllib.parse.quote(item_name)
        keyword = "&keyword=" + url_item_name
        item_info_url = main_url + keyword

        if items_info is not None:
            if items_info.crawl == False:
                continue
            if custom_date >= items_info.last_updated:
                items_crawl_info = m_crawler.get_items_info(item_info_url)  
                if items_crawl_info is None:
                    continue
                items_info.average_price = items_crawl_info["average_price"]
                items_info.sales_rate = items_crawl_info["sales_rate"]
                items_info.item_quantity = items_crawl_info["item_quantity"]
                items_info.save()
            elif items_info.last_updated > custom_date:
                pass
            else:
                print("最終更新日が設定されていません。")

        else:
            items_crawl_info = m_crawler.get_items_info(item_info_url)  
            if items_crawl_info is None:
                continue
            if items_crawl_info["item_quantity"] > 1:
                category = BookCategory.objects.get(book_category_id=category_id)
                Item.objects.create(
                    category = category,
                    name = item_name,
                    average_price = items_crawl_info["average_price"],
                    sales_rate = items_crawl_info["sales_rate"],
                    item_quantity = items_crawl_info["item_quantity"],
                )
                items_info = Item.objects.get(name = item_name)
            else:
                continue
                
        item_evaluation = get_item_evaluation(item_price, items_info.average_price)
        if item_evaluation["score"] >= 8:
            BargainItem.objects.create(
                item = items_info, 
                price = item_price, 
                score = item_evaluation["score"], 
                profit = item_evaluation["profit"],   
            )
            bargain_item_url = "urasekai.net"
            if item_evaluation["score"] == 10 and items_crawl_info["sales_rate"] >= 90:
                notify(bargain_item_url, item_name, item_evaluation["score"], item_evaluation["profit"])
    driver.close()
    driver.quit()

def get_new_latest_item_url_list(url_list):
    arrange_latest_item_url_list = []
    fd = open("crawler/latest_item_url_list.txt", mode='r')
    data = fd.read().splitlines()
    fd.close()
    tmp = False
    for url in url_list:
        for d in data:
            if url == d:
                tmp = True
            else:
                pass
        if tmp:
            break    
        arrange_latest_item_url_list.append(url)    
    arrange_latest_item_url_list = list(map(lambda x: x + "\n", arrange_latest_item_url_list))
    with open("crawler/latest_item_url_list.txt", mode='w') as f:
        f.writelines(arrange_latest_item_url_list)
    return arrange_latest_item_url_list    



if __name__ == '__main__':
    main()    
