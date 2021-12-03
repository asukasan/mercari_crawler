from .m_configs import MERCARI_POSTAGE, MERCARI_COMMISSION_RATE


def get_item_evaluation(item_price, average_price):
    profit, score = get_profit_and_price_score(item_price, average_price)

    evaluation = {
        "score": score,
        "profit": profit,
    }
    return evaluation

def get_profit_and_price_score(item_price, average_price):
    commission = int(average_price * MERCARI_COMMISSION_RATE)
    postage = MERCARI_POSTAGE
    profit = average_price - item_price - commission - postage
    if profit > 500:
        price_score = 10
    elif profit > 400:
        price_score = 9
    elif profit > 300:
        price_score = 8
    elif profit > 200:
        price_score = 7
    elif profit > 100:
        price_score = 7   
    else:
        price_score = 1 
    return (profit, price_score)  


if __name__ == "__main__":
    get_item_evaluation()