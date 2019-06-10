#! /usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
from bs4 import BeautifulSoup
import json
import urllib.request
import flickrapi
import re
import traceback




def image_query(mushroom_type):
    split = mushroom_type.split(" ")
    query = "+"
    query = query.join(split)
    google_url = "https://www.google.com/search?q=" + query + "&source=lnms&tbm=isch&sa=X"
    bing_rul = "https://www.bing.com/images/search?q=" + query
    urls = {'google' : google_url, "bing" : bing_rul}
    return urls


def download_page(url):
    print('run browser')
    try:
        chromedriver = "./chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        browser = webdriver.Chrome(chromedriver)
        browser.get(url)
        time.sleep(1)
        element = browser.find_element_by_tag_name("body")
        for i in range(10):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

            try:
                browser.find_element_by_class_name("btn_seemore").click()
                for i in range(20):
                    element.send_keys(Keys.PAGE_DOWN)
                    time.sleep(0.3)  # bot id protection
            except:
                try:
                    browser.find_element_by_id("smb").click()
                    for i in range(20):
                        element.send_keys(Keys.PAGE_DOWN)
                        time.sleep(0.3)  # bot id protection
                except:
                    for i in range(20):
                        element.send_keys(Keys.PAGE_DOWN)
                        time.sleep(0.3)  # bot id protection
        time.sleep(0.5)
        source = browser.page_source  # page source
        browser.close()
        return source
    except Exception as e:
        # print("get wrong url")
        print(str(e))




def parser_google_page(html):
    soup = BeautifulSoup(html, 'lxml')
    images_div = soup.findAll("div", {"class": "rg_meta"})
    f = open('urls.txt', 'w')
    count = 1
    urls = []
    for item in images_div:
        content = json.loads(item.text)
        f.write(content["ou"])
        urls.append(content["ou"])
        count += 1
    print("finished, " + str(count))
    print('there are ' + str(len(urls)) + ' images from google')
    return urls


def parser_flickr_page(mushroom_type):
    flickr = flickrapi.FlickrAPI('c6a2c45591d4973ff525042472446ca2', '202ffe6f387ce29b', cache=True)
    keyword = mushroom_type
    photos = flickr.walk(text=keyword,
                         tag_mode='all',
                         tags=keyword,
                         extras='url_c',
                         per_page=100,  # may be you can try different numbers..
                         sort='relevance')
    urls = []
    for i, photo in enumerate(photos):
        url = photo.get('url_c')
        urls.append(url)
        if i > 400:
            break
    print('there are ' + str(len(urls)) + ' images from flickr')
    return urls


def parser_bing_page(html):
    soup = BeautifulSoup(html, 'lxml')
    images_div = soup.findAll("a", {"class": "iusc"})
    urls = []
    for image in images_div:
        img = image.find("img")
        img = str(img)
        try:
            image_url = re.search('https://(\w|\d|[-\.\/\?=:])+', img)
            image_url = image_url.group()
            urls.append(image_url)
        except:
            print("invalid url")
    print('there are ' + str(len(urls)) + ' images from bing')
    return urls


def collect_urls(mushroom_type):
    query_urls = image_query(mushroom_type)
    google_page = download_page(query_urls['google'])
    google_results = parser_google_page(google_page)
    bing_page = download_page(query_urls['bing'])
    bing_results = parser_bing_page(bing_page)
    flickr_results = parser_flickr_page(mushroom_type)
    url_list = google_results[:400] + bing_results[:400] + flickr_results
    print(str(len(url_list)) + 'urls finded')
    file_name = mushroom_type + '-images urls.txt'
    f = open(file_name, 'w')
    count = 0
    fialed = 0
    for url in url_list:
        try:
            f.write(url + '\n')
            count += 1
        except:
            fialed += 1
    print('finished-- ' + str(count) + ' images urls writing')
    print(str(fialed) + ' image cannot be downloaded')
    return file_name


# def read_file():
#     f = open('pleurotus ostreatus-images urls.txt', 'r')
#     print(f.readline())
#
#
# read_file()


def download_img(url_file, type):
    print('start download images')
    f = open(url_file, 'r')
    url_list = f.readlines()
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    count = 1
    mkdir(type)
    for url in url_list:
        filename = './'+ type + '/image' + str(count) + '.jpg'
        try:
            urllib.request.urlretrieve(url, filename)
            count += 1
            print(filename + ' --finshed')
        except:
            print(url + ' --failed')
    print('image download complete')





def mkdir(file_path):
    is_exist = os.path.exists('./' + file_path)
    if not is_exist:
        os.makedirs('./' + file_path)
        print(file_path + ' new directory has been created')



def main():
    type = input('enter the mushroom type you want to download: ')
    urls = collect_urls(type)
    download_img(urls, type)

if __name__ == '__main__':
    main()


