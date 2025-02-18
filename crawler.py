import sys
import json
import argparse
import requests
from bs4 import BeautifulSoup


def fetch_article(article_id: str, **cookies):
    url = f"https://www.luogu.com/article/{article_id}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, cookies=cookies, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # <script id="lentille-context" type="application/json">...</script>
        script_tag = soup.find(
            "script", {"id": "lentille-context", "type": "application/json"}
        )
        if script_tag:
            return 200, script_tag.string
        return 200, None
    else:
        return int(response.status_code), None


def get_content(article_id: str, **cookies):
    status_code, content = fetch_article(article_id, **cookies)
    if content is None:
        return {"status": status_code, "data": None}
    data = json.loads(content)
    return data


def show_content(article_id: str, **cookies):
    data = get_content(article_id, **cookies)
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
    parser = argparse.ArgumentParser(
        description="Fetch and display article content from Luogu."
    )
    parser.add_argument("article_id", help="The ID of the article to fetch.")
    parser.add_argument("--uid", help="The UID for the cookies.")
    parser.add_argument("--client_id", help="The client ID for the cookies.")

    args = parser.parse_args()

    cookies = {}
    if args.uid and args.client_id:
        cookies["uid"] = args.uid
        cookies["__client_id"] = args.client_id

    show_content(args.article_id, **cookies)
