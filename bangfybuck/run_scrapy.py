from scrapy.crawler import CrawlerProcess
from spiders.scraping import noonSpider, AmazonSpider
from scrapy.utils.project import get_project_settings

item="adidas shoes"
settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(noonSpider, item=item)
process.crawl(AmazonSpider, item=item)
process.start()  