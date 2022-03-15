# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# from bs4 import BeautifulSoup
import urllib.request

import time 
import requests
import json
import os 
from tqdm import tqdm
from progress.spinner import Spinner
import string 

import config
import utils

spinner = Spinner('Loading ')

class ShopeeCrawler_API():
    def __init__(self) -> None:
        pass
    
    
    def crawl_by_shop_id(self, limit=90, shop_name='search_items_orihiro_officialstore', shop_id="350069056", lst_itemid=set()):
        os.makedirs(os.path.join('pharma', str(shop_name) ), exist_ok=True)
        lst_existed_title = os.listdir(os.path.join('pharma', str(shop_name)))                
        url = config.SHOPEE_API_SEARCH_BY_SHOP.format(limit, shop_id)    
        session = requests.Session()
        # response = requests.get(url=url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} )
        response = session.get(url=url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} )

        res = response.json()

        items = res['items']
        # spn = Spinner("Fetching for shop {}/ Page {}".format(shop_id,i + 1) )           
        for item in items: 
            shop_id = str(item['item_basic']['shopid']) 
            item_id = str(item['item_basic']['itemid'])
            if shop_id + '-' + item_id in lst_itemid:
                continue
            
            # print("Fetching for item {}".format(utils.make_product_url(shop_id, item_id)))
            try:
                item_dict = self.crawl_item(shop_id, item_id, lst_existed_title)
                if item_dict:
                    self.write_to_file(shop_id, item_dict)
                    lst_itemid.add(shop_id + '-' + item_id)
            except:
                continue

        
    
    def crawl_by_terms(self, term, lst_itemid):
        
        offset= 0
        os.makedirs(os.path.join('output', term), exist_ok=True)
        lst_existed_title = os.listdir(os.path.join('output', term))
        limit = 60
        
        if term == 'skincare': 
            return
        
        for i in range(0, 5): 
            url = config.SHOPEE_API_SEARCH_RElEVANCY.format(term, offset)    
            res = requests.get(url=url).json()   
            items = res['items']
            print("Fetching for term {}/ Page {}".format(term,i + 1) )           
            for item in items: 
                shop_id = str(item['item_basic']['shopid']) 
                item_id = str(item['item_basic']['itemid'])
                if shop_id + '-' + item_id in lst_itemid:
                    continue
                
                print("Fetching for item {}".format(utils.make_product_url(shop_id, item_id)))
                
                item_dict = self.crawl_item(shop_id, item_id, lst_existed_title)
                if item_dict:
                    self.write_to_file(term, item_dict)
                    lst_itemid.add(shop_id + '-' + item_id)
            
            offset += limit
            
    
    
    def crawl_item(self, shop_id, item_id, lst_existed_title):
        
        item_dict = dict()
        
        item_dict['item_id'] = item_id
        item_dict['shop_id'] = shop_id
        item_dict['url'] = utils.make_product_url(shop_id, item_id)
        
        # Get item basic information
        try: 
            title, desc, brand, rating_stars, breadcrumbs = self.extract_item_information(shop_id, item_id)
        except: 
            return None  
        if title + '.json' in lst_existed_title:
            return None
        
        if title.translate(str.maketrans('', '', string.punctuation)) in lst_existed_title:
            return None
        
        item_dict['title'] = title 
        item_dict['breadcrumb'] = breadcrumbs
        item_dict['desc'] = desc 
        item_dict['brand'] = brand
        item_dict['avg_star'] = rating_stars
        
        # Get reviews
        item_dict['reviews'] = self.extract_comments_from_shopee_api(shop_id, item_id)
        
        return item_dict
        
    
    def write_to_file(self, term, item_dict): 
        filepath = item_dict['title'].translate(str.maketrans('', '', string.punctuation))
        try:
            with open('output/' + term + '/' + filepath + '.json', 'w', encoding='utf8') as fp:
                json.dump(item_dict, fp, indent=4, ensure_ascii=False)        
        except OSError as e:
            print(e)
            
        
    def extract_item_information(self, shop_id, item_id):
        try: 
            url = config.SHOPEE_PRODUCT_INFORMATION.format(shop_id, item_id)
            result = requests.get(url).json()
            
            return result['data']['name'], result['data']['description'], result['data']['brand'], result['data']['item_rating']['rating_star'], [item['display_name'] for item in result['data']['fe_categories']]
        except Exception as e: 
            print(e)
            print("ERROR with this: ", utils.make_product_url(shop_id, item_id))
        finally:
            time.sleep(0.5)
    # def extract_item_information_use_bsoup(self, product_url):
    #     page = urllib.request.urlopen(product_url)
    #     soup = BeautifulSoup(page, 'html.parser')
    #     with open('temp.html', 'w') as f:
    #         f.write(soup.prettify())

    #     # new_feeds = soup.find_all('h3', class_='.page-product__breadcrumb .')
    #     a = soup.select('div.page-product__breadcrumb')
    #     print(a)
        
    
    def extract_comments_from_shopee_api(self, shop_id, item_id): 
        reviews = [
            [], #1star
            [], #2star
            [], #3star
            [], #4star
            [] #5star
        ]
        # reviews_5star = []
        # reviews_4star = []
        # reviews_3star = []
        # reviews_2star = []
        # reviews_1star = []

        offset = 0
        url = config.SHOPEE_API_RATINGS.format(item_id, offset, shop_id, 1)
        
        first_call = requests.get(url = url).json()
        
        maximum_reviews = first_call['data']['item_rating_summary']['rating_total']
        try:
            if offset + config.SHOPEE_API_RATINGS_MAX_REVIEWS < maximum_reviews:
                while offset + config.SHOPEE_API_RATINGS_MAX_REVIEWS < maximum_reviews:
                    url = config.SHOPEE_API_RATINGS.format(item_id, offset, shop_id, config.SHOPEE_API_RATINGS_MAX_REVIEWS)
                    print(url)
                    spinner.next()
                    ratings = requests.get(url= url).json()        
                    for rating in ratings['data']['ratings']: 
                        if not rating['comment']:
                            continue
                        reviews[rating['rating_star'] - 1].append({
                            "comment": rating['comment'],
                            "tags": rating['tags']
                        })
                    
                    offset += config.SHOPEE_API_RATINGS_MAX_REVIEWS
                    # time.sleep(0.5)
            else:
                url = config.SHOPEE_API_RATINGS.format(item_id, offset, shop_id, config.SHOPEE_API_RATINGS_MAX_REVIEWS)
                    
                ratings = requests.get(url= url).json()        
                for rating in ratings['data']['ratings']: 
                    reviews[rating['rating_star'] - 1].append({
                        "comment": rating['comment'],
                        "tags": rating['tags']
                    })
                
                offset += config.SHOPEE_API_RATINGS_MAX_REVIEWS
            # time.sleep(0.5)
        except Exception as e:
            print(e)
        
        return reviews
        
        
    def __close_connection__(self):
        print("closed")
        self.driver.quit()

if __name__ == '__main__': 
    crawler = ShopeeCrawler_API()
    crawler.crawl_by_shop_id()