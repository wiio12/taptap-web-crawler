from html.parser import HTMLParser
from urllib import parse
from bs4 import BeautifulSoup
from urllib.request import urlopen
from general import *
import requests

class ReviewFinder():

    def __init__(self, page_url, html_doc, header):
        self.page_url = page_url
        self.soup = BeautifulSoup(html_doc, 'html.parser')
        self.header = header

        self.review = dict()
        self.review['review-id'] = page_url.split('/')[-1]
    
    def get_all_comment_soup(self, review_id):
        results = []
        page = 1
        while True:
            print ('get review {} page {}'.format(review_id, page))
            url = 'https://www.taptap.com/ajax/review/comments/{}?show_all=0&id={}&page={}'.format(review_id, review_id, page)
            res = requests.get(url, headers=self.header)
            html_doc = res.json()['data']['html']
            soup = BeautifulSoup(html_doc, 'html.parser').find_all(attrs={'class':'taptap-comment-item'})
            if soup:
                results += soup
            else:
                break
            page += 1
        return results



    def page_review(self):
        self.review['item-id'] = self.soup.find(attrs={'class':'main-app-text'}).find('a')['href'].strip().split('/')[-1]
        self.review['user-id'] = self.soup.find(attrs={'class':'review-main-user'}).find('a')['href'].strip().split('/')[-1]
        self.review['rating'] = int(self.soup.find(class_='main-contents-score').find(class_='colored')["style"][7:-2]) / 100
        self.review['time'] = self.soup.find(attrs={"class":"main-footer-time"}).find(attrs={"data-placement":"top"})['title'].strip()[4:]
        self.review['funny-count'] = self.soup.find(attrs={'data-value':'funny'}).find(attrs={'data-taptap-ajax-vote':'count'}).string
        self.review['upvoted-count'] = self.soup.find(attrs={'data-value':'up'}).find(attrs={'data-taptap-ajax-vote':'count'}).string

        
        tmp = self.soup.find(attrs={'id':'review-detail-reply-button'}).find('span')
        if tmp:
            self.review['comment-count'] = tmp.string
        else:
            self.review['comment-count'] = 0
        self.review['content'] = self.soup.find(attrs={'class':'main-contents-text'}).div.text.strip()
        
        comment_id = []
        comment_time = []
        comment_user = []
        comment_upvoted = []
        comment_downvoted = []
        comment_content = []

        all_comment = self.get_all_comment_soup(self.review['review-id'])
        for c in all_comment:
            comment_id.append(c['id'][8:])
            comment_time.append(c.find(attrs={'class':'text-footer-time'}).string)
            comment_user.append(c.find(attrs={'class':'taptap-user'})['data-user-id'])
            tmp = c.find(attrs={'data-value':"up"}).find('span').string
            comment_upvoted.append(tmp if tmp else 0)
            tmp = c.find(attrs={'data-value':"down"}).find('span').string
            comment_downvoted.append(tmp if tmp else 0)
            comment_content.append(c.find(attrs={'class':'item-text-body'}).text.strip())


        self.review['comment-id'] = comment_id
        self.review['comment-time'] = comment_time
        self.review['comment-user'] = comment_user
        self.review['comment-upvoted'] = comment_upvoted
        self.review['comment-downvoted'] = comment_downvoted
        self.review['comment-content'] = comment_content
        
        return self.review

# HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
#             "Cookie": "tapadid=b53366d2-5f94-8719-a1f9-dcf17d95476e; _ga=GA1.2.1904631115.1594384658; _gid=GA1.2.1825533947.1594384658; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6ImFlM0ZlWTFuVlRCTlVkRGtjc0tPbUE9PSIsInZhbHVlIjoibFdVZ1ZlZnIrTitiOW04V1hMVVhhTytDS3psS1JPUngySUlWUlo4VW42eUI5UEhpcDNkc2lIZDJYRmRcL3VXTlpsZHpUYjBvTlQ1T2JYb054REp2NTA3eDJuVDN0N1dVSUo0TXdTdFZcL2dMUT0iLCJtYWMiOiI1MmNjZDVjNzdmYTRhNjdkZTI2MGE2MGI4NzcxMTRjMWU3NGI2ZTQ5NWIwM2VjZWFjN2E5MGRlMjFkOTg3NjU0In0%3D; user_id=98599428; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2298599428%22%2C%22%24device_id%22%3A%2217338bb2d859a0-0194aeddee6bc2-4353760-2359296-17338bb2d86ae2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2217338bb2d859a0-0194aeddee6bc2-4353760-2359296-17338bb2d86ae2%22%7D; acw_tc=2760829b15946265484016098ec7389c097292278648e83891023fce42f5d0; XSRF-TOKEN=eyJpdiI6IkZyME5Hdm5KSWphdVQ1THc2VGpBaFE9PSIsInZhbHVlIjoieitOUXZENytqcUdYSzZmelcrNEp1OVAyNkU4bmgxN1I3VzJrTDdodFwvbTV6dEphcEZUdUNvSXlWd0NlbTU3TzU0QUFPN3dtRzFHZFI2UGRSWmN2ZEhnPT0iLCJtYWMiOiI5YzUwOGJiZmViMWMwNzdiNDdiNWVmNDkzNjIwMmIxNzIxNTgzYTgyYjQwZThhNjUyZjQyY2Q5MzI5ZWQ0OTNjIn0%3D; tap_sess=eyJpdiI6IkpuNW1kY2tSQlhDSFNlNGk5Z0JFZ1E9PSIsInZhbHVlIjoiOWtVY3pyVm9UTXY1S3hRckN0N1wvMEUzZ0Rxa3R6YVdWYlV1WGVOaUY0bWc2bW1nSGZZVm5UZ1Yzb2NHTVwvOUVmS2Jic0VjTmdXeGNiekRqcEIrbHpoQT09IiwibWFjIjoiMDQyY2Q3NzRkODM4N2ZmOTViZTk4ZjE1NTE0MWNhODRkNGQ1YmVkNDgwN2NiN2E1ZDM0MDIwZWRkZTc2YzY4OCJ9"}


# page_url = 'https://www.taptap.com/review/20418252'
# res = urlopen(page_url)
# html_doc = res.read().decode('utf-8')
# finder = ReviewFinder(page_url, html_doc, HEADERS)
# item = finder.page_review()
# print(item)
# write_review('taptap', item)