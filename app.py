from crawler import ShopeeCrawler_API

import time


if __name__ == '__main__':
    print("hello world")
    
    crawler = ShopeeCrawler_API()
    terms = [
        'serum',
        # 'toner'
    ]
    for term in terms:
        crawler.crawl_by_terms(term)
    # time.sleep(10)
    # crawler.extract_item_information("https://shopee.vn/product/292513909/3646115183/")
    # crawler.extract_comments_from_shopee_api("274028659", "5945693195")
    # crawler.craw_item("https://shopee.vn/product/274028659/5945693195")
    # crawler.extract_item_information("https://shopee.vn/product/194923909/15103850849")
    # crawler.__close_connection__()