# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# from bs4 import BeautifulSoup
import filecmp
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

import re

import urllib.request

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

spinner = Spinner('Loading ')

class ShopeeCrawler_API():
    def __init__(self) -> None:
        pass
    
    
    def crawl_by_shop_recommend_bundle(self, limit=90, shop_name='pernodricardvn', shop_id="574100363", lst_itemid=set()):
        with open('list_url.txt', 'r') as f: 
            list_url = f.read().splitlines()
            

        # cookie = utils.parseCookieFile('cookie_raw.txt')
        # list_url = '17075070599'
        lst_itemid =  set([item_id for item_id in os.listdir(os.path.join('output', 'homecare', shop_name))])

        for url in list_url: 
            # res = requests.get(url=url, cookies=cookie).json()
            res = requests.get(url=url).json()

            # shop_id = utils.get_shop_id_from_url(url)
            

            product_hot_deals_count = res['data']['sections'][0]['total']
            print("total_product_hot_deals_count", product_hot_deals_count)
            product_hot_deals = res['data']['sections'][0]['data']['item']

            product_rfu_count = res['data']['sections'][1]['total']
            print("total_product_rfu_count", product_rfu_count)
            product_rfu = res['data']['sections'][1]['data']['item']
            
            
            # lst_product = product_hot_deals + product_rfu
            lst_product = product_rfu

            for product in tqdm(lst_product): 
            
                item_id = product['itemid']
                
                if item_id in lst_itemid:
                    print("PONG")
                    continue
                
                product_to_export = dict()
                
                product_to_export['shop_id'] = shop_id
                product_to_export['item_id'] = item_id
                product_to_export['name'] = product['name']
                product_to_export['avg_star'] = product['shop_rating']
                product_to_export['url'] = config.SHOPPE_PRODUCT_URL + str(shop_id) + '/' + str(item_id) + '/'
                product_to_export['breadcrumb'] = []
                product_to_export['desc'] = ""
                product_to_export['brand'] = product['brand']
                product_to_export['reviews'] = self.extract_comments_from_shopee_api(shop_id, item_id)
                
                
                self.write_to_file('homecare/' + shop_name, product_to_export)
                lst_itemid.add(item_id)


      
    
    
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
        filepath = str(item_dict['item_id'])
        try:
            with open('output/' + term + '/' + filepath + '.json', 'w', encoding='utf8') as fp:
                json.dump(item_dict, fp, indent=4, ensure_ascii=False)        
        except OSError as e:
            print(e)

    def write_only_ratings_to_file(self, term, item_dict): 
        try: 
            with open(os.path.join('output_domain', term, '.txt'), 'a', encoding='utf8') as fp:
                for rating in item_dict['reviews']: 
                    fp.write(rating + '\n')

            with open(os.path.join('output_domain', term, '_itemId.txt'), 'a', encoding='utf8') as fp:
                fp.write(item_dict['item_id'] + '\n')
        except OSError as e: 
            print(e)
            
        
    def extract_item_information(self, shop_id, item_id):
        try: 
            url = config.SHOPEE_PRODUCT_INFORMATION.format(shop_id, item_id)
            result = requests.get(url).json()
            print(result)
            
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
        
    
    def extract_comments_from_shopee_api(self, shop_id=574100363, item_id=18061404526): 
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
        url = config.SHOPPE_PRODUCT_RATINGS_API.format(item_id, offset, shop_id, 1)
        count_empty_ratings= 0
        limit_empty_ratings= 5
        
        first_call = requests.get(url = url).json()
        
        maximum_reviews = first_call['data']['item_rating_summary']['rating_total']
        try:
            if offset + config.SHOPEE_RATINGS_API_MAX_RETURNED < maximum_reviews:
                while offset + config.SHOPEE_RATINGS_API_MAX_RETURNED < maximum_reviews:
                    url = config.SHOPPE_PRODUCT_RATINGS_API.format(item_id, offset, shop_id, config.SHOPEE_RATINGS_API_MAX_RETURNED)
                    print(url)
                    spinner.next()
                    ratings = requests.get(url= url).json()   

                    if len(ratings['data']['ratings']) == 0:
                        count_empty_ratings += 1
                        if count_empty_ratings > limit_empty_ratings:
                            return reviews

                    for rating in ratings['data']['ratings']: 
                        if not rating['comment']:
                            continue
                        reviews[rating['rating_star'] - 1].append({
                            "comment": rating['comment'],
                            "tags": rating['tags']
                        })
                    
                    offset += config.SHOPEE_RATINGS_API_MAX_RETURNED
                    # time.sleep(0.5)
            else:
                url = config.SHOPPE_PRODUCT_RATINGS_API.format(item_id, offset, shop_id, config.SHOPEE_RATINGS_API_MAX_RETURNED)
                    
                ratings = requests.get(url= url).json()        
                for rating in ratings['data']['ratings']: 
                    reviews[rating['rating_star'] - 1].append({
                        "comment": rating['comment'],
                        "tags": rating['tags']
                    })
                    print(reviews)
                
                offset += config.SHOPEE_RATINGS_API_MAX_RETURNED
            # time.sleep(0.5)
        except Exception as e:
            print(e)
        
        return reviews
        
        
    def __close_connection__(self):
        print("closed")
        self.driver.quit()

if __name__ == '__main__': 
    crawler = ShopeeCrawler_API()
    # crawler.crawl_by_shop_id()
    # crawler.crawl_by_shop_recommend_bundle()
    # crawler.crawl_by_terms(term="baking soda", lst_itemid=set())
    crawler.extract_comments_from_shopee_api()