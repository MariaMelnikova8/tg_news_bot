import requests


def telegram_send_message(tg_id, post, picture_link, tg_token):
    url = f'https://api.telegram.org/bot{tg_token}/sendPhoto'
    params = {
        "photo": picture_link,
        "chat_id": tg_id,
        "caption": post
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
