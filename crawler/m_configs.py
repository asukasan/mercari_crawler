GET_NEXT_BUTTON_SCRIPT = "return document.querySelector('[data-testid=pagination-next-button] > button')"

MERCARI_IT_BOOK_URL = "https://jp.mercari.com/search?category_id=674&t1_category_id=5&t2_category_id=72&t3_category_id=674" 

MERCARI_DEFAULT_URL = "https://jp.mercari.com"

GET_ITEM_QUANTITY_SCRIPT = "return document.querySelector('#search-result > div > div > div > mer-text').textContent"

GET_ITEM_NAME = "return document.querySelector('#item-info > section:nth-child(1) > div > mer-heading').shadowRoot.querySelector('div > div > h1').textContent"

GET_ITEM_PRICE = "return document.querySelector('mer-price').shadowRoot.querySelector('span:nth-of-type(2)').textContent"

MERCARI_POSTAGE = 175

MERCARI_COMMISSION_RATE = 0.1

ITEM_PRICE_SCRIPT = r"""item_sold_price_list = [];
        var item_lists =  document.querySelector('#item-grid').querySelectorAll('li > a > mer-item-thumbnail');
        for (let i = 0; i < item_lists.length; i++) {
            item_price = item_lists[i].shadowRoot.querySelector('div > figure > div > mer-price');
            price = item_price.shadowRoot.querySelector('span:nth-of-type(2)').textContent;
            sold_exist = item_lists[i].shadowRoot.querySelector('div > figure > div:nth-of-type(3)');
            if (sold_exist !== null){sold = true}else{sold=false}; 
            if (sold){item_sold_price_list.push(price)};
        }
        return item_sold_price_list;"""

GET_SALES_RATE_SCRIPT = r"""var item_lists =  document.querySelector('#item-grid').querySelectorAll('li > a > mer-item-thumbnail');
var item_sold_count = 0
for (let i = 0; i < item_lists.length; i++) {
            sold_exist = item_lists[i].shadowRoot.querySelector('div > figure > div:nth-of-type(3)');
            if (sold_exist !== null){item_sold_count++}; 
        }
var sales_rate = Math.round((item_sold_count / item_lists.length) * 100);
return sales_rate;
"""

