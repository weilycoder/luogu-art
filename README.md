## 洛谷文章下载器

以 Markdown 格式下载洛谷文章区代码。

项目初衷是方便下载后转其他打印友好的格式，以方便不在机房时阅读。

使用方法：

```plaintext
usage: luogu-art.py [-h] [-u UID] [-c CLIENT_ID] [-f COOKIE_FILE] [-p PROXY] article_id

Fetch and display article content from Luogu.

positional arguments:
  article_id            The ID of the article to fetch.

optional arguments:
  -h, --help            show this help message and exit
  -u UID, --uid UID     The UID for the cookies.
  -c CLIENT_ID, --client_id CLIENT_ID
                        The client ID for the cookies.
  -f COOKIE_FILE, --cookie-file COOKIE_FILE
                        Path to a file containing cookies in JSON format.
  -p PROXY, --proxy PROXY
                        The proxy server to use (e.g., http://proxy.example.com:8080).
```

### 其他声明

图标从 [洛谷](https://github.com/luogu-dev) 复制，非原创，请勿商业使用，其他内容使用 MIT 许可证。
