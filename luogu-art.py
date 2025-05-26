import sys
import json
import argparse
import requests
from bs4 import BeautifulSoup

def fetch_article(article_id: str, proxies=None, **cookies):
    url = f"https://www.luogu.com/article/{article_id}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, cookies=cookies, headers=headers, proxies=proxies)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        script_tag = soup.find("script", {"id": "lentille-context", "type": "application/json"})
        if script_tag:
            return 200, script_tag.string
        return 200, None
    else:
        return int(response.status_code), None

def get_content(article_id: str, proxies=None, **cookies):
    status_code, content = fetch_article(article_id, proxies=proxies, **cookies)
    if content is None:
        return {"status": status_code, "data": None}
    data = json.loads(content)
    return data

def show_content(article_id: str, proxies=None, **cookies):
    data = get_content(article_id, proxies=proxies, **cookies)
    if data["data"] is not None:
        data = data["data"]["article"]
        print(f"# {data['title']}")
        print()
        print(f"*Author: {data['author']['name']}*")
        print()
        print(data["content"])
    else:
        print(f"Failed to fetch article: {article_id}", file=sys.stderr)
        print(f"Status code: {data['status']}", file=sys.stderr)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fetch and display article content from Luogu.")
    parser.add_argument("article_id", help="The ID of the article to fetch.")
    parser.add_argument("-u", "--uid", help="The UID for the cookies.")
    parser.add_argument("-c", "--client_id", help="The client ID for the cookies.")
    parser.add_argument("-f", "--cookie-file", help="Path to a file containing cookies in JSON format.")
    parser.add_argument("-p", "--proxy", help="The proxy server to use (e.g., http://proxy.example.com:8080).")

    args = parser.parse_args()

    cookies = {}

    if args.cookie_file:
        try:
            with open(args.cookie_file, "r") as f:
                cookies = json.load(f)
            assert isinstance(cookies, dict), "Cookie file must contain a JSON object."
            assert all(isinstance(k, str) and isinstance(v, str) for k, v in cookies.items()), "Cookies must be key-value pairs of strings."
        except AssertionError as e:
            print(f"Invalid cookie format: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Error reading cookie file: {e}", file=sys.stderr)

    if args.uid and args.client_id:
        cookies["uid"] = args.uid
        cookies["__client_id"] = args.client_id

    proxies = None
    if args.proxy:
        proxies = {
            "http": args.proxy,
            "https": args.proxy,
        }

    show_content(args.article_id, proxies=proxies, **cookies)
