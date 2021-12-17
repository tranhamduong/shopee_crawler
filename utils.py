import config
import os 

def get_product_url(url):
    ab= url.split("-i.")[-1].split("?")[0].split(".")
    
    return config.SHOPPE_PRODUCT_URL + ab[0] + '/' + ab[1] + '/'

def extract_from_url(url): 
    # url = https://shopee.vn/product/292513909/3646115183/
    
    return url.split("/")[4], url.split("/")[5]

if __name__ == '__main__':
    # x = process_url('https://shopee.vn/Serum-gi%E1%BA%A3m-m%E1%BB%A5n-th%C3%A2m-r%E1%BB%97-Seimy-Skin-7-Days-C%C3%B4ng-d%E1%BB%A5ng-5-trong-1-hi%E1%BB%87u-qu%E1%BA%A3-sau-7-ng%C3%A0y-i.292513909.3646115183?sp_atk=da5c1dae-1387-47b6-9360-69f0b88d2f46')
    # print(x)
    pass 