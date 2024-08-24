import scrapy
import json

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.eg"]

    def __init__(self, item: str, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.amazon.eg/s?k={item}&language=en']

    def parse(self, response):
        names = response.css(".a-size-base-plus.a-color-base.a-text-normal::text").getall()
        prices = response.css(".a-price-whole::text").getall()
        references = response.css("a.s-no-outline::attr(href)").getall()
        amazon_data = []
        for i in range(len(names)):
            item_data = {
                "name": names[i],
                "price": prices[i],
                "href": response.urljoin(references[i]) 
            }
            amazon_data.append(item_data)
        json_object=json.dumps(amazon_data, indent=4)
        with open("amazon.json", "w") as outfile:
            outfile.write(json_object)

class noonSpider(scrapy.Spider):
    name = "noon"
    def __init__(self, item: str, *args, **kwargs):
        super(noonSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.noon.com/egypt-en/search/?q={item}&language=en']

    def parse(self, response):
        names = response.css(".sc-26c8c6bb-24.cCbHzm::attr(title)").getall()
        prices= response.css(".amount::text").getall()
        references= response.css("a[id^='productBox']::attr(href)").getall()
        noon_data = []
        for i in range(len(names)):
            item_data = {
                "name": names[i],
                "price": prices[i],
                "href": response.urljoin(references[i]) 
            }
            noon_data.append(item_data)
        json_object=json.dumps(noon_data, indent=4)
        with open("noon.json", "w") as outfile:
            outfile.write(json_object)
