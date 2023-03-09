import config 

def make_shopee_product_url(shop_id, item_id):
    return config.SHOPPE_PRODUCT_URL + str(shop_id) + '/' + str(item_id) + '/'
    