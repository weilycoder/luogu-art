import requests
from bs4 import BeautifulSoup


def fetch_article(article_id, uid, client_id):
    url = f"https://www.luogu.com.cn/article/{article_id}"

    cookies = {"uid": uid, "__client_id": client_id}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, cookies=cookies, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        return 200, soup.article
    else:
        return int(response.status_code), None


print(fetch_article("fwod4ozy", "818693", "d95b3fe40b6a19e667901d97a5b9cacb4e62b97d"))
