import scrapy
import json
import scrapy.resolver

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
            if name and price and reference:
                item_data = {
                    "name": (brand + " " if brand else "") + name,
                    "price": price,
                    "href": response.urljoin(reference)
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
    def __init__(self, item: str, page_limit=4, *args, **kwargs):
        super(noonSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.noon.com/egypt-en/search/?q={item}&language=en']
        self.noon_data = []  
        self.page_count = 0  
        self.page_limit = page_limit 

    def parse(self, response):
        self.page_count += 1  
        names = response.css(".sc-26c8c6bb-24.cCbHzm::attr(title)").getall()
        prices = response.css(".amount::text").getall()
        references = response.css("a[id^='productBox']::attr(href)").getall()
        for i in range(len(names)):
            item_data = {
                "name": names[i],
                "price": prices[i],
                "href": response.urljoin(references[i]) 
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
        else:
                json_object = json.dumps(self.noon_data, indent=4)
                with open("noon.json", "w") as outfile:
                    outfile.write(json_object)
            

