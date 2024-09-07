from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import Levenshtein
import json
import scrapy
import json
import scrapy.resolver
from bs4 import BeautifulSoup,SoupStrainer

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.eg"]

    def __init__(self, item: str, page_limit=4, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.amazon.eg/s?k={item}&language=en']
        self.amazon_data = []
        self.page_count = 0
        self.page_limit = page_limit

    def parse(self, response):
        self.page_count += 1
        products = response.css(".s-result-item")
        for product in products:
            name = product.css(".a-size-base-plus.a-color-base.a-text-normal::text").get()
            price = product.css(".a-price-whole::text").get()
            brand = product.css(".a-size-base-plus.a-color-base::text").get()
            reference = product.css("a.s-no-outline::attr(href)").get()
            picture = product.css('img.s-image::attr(src)').get()
            if not picture:
                picture = product.css('img.s-image::attr(data-src)').get()
            if name and price and reference and  picture:
                item_data = {
                    "name": name,
                    # "name": (brand + " " if brand else "") + name,
                    "price": price,
                    "href": response.urljoin(reference),
                    'picture': picture
                }
                self.amazon_data.append(item_data)
        if self.page_count < self.page_limit:
            next_button = response.xpath("//span[@class='s-pagination-strip']/a[contains(@class, 's-pagination-next')]")
            if next_button and next_button.xpath("@aria-disabled").get() != 'true':
                next_page_url = response.urljoin(next_button.xpath("@href").get())
                yield scrapy.Request(url=next_page_url, callback=self.parse)
            else:
                json_object = json.dumps(self.amazon_data, indent=4)
                with open("amazon.json", "w") as outfile:
                    outfile.write(json_object)
        else:
            json_object = json.dumps(self.amazon_data, indent=4)
            with open("amazon.json", "w") as outfile:
                outfile.write(json_object)

class noonSpider(scrapy.Spider):
    name = "noon"
    def __init__(self, item: str, page_limit=1, *args, **kwargs):
        super(noonSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.noon.com/egypt-en/search/?q={item}&language=en']
        self.noon_data = []  
        self.page_count = 0  
        self.page_limit = page_limit 
    def parse(self, response):
        self.page_count += 1  
        products = response.css(".sc-19767e73-0.bwele")
        for product in products:
            list_of_images=[]
            name = product.css(".sc-26c8c6bb-24.cCbHzm::attr(title)").get()
            price = product.css(".amount::text").get()
            reference = product.css("a[id^='productBox']::attr(href)").get()
            product_html = product.get()
            soup=BeautifulSoup(product_html, "html.parser")
            images = soup.find_all('img')
            for img in images:
                img_url = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
                list_of_images.append(img_url)
            if name and price and reference:
                item_data = {
                    "name": name,
                    "price": price,
                    "href": response.urljoin(reference),
                    'picture':list_of_images if list_of_images else 'No image available'
                }
                self.noon_data.append(item_data)

        if self.page_count < self.page_limit:
            next_button = response.xpath("//*[@id='__next']/div/section/div/div/div/div[2]/div[2]/div/ul/li[7]/a")
            if next_button and next_button.xpath("@aria-disabled").get() != 'true':
                next_page_url = response.urljoin(next_button.xpath("@href").get())
                yield scrapy.Request(url=next_page_url, callback=self.parse)
        else:
            json_object = json.dumps(self.noon_data, indent=4)
            with open("noon.json", "w") as outfile:
                outfile.write(json_object)

def levenshtein_ratio(s1, s2):
    return Levenshtein.ratio(s1, s2)

def search(item):
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(noonSpider, item=item)
    process.crawl(AmazonSpider, item=item)
    process.start()  

    with open('amazon.json') as amazon_file:
        amazon_json = json.load(amazon_file)
    amazon_titles = []
    amazon_prices = []
    amazon_prod = []
    amazon_pic=[]
    for item in amazon_json:
        amazon_titles.append(item['name'])
        amazon_prices.append(item['price'])
        amazon_prod.append(item['href'])
        amazon_pic.append(item['picture'])

    with open("noon.json") as noon_file:
        noon_json = json.load(noon_file)
    noon_titles = []
    prices = []
    product_ref = []
    noon_pic=[]
    for item in noon_json:
        noon_titles.append(item['name'])
        prices.append(item['price'])
        product_ref.append(item['href'])
        noon_pic.append(item['picture'])

    matched_products = []
    for noonItem in range(len(noon_titles)):
        best_match = None
        best_score = 0
        noon_ref = product_ref[noonItem]
        noon_price = prices[noonItem]
        og_product = noon_titles[noonItem]
        picture=noon_pic[noonItem]
        for amazonItem in range(len(amazon_titles)):
            score = levenshtein_ratio(noon_titles[noonItem], amazon_titles[amazonItem])
            if score > best_score:
                best_score = score
                best_match = amazon_titles[amazonItem]
                amazon_ref = amazon_prod[amazonItem]
                amazon_price = amazon_prices[amazonItem]
                amazon_picture=amazon_pic[amazonItem]
        matched_products.append({
            'noon_prod': og_product,
            'noon_ref': noon_ref,
            'noon_price': noon_price,
            'noon_pic':picture,
            'amazon_prod': best_match,
            'amazon_ref': amazon_ref,
            'amazon_price': amazon_price,
            'amazon_pic': amazon_picture,
            'similarity_score': best_score
        })
    matched_products.sort(key=lambda x: x["similarity_score"], reverse=True)
    json_object = json.dumps(matched_products, indent=4)
    with open('products.json', "w") as outfile:
        outfile.write(json_object)

search("makeup")