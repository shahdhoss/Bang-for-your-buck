import Levenshtein
import json
from scraping import AmazonSpider,noonSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def levenshtein_ratio(s1, s2):
    return Levenshtein.ratio(s1, s2)

def search():
    # settings = get_project_settings()
    # process = CrawlerProcess(settings)
    # process.crawl(noonSpider, item=item)
    # process.crawl(AmazonSpider, item=item)
    # process.start()  
    with open('amazon.json') as amazon_file:
        amazon_json = json.load(amazon_file)
    amazon_titles = []
    amazon_prices = []
    amazon_prod = []
    amazon_pic=[]
    amazon_ship=[]
    for item in amazon_json:
        amazon_titles.append(item['name'])
        amazon_prices.append(item['price'])
        amazon_prod.append(item['href'])
        amazon_pic.append(item['picture'])
        amazon_ship.append(item['shipping'])
    with open('noon.json') as noon_file:
        noon_json = json.load(noon_file)
    noon_titles = []
    prices = []
    product_ref = []
    noon_pic=[]
    noon_ship=[]
    for item in noon_json:
        noon_titles.append(item['name'])
        prices.append(item['price'])
        product_ref.append(item['href'])
        noon_pic.append(item['picture'])
        noon_ship.append(item['shipping'])
    matched_products = []
    for noonItem in range(len(noon_titles)):
        best_match = None
        best_score = 0
        noon_ref = product_ref[noonItem]
        noon_price = prices[noonItem]
        og_product = noon_titles[noonItem]
        picture=noon_pic[noonItem]
        shipment= noon_ship[noonItem]
        for amazonItem in range(len(amazon_titles)):
            score = levenshtein_ratio(noon_titles[noonItem], amazon_titles[amazonItem])
            if score > best_score:
                best_score = score
                best_match = amazon_titles[amazonItem]
                amazon_ref = amazon_prod[amazonItem]
                amazon_price = amazon_prices[amazonItem]
                amazon_picture=amazon_pic[amazonItem]
                amazon_ship_dur=amazon_ship[amazonItem]
        matched_products.append({
            'noon_prod': og_product,
            'noon_ref': noon_ref,
            'noon_price': noon_price,
            'noon_pic':picture,
            'noon_ship': shipment,
            'amazon_prod': best_match,
            'amazon_ref': amazon_ref,
            'amazon_price': amazon_price,
            'amazon_pic': amazon_picture,
            'amazon_ship': amazon_ship_dur,
            'similarity_score': best_score
        })
    matched_products.sort(key=lambda x: x["similarity_score"], reverse=True)
    json_object = json.dumps(matched_products, indent=4)
    with open('products.json', "w") as outfile:
        outfile.write(json_object)
#search('makeup')
