from crawler import ShopeeCrawler_API
import utils

import time


if __name__ == '__main__':
    print("hello world")
    lst_itemid = set()
    crawler = ShopeeCrawler_API()
    terms = [
        "skincare",
        "sửa rửa mặt", 
        "toner", 
        "serum", 
        "essence"
    ]
    
    lst_itemid = utils.get_existed_item_list()
    
    for term in terms:
        crawler.crawl_by_terms(term, lst_itemid)
    # time.sleep(10)
    # crawler.extract_item_information("https://shopee.vn/product/292513909/3646115183/")
    # crawler.extract_comments_from_shopee_api("274028659", "5945693195")
    # crawler.craw_item("https://shopee.vn/product/274028659/5945693195")
    # crawler.extract_item_information("https://shopee.vn/product/194923909/15103850849")
    # crawler.__close_connection__()
    
    # item_dict = crawler.crawl_item("58647841", "3937198463")
    # crawler.write_to_file("serum", item_dict)
    
    
    