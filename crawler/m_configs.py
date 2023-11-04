GET_NEXT_BUTTON_SCRIPT = "return document.querySelector('[data-testid=pagination-next-button] > button')"

MERCARI_IT_BOOK_URL = "https://jp.mercari.com/search?category_id=674&t1_category_id=5&t2_category_id=72&t3_category_id=674" 

MERCARI_DEFAULT_URL = "https://jp.mercari.com"

GET_ITEM_QUANTITY_SCRIPT = """
let items = document.querySelectorAll("#item-grid > ul > li");
return items.length;
"""

GET_ITEM_NAME = "return document.querySelector('#item-info > section:nth-child(1) > div.mer-spacing-b-12 > div > div > h1').textContent"

GET_ITEM_PRICE = "return document.querySelector('#item-info > section:nth-child(1) > section:nth-child(2) > div > div > span:nth-child(2)').textContent"

MERCARI_POSTAGE = 175

MERCARI_COMMISSION_RATE = 0.1

ITEM_PRICE_SCRIPT = r"""
let pricesList = [];  // 価格を格納するためのリスト

// セレクタを使用してulの中のli要素を取得
let items = document.querySelectorAll("#item-grid > ul > li");

// 各li要素に対してループを実行
for (let item of items) {
    // 各li要素の中の価格を指定するセレクタを使用して取得
    let priceElement = item.querySelector("div > a > div > figure > div:nth-of-type(3) > div:nth-of-type(2)");
    
    // 売り切れの場合priceElementはNoneなので飛ばす
    if (priceElement !== null){
        price = priceElement.querySelector("span > span:nth-of-type(2)");
        pricesList.push(price.textContent.trim());
    }
}

// リストを返却
return pricesList;
"""

GET_SALES_RATE_SCRIPT = r"""
let pricesList = [];  // 価格を格納するためのリスト

// セレクタを使用してulの中のli要素を取得
let items = document.querySelectorAll("#item-grid > ul > li");
var item_sold_count = 0
// 各li要素に対してループを実行
for (let item of items) {
    // 各li要素の中の価格を指定するセレクタを使用して取得
    let priceElement = item.querySelector("div > a > div > figure > div:nth-of-type(3) > div:nth-of-type(2)");
    
    // 売り切れの場合priceElementはNoneなので飛ばす
    if (priceElement !== null){
        item_sold_count++;
    }
}
var sales_rate = Math.round((item_sold_count / items.length) * 100);
// リストを返却
return sales_rate;

"""

