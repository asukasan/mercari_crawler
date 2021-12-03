import requests
from . import line_configs

def notify(url, name, score, profit):
    message = """
    url: {url}
    name: {name}
    score: {score}
    profit: {profit}
    """.format(url=url, name=name, score=score, profit=profit)
    send_line_notify(message)

def send_line_notify(notification_message):
    """
    LINEに通知する
    """
    line_notify_token = line_configs.line_notify_token
    line_notify_api = line_configs.line_notify_api
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'message: {notification_message}'}
    requests.post(line_notify_api, headers = headers, data = data)

if __name__ == "__main__":
    notify()