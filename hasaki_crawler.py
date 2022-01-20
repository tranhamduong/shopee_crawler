# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

from cgitb import text
from bs4 import BeautifulSoup
import urllib.request
from unidecode import unidecode
import re
import time 
import requests
import json
import os 
from tqdm import tqdm
from progress.spinner import Spinner
import string 

import config
import utils

spinner = Spinner('Crawling ')

terms = [
    "Sức Khỏe - Làm Đẹp"
]

class HasakiCrawler_API():
    def __init__(self) -> None:
        pass
    
    
    def crawl(self, lst_itemid):
        start_index = 95163
        end_index = 100000
        
        for i in tqdm(range(start_index, end_index)):
            # spinner.next(text=str(i))

            item_id = str(i)
            if item_id in lst_itemid:
                continue
                
            try:
                item_dict = self.crawl_item(item_id)
                if item_dict:
                    self.write_to_file(item_dict)
                    lst_itemid.add(item_id)
            except Exception as e:
                print("exception in crawling item ", item_id, e)
                continue            
    
    
    def write_to_file(self, item_dict): 
        # filepath = item_dict['title'].translate(str.maketrans('', '', string.punctuation))
        filepath = item_dict['item_id']
        try:
            tmp_dir = ['output_hasaki'] + ["_".join(unidecode(crumb).split()) for crumb in item_dict['breadcrumb']]
            os.makedirs(os.path.join(*tmp_dir), exist_ok = True)
            with open( os.path.join(*tmp_dir) + '/' + filepath + '.json', 'w', encoding='utf8') as fp:
                json.dump(item_dict, fp, indent=4, ensure_ascii=False)        
        except OSError as e:
            print("Exception in writing",e)

            
    
    def crawl_item(self, item_id):
        
        item_dict = dict()
        
        item_dict['item_id'] = item_id
        
        # Get item basic information
        title, desc, brand, avg_star, breadcrumb, url = self.extract_item_information(item_id)
        
        item_dict['title'] = title 
        item_dict['breadcrumb'] = breadcrumb
        item_dict['desc'] = desc 
        item_dict['brand'] = brand
        item_dict['avg_star'] = avg_star
        item_dict['url'] = url
        
        # Get reviews
        item_dict['reviews'] = self.extract_comments_from_api(item_id)
        
        return item_dict


    def extract_item_information(self, item_id):
        # try: 
        url = config.HASAKI_URL_PRODUCT.format(item_id)
        # response = requests.get(url)
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        
        try: 
            breadcrumb = soup.find_all("nav", {"id": "breadcrumb"})[0]
        except IndexError: 
            print("No breadcrumb found --> wrong page" , item_id)
            return 

        breadcrumb_str = [breadcrumb for breadcrumb in breadcrumb.get_text().split("\n") if breadcrumb and breadcrumb != " " and breadcrumb != 'Trang chủ'][:-1]

        match_term = [term for term in terms if term in breadcrumb_str]
        if not match_term: 
            return

        title = soup.find_all("div", {"class": "page-title name_detail"})[0].get_text().strip()
        desc = soup.find_all("div", {"id": "box_thongtinsanpham"})[0].get_text().strip()
        brand = soup.find_all("div", {"class": "thumb_brand_follow"})[0].a["href"].split("https://hasaki.vn/thuong-hieu/")[1].split(".html")[0]
        avg_star_style = soup.find_all("div", {"class": "number_start"})[0]["style"]
        avg_star = int(''.join([n for n in avg_star_style if n.isdigit()])) / 20 


        return title, desc, brand, avg_star, breadcrumb_str, url


    def extract_faqs_from_api(self, item_id, faqs = dict()):
        

        offset = 0
        url = config.HASAKI_API_FAQS.format(item_id, offset)    

        is_continue = True

        while is_continue: 
            url = config.HASAKI_API_FAQS.format(item_id, offset)
            response = requests.get(url = url).json()
            total_item = int(response['data']['total_item'])
            if total_item == 0:
                is_continue = False
            else: 
                if item_id not in faqs:
                    faqs[item_id] = []
                    
            # if ok --> continue
            soup = BeautifulSoup(response['data']['html'], 'html.parser')
            for link in soup.find_all("div", {"class": "item_quest"}):
                question = link.find("div", {"class": "txt_quest"}).get_text()
                if question and question != " ": 
                    faqs[item_id].append(
                        {
                            "question": question,
                            "answer": []
                        }
                        )
                
                for answer in link.find_all("div", {"class": "txt_answear"}):
                    if answer and answer != " ":
                        faqs[item_id][-1]["answer"].append(
                            answer.get_text().strip()
                        )
            offset += total_item
        return faqs



    def extract_comments_from_api(self, item_id): 
        reviews = [
            [], #1star
            [], #2star
            [], #3star
            [], #4star
            [] #5star
        ]

        offset = 0
        url = config.HASAKI_API_RATINGS.format(item_id, offset)
        
        is_continue = True

        while is_continue: 
            url = config.HASAKI_API_RATINGS.format(item_id, offset)
            response = requests.get(url = url).json()
            total_item = int(response['data']['total_item'])
            if total_item == 0:
                is_continue = False

            # if ok --> continue
            soup = BeautifulSoup(response['data']['html'], 'html.parser')
            for link in soup.find_all("div", {"class": "item_comment"}):
                star = link.find_all("div", {"class": "number_start"})[0]["style"]
                star = int(int(''.join([n for n in star if n.isdigit()])) / 20 )
                # print("star", star)
                comment = link.find("div", {"class": "content_comment"}).get_text()
                # print("="*10)
                if comment and comment != " ":
                    reviews[star - 1].append(comment)

            offset += total_item
        return reviews
        
    def __close_connection__(self):
        print("closed")
        self.driver.quit()

        
if __name__ == '__main__':
    lst_itemId = set()
    crawler = HasakiCrawler_API()
    with open('hasaki_item_ids.txt', 'r') as f:
        ids = f.read().splitlines()[17500:]
        for _id in tqdm(ids):
            faqs = crawler.extract_faqs_from_api(item_id=_id)
        
    with open('output_hasaki_faqs/result_8.json', 'w', encoding='utf8') as fp:
        json.dump(faqs, fp, ensure_ascii=False)
        
    # crawler.crawl(lst_itemId)

    
