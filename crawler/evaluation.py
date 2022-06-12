from .m_configs import MERCARI_POSTAGE, MERCARI_COMMISSION_RATE




def get_item_evaluation(item_price, average_price, sales_rate):
    #ファイルから設定の値を読み込む

    commission = MERCARI_COMMISSION_RATE
    postage = MERCARI_POSTAGE
    profit = average_price - item_price -  (int)(commission * item_price) - postage
    srate_point = sales_rate * 5    

    if profit < 100 or sales_rate < 30:
        score = 0
        return (score, profit)

    point = srate_point + profit

    if point < 100:
        score = 1
    elif point <= 100:
        score = 2     
    elif point <= 200:
        score = 3        
    elif point <= 300:
        score = 4        
    elif point <= 400:
        score = 5        
    elif point <= 500:
        score = 6        
    elif point <= 600:
        score = 7        
    elif point <= 700:
        score = 8        
    elif point <= 800:
        score = 9        
    else:
        score = 10  
    return (score, profit)

if __name__ == "__main__":
    get_item_evaluation()

