from bs4 import BeautifulSoup
import requests


class scrape:

    def __init__(self, url):
        self.url = url
        self.page = None
        self.response = None

        try:
            self.response = requests.get(
                self.url,
                allow_redirects=False,
                timeout=10,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            if self.response.status_code == 200:
                self.page = BeautifulSoup(self.response.text, 'html.parser')

        except requests.exceptions.RequestException as e:
            print(f"[SCRAPER ERROR] {self.url} -> {e}")

    def get_title(self):
        if not self.page:
            return None
        tag = self.page.find('title')
        return tag.string.strip() if tag and tag.string else None

    def get_meta_description(self):
        if not self.page:
            return None

        tag = self.page.find("meta", attrs={"name": "description"})
        return tag.get("content") if tag else None

    def get_h1_tags(self):
        if not self.page:
            return []
        return [h.text.strip() for h in self.page.find_all("h1")]

    def get_canonical(self):
        if not self.page:
            return None
        tag = self.page.find("link", rel="canonical")
        return tag.get("href") if tag else None

    def get_viewports(self):
        if not self.page:
            return False
        return self.page.find("meta", attrs={"name": "viewport"}) is not None