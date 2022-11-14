import re
import requests
import csv
import os
import io
from googletrans import Translator
from .m_configs import PRODUCT_CATEGORY, trans_lang

translator = Translator()


def notify(item_url, name, price, description):
    eur_price = str(round(((price * 0.0068) * 1.5), 2)) + " EUR" 
    
    #example url: https://jp.mercari.com/item/m35776031725
    
    
    #get the item id from the url and use it to get the images
    item_id = item_url.split("/")[-1]
    img_url_1 = "https://static.mercdn.net/item/detail/orig/photos/" + item_id + "_1.jpg"
    img_url_2 = "https://static.mercdn.net/item/detail/orig/photos/" + item_id + "_2.jpg"
    img_url_3 = "https://static.mercdn.net/item/detail/orig/photos/" + item_id + "_3.jpg"
    img_url_4 = "https://static.mercdn.net/item/detail/orig/photos/" + item_id + "_4.jpg"
    img_url_5 = "https://static.mercdn.net/item/detail/orig/photos/" + item_id + "_5.jpg"

    #check if the image exists
    img_1_exists = requests.get(img_url_1).status_code == 200
    img_2_exists = requests.get(img_url_2).status_code == 200
    img_3_exists = requests.get(img_url_3).status_code == 200
    img_4_exists = requests.get(img_url_4).status_code == 200
    img_5_exists = requests.get(img_url_5).status_code == 200


    #concatenate sepparated by commas the images and add a " at the beginning and at the end of each image url if it exists
    img_urls = ""
    if img_1_exists:
        img_urls += img_url_1
    if img_2_exists:
        img_urls += "," +img_url_2
    if img_3_exists:
        img_urls += "," +img_url_3
    if img_4_exists:
        img_urls += "," +img_url_4
    if img_5_exists:
        img_urls += "," +img_url_5

    #get SKU number out of item_id
    item_sku = item_id.replace("m", "")

    
    try:
        #translate from japanese to english
        name = translator.translate(name, dest=trans_lang).text
        description = translator.translate(description, dest=trans_lang).text


        #replace all double quotes with single quotes
        name = name.replace('"', "'")
        description = description.replace('"', "'")
        #remove "#n minutes ago" from description where n is a number (use regex)
        description = re.sub(r'#?\d+ minutes ago', '', description)
        # remove "#n minute before the game" from description where n is a number (use regex)
        description = re.sub(r'#?\d+ minute before the game', '', description)
        # remove "#nn minutes before the game" from description where nn are two numbers (use regex) and # is optional
        description = re.sub(r'#?\d\d+ minutes before the game', '', description)
        # remove "#One minute ago" from description (use regex) and # is optional
        description = re.sub(r'#?One minute ago', '', description)
        # remove "#(word) 1 minute ago" from description (use regex) and # is optional
        description = re.sub(r'#?\w+ 1 minute ago', '', description)
        # remove "#(word) n minutes ago" from description (use regex) and # is optional
        description = re.sub(r'#?\w+ \d+ minutes ago', '', description)
        # remove "#n minutes before switch process" from description where n is a number (use regex) and # is optional
        description = re.sub(r'#?\d+ minutes before switch process', '', description)
        # remove "#n minutes before controller" from description where n is a number (use regex) and # is optional
        description = re.sub(r'#?\d+ minutes before controller', '', description)
        # remove #(word) n seconds ago from description where n is a number (use regex) and # is optional and word is optional
        description = re.sub(r'#?\w+ \d+ seconds ago', '', description)
        # if there are dots in description and they have no space after it, add a space after each dot
        description = re.sub(r'(?<=[^ ])\.(?=[^ ])', '. ', description)
        # remove n hours ago from description where n is a number (use regex)
        description = re.sub(r'\d+ hours ago', '', description)
        #if description has yen currency (¥) replace it with euro currency (€) and multiply the price by 0.65 and then by 1.5
        if "¥" in description:
            description = description.replace("¥", "€")
            #find the price in the description and replace it with the euro price (optional if price digit is before or after the currency and optional space befor or after the currency)
            description = re.sub(r'(\d+)(\s*)(€)', eur_price, description)
            description = re.sub(r'(€)(\s*)(\d+)', eur_price, description)
        if "yen" in description:
            description = description.replace("yen", "€")
            #find the price in the description and replace it with the euro price
            description = re.sub(r'(\d+)(\s*)(€)', eur_price, description)
            description = re.sub(r'(€)(\s*)(\d+)', eur_price, description)







    except:
        pass



    message = """
    url: {url}
    name: {name}
    price: {price}
    description: {description}
    """.format(url=item_url, name=name, item_url = item_url, price = eur_price, description = description)
    send_line_notify(message)
    
    #Create a products list csv file if it doesn't exist and with the rows of the products. If it exists, just add the new product to the csv file.
    #Set the first columns as url, name and price:

    if not os.path.exists('products.csv'):
        with io.open('products.csv', 'w', encoding="utf-8") as f:

            #writer = csv.writer(f, quoting=csv.QUOTE_NONE, quotechar=None, escapechar='\n')
            #prevent img_urls from breaking lines on each comma
            writer = csv.writer(f)
            writer.writerow([
            'Explicit URL',
            'Type',
            'Published',
            'Is featured?',
            'Visibility in catalog',
            'Tax status',
            'In stock?',
            'Backorders allowed?',
            'Sold individually?',
            'Allow customer reviews?',
            'Parent',
            'Name',
            'Regular price',
            'Stock',
            'url',
            'Images',
            'Description',
            'SKU',
            'Categories'])
            #check if the product is already in the csv file
            if not any(item_id in s for s in io.open('products.csv', encoding="utf-8")):
                writer.writerow([
                    item_url,
                    'simple',
                    '1',
                    '0',
                    'visible',
                    'taxable',
                    '1',
                    '0',
                    '0',
                    '1',
                    '',
                    name,
                    eur_price,
                    '',
                    item_url,
                    img_urls,
                    description,
                    item_sku,
                    PRODUCT_CATEGORY
                    ])
            else:
                print("ya existe un producto con esta ID")

    else:
        with io.open('products.csv', 'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            #add "" to each value. example: "simple" instead of simple
            if not any(item_id in s for s in io.open('products.csv', encoding="utf-8")):
                writer.writerow([
                    item_url,
                    'simple',
                    '1',
                    '0',
                    'visible',
                    'taxable',
                    '1',
                    '0',
                    '0',
                    '1',
                    '',
                    name,
                    eur_price,
                    '',
                    item_url,
                    img_urls,
                    description,
                    item_sku,
                    PRODUCT_CATEGORY
                    ])
            else:
                print("ya existe un producto con esta ID")
    






def send_line_notify(notification_message):
    print("notification_message: ", notification_message)
if __name__ == "__main__":
    notify()