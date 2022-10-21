import requests

def notify(url, name, score, profit, item_url, price):
    message = """
    url: {url}
    name: {name}
    score: {score}
    profit: {profit}
    item_url: {item_url}
    price: {price}
    """.format(url=url, name=name, score=score, profit=profit, item_url = item_url, price = price)
    send_line_notify(message)

def send_line_notify(notification_message):
    print("notification_message: ", notification_message)
if __name__ == "__main__":
    notify()