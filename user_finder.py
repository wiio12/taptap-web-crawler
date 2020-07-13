from html.parser import HTMLParser
from urllib import parse
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from general import *
from link_finder import LinkFinder
import re




class UserFinder():


    def __init__(self, page_url, html_doc, header):
        self.page_url = page_url
        self.soup = BeautifulSoup(html_doc, 'html.parser')

        self.user = dict()
        self.user['user-id'] = page_url.split('/')[-1]
        self.header = header
        

    def get_all_played_soup(self):
        if not is_user(self.page_url):
            return None
        user_id = self.page_url.split('/')[-1]
        results = []
        page = 1
        while True:
            url = "https://www.taptap.com/user/{}?page={}".format(user_id, page)
            print('getting user {} played page {}'.format(user_id, page))
            res = requests.get(url,headers=self.header)
            soup = BeautifulSoup(res.text, 'html.parser')
            if soup.find(attrs={'class':'taptap-user-card'}) is not None:
                results.append(soup.find(attrs={'class':'user-home-body'}))
            else:
                break
            page += 1
        return results

    def page_user(self):
        self.user['name'] = self.soup.h1.string.strip()
        tmp = self.soup.find(attrs={'class':'left-text-intro'}).string
        if tmp:
            self.user['intro'] = tmp.replace('\n',' ').replace(u'\xa0', u' ').strip()
        else:
            self.user['intro'] = None
        
        self.user['fans'], self.user['following'], self.user['collected'] = [x.string for x in self.soup.find_all(attrs={'class':'right-stats-number'})]
        vote = self.soup.find(attrs={'class':'left-text-vote'})
        if vote:
            u_f = [x.string for x in vote.find_all('span')]
        else:
            u_f = []
        if len(u_f) == 0:
            self.user['upvote'] = 0
            self.user['funny'] = 0
        elif len(u_f) == 1:
            self.user['upvote'] = u_f[0]
            self.user['funny'] = 0
        else:
            self.user['upvote'] = u_f[0]
            self.user['funny'] = u_f[1]
        played_soup = self.get_all_played_soup()
        played = []
        played_time = []
        user_cards = []
        for s in played_soup:
            u = s.find_all(attrs={'class':'taptap-user-card'})
            user_cards += u
        for uc in user_cards:
            played.append(uc['id'][7:])
            time = uc.find(attrs={'class':'play_time'})
            if time:
                played_time.append(time.string.strip()[5:])
            else:
                played_time.append('')
        self.user['played'] = played
        self.user['played-time'] = played_time
        return self.user

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "Cookie": "tapadid=b53366d2-5f94-8719-a1f9-dcf17d95476e; _ga=GA1.2.1904631115.1594384658; _gid=GA1.2.1825533947.1594384658; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6ImFlM0ZlWTFuVlRCTlVkRGtjc0tPbUE9PSIsInZhbHVlIjoibFdVZ1ZlZnIrTitiOW04V1hMVVhhTytDS3psS1JPUngySUlWUlo4VW42eUI5UEhpcDNkc2lIZDJYRmRcL3VXTlpsZHpUYjBvTlQ1T2JYb054REp2NTA3eDJuVDN0N1dVSUo0TXdTdFZcL2dMUT0iLCJtYWMiOiI1MmNjZDVjNzdmYTRhNjdkZTI2MGE2MGI4NzcxMTRjMWU3NGI2ZTQ5NWIwM2VjZWFjN2E5MGRlMjFkOTg3NjU0In0%3D; user_id=98599428; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2298599428%22%2C%22%24device_id%22%3A%2217338bb2d859a0-0194aeddee6bc2-4353760-2359296-17338bb2d86ae2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2217338bb2d859a0-0194aeddee6bc2-4353760-2359296-17338bb2d86ae2%22%7D; acw_tc=2760829b15946265484016098ec7389c097292278648e83891023fce42f5d0; XSRF-TOKEN=eyJpdiI6IkZyME5Hdm5KSWphdVQ1THc2VGpBaFE9PSIsInZhbHVlIjoieitOUXZENytqcUdYSzZmelcrNEp1OVAyNkU4bmgxN1I3VzJrTDdodFwvbTV6dEphcEZUdUNvSXlWd0NlbTU3TzU0QUFPN3dtRzFHZFI2UGRSWmN2ZEhnPT0iLCJtYWMiOiI5YzUwOGJiZmViMWMwNzdiNDdiNWVmNDkzNjIwMmIxNzIxNTgzYTgyYjQwZThhNjUyZjQyY2Q5MzI5ZWQ0OTNjIn0%3D; tap_sess=eyJpdiI6IkpuNW1kY2tSQlhDSFNlNGk5Z0JFZ1E9PSIsInZhbHVlIjoiOWtVY3pyVm9UTXY1S3hRckN0N1wvMEUzZ0Rxa3R6YVdWYlV1WGVOaUY0bWc2bW1nSGZZVm5UZ1Yzb2NHTVwvOUVmS2Jic0VjTmdXeGNiekRqcEIrbHpoQT09IiwibWFjIjoiMDQyY2Q3NzRkODM4N2ZmOTViZTk4ZjE1NTE0MWNhODRkNGQ1YmVkNDgwN2NiN2E1ZDM0MDIwZWRkZTc2YzY4OCJ9"}



# base_url = 'https://www.taptap.com'
# page_url = 'https://www.taptap.com/user/19165178'
# post_url = 'https://www.taptap.com/ajax/user/71731647/played'
# # page = 'https://www.taptap.com/ajax/friendship/multi-get?user_ids=&app_ids=%2C&group_ids=&developer_ids=&format=json&show_text_ids=%7B%22user%22%3A%5B%222%22%5D%7D'
# res = requests.get(page_url,headers=HEADERS)
# html_doc = res.text
# # print(html_doc)
# # l_finder = LinkFinder(base_url, page_url)
# # l_finder.feed(html_doc)
# # links = l_finder.page_links()
# # [print(l) if l.startswith(page_url + '?') else 'None' for l in sorted(links)]
# finder = UserFinder(page_url, html_doc, HEADERS)
# user = finder.page_user()
# #[print(s) for s in soup]
# print(user)
# write_user('taptap', user)

