import json 
from crawler import ShopeeCrawler_API
import os 
from  tqdm import tqdm

if __name__ == '__main__':
    
    with open('pharma/goldenhealth_official_store/search_items.json', 'r') as f: 
        data = json.load(f)['items']
        os.makedirs(os.path.join('output', "goldenhealth_official_store"), exist_ok=True)
        already_crawled = os.listdir(os.path.join('output', "goldenhealth_official_store"))
        shopee_crawler = ShopeeCrawler_API()
        output = dict() 
        
        for item in tqdm(data): 
            item_id = str(item["itemid"])
            shop_id = str(item["shopid"])
            if item_id + '.json' in already_crawled:
                continue
            
            item_details = dict() 

            
            item_dict = shopee_crawler.crawl_item(shop_id, item_id, already_crawled)
            if item_dict:
                shopee_crawler.write_to_file("goldenhealth_official_store", item_dict)
                already_crawled.add(item_id + '.json')
