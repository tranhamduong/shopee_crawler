#============# TIKI #============#
TIKI_PRODUCT_URL = "https://tiki.vn/j-p{}.html"
TIKI_PRODUCT_RATINGS_API = "https://tiki.vn/api/v2/reviews?limit={}&include=comments&page=1&product_id={}"
TIKI_PRODUCT_DETAILS_API = "https://tiki.vn/api/v2/products/{}?platform=web"

TIKI_CATEGORY_ID_THUCPHAMCHUCNANG = "2322"
TIKI_PRODUCT_LISTING_CATEGORY = "https://tiki.vn/api/personalish/v1/blocks/listings?limit=100&category={}&page={}"


#============# SHOPEE #============#
SHOPPE_PRODUCT_URL = 'https://shopee.vn/product/'
SHOPPE_PRODUCT_RATINGS_API = "https://shopee.vn/api/v2/item/get_ratings?itemid={}&offset={}&shopid={}&limit={}"
SHOPPE_PRODUCT_DETAILS_API = "https://shopee.vn/api/v4/item/get?shopid={}&itemid={}"
SHOPEE_SEARCH_RElEVANCY_API = "https://shopee.vn/api/v4/search/search_items?by=relevancy&keyword={}&limit=60&newest={}&order=desc&page_type=search" 
SHOPEE_SEARCH_BY_SHOP_API = "https://shopee.vn/api/v4/search/search_items?limit={}&match_id={}&newest=0&page_type=shop"

#============# HASAKI #============#
HASAKI_PRODUCT_URL = "https://hasaki.vn/san-pham/abc-{}.html"
HASAKI_PRODUCT_RATINGS_API = "https://hasaki.vn/ajax?api=product.getRatingMore&id={}&offset={}&sort=date"
HASAKI_PRODUCT_FAQS_API = "https://hasaki.vn/ajax?api=product.getQuestionMore&id={}&offset={}"


#============# CONVERTING_KEY_DICT #============#


TIKI_MAX_COMMENTS_TO_FETCH = 1000
TIKI_MAX_LISTING_PAGE_TO_FETCH = 85

SHOPEE_RATINGS_API_MAX_RETURNED = 59
SHOPEE_SEARCH_BY_TERM_MAX_RETURNED = 60
SHOPEE_SEARCH_BY_SHOPID_RETURNED = 90

BROWSER_HEADER = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0',
    'referer': 'https://shopee.vn/'
}