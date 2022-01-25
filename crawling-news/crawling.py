import feedparser


# ニュース記事のデータを取得するためのクラス
class CrawlingNews:

    def __init__(self, rss_url):
        self.rss_url = rss_url

    def crawling(self):
        # ニュース記事のRSSからタイトルと要約を取得してリストに格納する。
        data = feedparser.parse(self.rss_url)
        news = [[entry.title, entry.summary, entry.link] for entry in data.entries]

        return news
