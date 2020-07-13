from html.parser import HTMLParser
from urllib import parse
from bs4 import BeautifulSoup
from urllib.request import urlopen
from general import *


class ItemFinder():

    def __init__(self, page_url, html_doc):
        self.page_url = page_url
        self.soup = BeautifulSoup(html_doc, 'html.parser')

        self.item = dict()
        self.item['app-id'] = page_url.split('/')[-1]

    def page_item(self):
        self.item['name'] = self.soup.h1.find(text=True, recursive=False).strip()
        self.item['taptap-app-area'] = self.soup.find(attrs={'class':'taptap-app-area'}).string
        self.item['app-rating-score'] = self.soup.find(attrs={'class':'app-rating-score'}).string
        self.item['description'] = self.soup.find(attrs={'class':'body-description-paragraph'}).text.strip()
        self.item['app-tag'] = [a.string.strip() for a in self.soup.find(attrs={'id':'appTag'}).find_all('a')]
        self.item['count-stats'] = [a.string.strip() for a in self.soup.find_all(attrs={'class':'count-stats'})]
        return self.item


# page_url = 'https://www.taptap.com/app/17997'
# res = urlopen(page_url)
# html_doc = res.read().decode('utf-8')
# finder = ItemFinder(page_url, html_doc)
# item = finder.page_item()
# print(item)
# write_item('taptap', item)