import scrapy
import json
import scrapy.resolver
import scrapy
import json
from noon_images_api import noon_api

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.eg"]

    def __init__(self, item: str, page_limit=1, *args, **kwargs):
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
            shipping = product.css(".a-row.a-size-base.a-color-secondary.s-align-children-center span span::text").get()
            if not picture:
                picture = product.css('img.s-image::attr(data-src)').get()
            if name and price and reference and picture:
                name=(brand + " " if brand else "") + name
                item_data = {
                    "name": name if len(name) < 70 else name[:70] + '...',
                    "price": price,
                    "href": response.urljoin(reference),
                    'picture': picture,
                    'shipping': 'Free Delivery' if shipping else ""
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


def search():
    with open('noon.json','r') as noon_json:
        noon_data=json.load(noon_json)
    with open('noon_images.json','r') as noon_images:
        noon_images=json.load(noon_images)
    for fitem in noon_data:
        for sitem  in noon_images:
            if(fitem['name_for_search']==sitem['name']):
                fitem['picture']=sitem['picture']
            if ("free_delivery_eligible" in sitem['flags']):
                fitem['shipping']= 'Free Delivery'
            else:
                fitem['shipping']=""
    with open('noon.json', 'w') as noon_json:
        json.dump(noon_data, noon_json, indent=4)  # indent=4 makes it more readable

class noonSpider(scrapy.Spider):
    name = "noon"
    def __init__(self, item: str, page_limit=1, *args, **kwargs):
        super(noonSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.noon.com/egypt-en/search/?q={item}&language=en']
        self.noon_data = []  
        self.page_count = 0  
        self.page_limit = page_limit 
        self.item=item
    def parse(self, response):
        noon_api(self.item)
        self.page_count += 1  
        products = response.css(".sc-19767e73-0.bwele")
        for product in products:
            name = product.css(".sc-26c8c6bb-24.cCbHzm::attr(title)").get()
            price = product.css(".amount::text").get()
            reference = product.css("a[id^='productBox']::attr(href)").get()
            if name and price and reference:
                item_data = {
                    "name": name if len(name) < 70 else name[:70] + '...',
                    "name_for_search":name,
                    "price": price,
                    "href": response.urljoin(reference),
                    'picture':None,
                    'shipping':None
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
                search()
        else:
            json_object = json.dumps(self.noon_data, indent=4)
            with open("noon.json", "w") as outfile:
                outfile.write(json_object)
            search()