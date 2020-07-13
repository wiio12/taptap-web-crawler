import os
import csv
import re

# Each website you crawl is a separeate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating project ' + directory)
        os.makedirs(directory)

# Create queue and crawled files (if not created)
def create_data_files(project_name, base_url):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    items = project_name + '/items.csv'
    users = project_name + '/users.csv'
    reviews = project_name + '/reviews.csv'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')
    if not os.path.isfile(items):
        write_file(items, '')
    if not os.path.isfile(users):
        write_file(users, '')
    if not os.path.isfile(reviews):
        write_file(reviews, '')

# Create a new file
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()


# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write((data.strip() + '\n').replace(u'\xa0', u' '))

# Delete the contents of a file
def delete_file_contents(path):
    with open(path, 'w'):
        pass

# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

# Iterate through a set, each item will be a new line in the file
def set_to_file(file_name, links):
    delete_file_contents(file_name)
    for link in sorted(links):
        append_to_file(file_name, link)

# Judge if a web page is an item
def is_item(url):
    if re.match(r'^https:\/\/www\.taptap\.com\/app\/[0-9]+$', url):
        return True
    return False

# Judge if a web url is an user
def is_user(url):
    if re.match(r'^https:\/\/www\.taptap\.com\/user\/[0-9]+$', url):
        return True
    return False

def is_review(url):
    if re.match(r'^https:\/\/www\.taptap\.com\/review\/[0-9]+$', url):
        return True
    return False

def is_needed(url):
    flag = False
    if re.match(r'^https:\/\/www\.taptap\.com\/user\/[0-9]+\/reviews$', url):
        flag = True
    if re.match(r'^https:\/\/www\.taptap\.com\/user\/[0-9]+\/reviews\?page', url):
        flag = True
    if re.match(r'^https:\/\/www\.taptap\.com\/app\/[0-9]+\/review$', url):
        flag = True
    if re.match(r'^https:\/\/www\.taptap\.com\/app\/[0-9]+\/review\?order', url):
        flag = True
    return flag


# Write item data to csv file
def write_item(project_name, item):
    item_file = project_name + '/items.csv'
    
    if os.stat(item_file).st_size == 0:
        with open(item_file, 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, item.keys())
            w.writeheader()
            w.writerow(item)
    else:
        with open(item_file, 'a', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, item.keys())
            w.writerow(item)

# Write user data to csv file
def write_user(project_name, user):
    user_file = project_name + '/users.csv'
    
    if os.stat(user_file).st_size == 0:
        with open(user_file, 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, user.keys())
            w.writeheader()
            w.writerow(user)
    else:
        with open(user_file, 'a', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, user.keys())
            w.writerow(user)

# Write review data to csv file
def write_review(project_name, review):
    review_file = project_name + '/reviews.csv'

    if os.stat(review_file).st_size == 0:
        with open(review_file, 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, review.keys())
            w.writeheader()
            w.writerow(review)
    else:
        with open(review_file, 'a', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, review.keys())
            w.writerow(review)