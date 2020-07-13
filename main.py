import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'taptap'
HOMEPAGE = 'https://www.taptap.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 20
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "Cookie": "tapadid=b53366d2-5f94-8719-a1f9-dcf17d95476e; _ga=GA1.2.1904631115.1594384658; _gid=GA1.2.1825533947.1594384658; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6ImFlM0ZlWTFuVlRCTlVkRGtjc0tPbUE9PSIsInZhbHVlIjoibFdVZ1ZlZnIrTitiOW04V1hMVVhhTytDS3psS1JPUngySUlWUlo4VW42eUI5UEhpcDNkc2lIZDJYRmRcL3VXTlpsZHpUYjBvTlQ1T2JYb054REp2NTA3eDJuVDN0N1dVSUo0TXdTdFZcL2dMUT0iLCJtYWMiOiI1MmNjZDVjNzdmYTRhNjdkZTI2MGE2MGI4NzcxMTRjMWU3NGI2ZTQ5NWIwM2VjZWFjN2E5MGRlMjFkOTg3NjU0In0%3D; user_id=98599428; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2298599428%22%2C%22%24device_id%22%3A%2217338bb2d859a0-0194aeddee6bc2-4353760-2359296-17338bb2d86ae2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2217338bb2d859a0-0194aeddee6bc2-4353760-2359296-17338bb2d86ae2%22%7D; acw_tc=2760829b15946265484016098ec7389c097292278648e83891023fce42f5d0; XSRF-TOKEN=eyJpdiI6IkZyME5Hdm5KSWphdVQ1THc2VGpBaFE9PSIsInZhbHVlIjoieitOUXZENytqcUdYSzZmelcrNEp1OVAyNkU4bmgxN1I3VzJrTDdodFwvbTV6dEphcEZUdUNvSXlWd0NlbTU3TzU0QUFPN3dtRzFHZFI2UGRSWmN2ZEhnPT0iLCJtYWMiOiI5YzUwOGJiZmViMWMwNzdiNDdiNWVmNDkzNjIwMmIxNzIxNTgzYTgyYjQwZThhNjUyZjQyY2Q5MzI5ZWQ0OTNjIn0%3D; tap_sess=eyJpdiI6IkpuNW1kY2tSQlhDSFNlNGk5Z0JFZ1E9PSIsInZhbHVlIjoiOWtVY3pyVm9UTXY1S3hRckN0N1wvMEUzZ0Rxa3R6YVdWYlV1WGVOaUY0bWc2bW1nSGZZVm5UZ1Yzb2NHTVwvOUVmS2Jic0VjTmdXeGNiekRqcEIrbHpoQT09IiwibWFjIjoiMDQyY2Q3NzRkODM4N2ZmOTViZTk4ZjE1NTE0MWNhODRkNGQ1YmVkNDgwN2NiN2E1ZDM0MDIwZWRkZTc2YzY4OCJ9"
            }

queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME, HEADERS)

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

create_workers()
crawl()