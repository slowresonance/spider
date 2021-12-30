from bs4.element import SoupStrainer
import requests
from bs4 import BeautifulSoup as bs
import threading
import concurrent.futures


class Spider:
    def __init__(self, seeds):
        self.seen = set()
        self.to_see = set(seeds)
        self.errored = []
        self.exl_ext = [
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".tif",
            ".txt",
            ".pdf",
            ".svg",
            "=",
            "?",
            "&",
            ":+",
        ]
        self.lock = threading.Lock()

    def start_spider(self):
        while self.to_see:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.fetch, self.to_see)
            print(*self.to_see, sep="\n")
        # while self.to_see:
        #     link = self.to_see.pop()
        #     self.fetch(link)

    def fetch(self, url):
        self.seen.add(url)
        # print(f"🏁 STARTED PARSING {url} \n")
        try:
            response = requests.get(url)
            html = response.content
            soup = bs(html, features="lxml")
        except:
            return print(f"🛑 COULDN'T ACCESS {url} \n")

        valid_links = []

        for link in soup.findAll("a", href=True):
            s = self.parse(url, link["href"])
            if s != 0:
                valid_links.append(s)

        # print(f"✅ COMPLETED PARSING {url} \n")
        # print(f"🔎 FOUND {len(valid_links)} NEW LINK(S) \n")
        # print(*valid_links, sep="\n")
        print(f"\n📢 UPDATED QUEUE COUNT: {len(self.to_see)} \n")

    def parse(self, base, url):
        # https://stackoverflow.com/a/10893427
        from urllib.parse import urljoin

        s = urljoin(base, url)

        if "#" in s:
            s = s.split("#")[0]

        if s in self.seen or s in self.to_see:
            return 0
        for e in self.exl_ext:
            if e in s:
                return 0

        self.to_see.add(s)
        return s


seeds = [
    # "https://github.com/jwasham/coding-interview-university",
    # "https://en.wikipedia.org/wiki/Web_crawler",
    "https://blog.hubspot.com/marketing/web-crawler"
]

spider = Spider(seeds)
spider.start_spider()
