from urllib.request import urlopen
from link_finder import LinkFinder
from item_finder import ItemFinder
from user_finder import UserFinder
from review_finder import ReviewFinder
from general import *
import requests

class Spider:

    # Class variables (shared among all instances)
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    header = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name, header):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.header = header
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        
        self.boot()
        self.crawl_page('First spider', Spider.base_url)
    
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)
    
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled ' + str(len(Spider.crawled)))
            links, item, user, review = Spider.gather_info(page_url)
            Spider.add_links_to_queue(links)
            if item:
                write_item(Spider.project_name, item)
            if user:
                write_user(Spider.project_name, user)
            if review:
                write_review(Spider.project_name, review)
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()
    

    @staticmethod
    def gather_info(page_url):
        html_doc = ''
        links = None
        item = None
        user = None
        review = None
        try:
            response = requests.get(page_url, headers=Spider.header)
            html_doc = response.text
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_doc)
            links = finder.page_links()
            if is_item(page_url):
                item_finder = ItemFinder(page_url, html_doc)
                item = item_finder.page_item()
            if is_user(page_url):
                user_finder = UserFinder(page_url, html_doc, Spider.header)
                user = user_finder.page_user()
            if is_review(page_url):
                review_finder = ReviewFinder(page_url, html_doc, Spider.header)
                review = review_finder.page_review()
        except:
            print('Error: can not crawl page ' + page_url)
            return set(), None, None, None
        return links, item, user, review

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domain_name not in url:
                continue
            if is_item(url) == False and is_user(url) == False and is_review(url) == False and is_needed(url) == False:
                continue
            Spider.queue.add(url)
    
    @staticmethod
    def update_files():
        set_to_file(Spider.queue_file, Spider.queue)
        set_to_file(Spider.crawled_file, Spider.crawled)


