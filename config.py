SHOPEE_BASE_URL = 'https://shopee.vn/'
SHOPPE_PRODUCT_URL = 'https://shopee.vn/product/'

TERMS_SEARCH_URL = 'https://shopee.vn/search?keyword='

PAGINATION_POSTFIX = '&page='

SHOPEE_MAX_PAGE = 100

# SHOPEE_ITEM_XPATH_LINK = "//div[contains(@class, 'shopee-search-item-result__item')]/a"

REVIEW_CLASS = ".tuNfsN"

# https://shopee.vn/api/v2/item/get_ratings?filter=0&flag=1&itemid=3104821596&offset=1&shopid=172288895&type=0

SHOPEE_RATING_TYPE_LIST = {
    "1-star": 0,
    "2-star": 1,
    "3-start": 2,
    "4-start": 4,
    "5-start": 4
}

SHOPEE_API_RATINGS_MAX_REVIEWS = 59
SHOPEE_API_RATINGS = "https://shopee.vn/api/v2/item/get_ratings?itemid={}&offset={}&shopid={}&limit={}"

SHOPEE_API_SEARCH_RElEVANCY = "https://shopee.vn/api/v4/search/search_items?by=relevancy&keyword={}&limit=60&newest={}&order=desc&page_type=search"
SHOPEE_API_SEARCH_BY_SHOP = "https://shopee.vn/api/v4/search/search_items?limit={}&match_id={}&newest=0&page_type=shop"


SHOPEE_PRODUCT_INFORMATION = "https://shopee.vn/api/v4/item/get?shopid={}&itemid={}"

HASAKI_API_RATINGS = "https://hasaki.vn/ajax?api=product.getRatingMore&id={}&offset={}&sort=date"
HASAKI_URL_PRODUCT = "https://hasaki.vn/san-pham/abc-{}.html"
HASAKI_API_FAQS = "https://hasaki.vn/ajax?api=product.getQuestionMore&id={}&offset={}"