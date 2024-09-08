from flask import Flask, request, jsonify, render_template
import json
import requests
from scrapy.crawler import CrawlerRunner
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../spiders')))
from spiders import scraping, run_scrapy
import time
from twisted.internet import reactor
from multiprocessing import Process

app=Flask(__name__)
crawl_runner = CrawlerRunner()

def wait_for_file(filepath, timeout=60, check_interval=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            return True
        time.sleep(check_interval)
    return False

def run_spiders(item):
    runner = CrawlerRunner()
    runner.crawl(scraping.AmazonSpider, item=item)
    runner.crawl(scraping.noonSpider, item=item)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/search', methods=['GET','POST'])
def search():
   try:
      if request.method == 'POST': 
         text = request.form.get('textarea')
         p = Process(target=run_spiders, args=(text,))
         p.start()
         p.join()
         run_scrapy.search() 
         if wait_for_file('products.json'):
            return result()
      else:
         return "Data not ready yet, please try again later.", 503
   except:
      return "Please try again :("


@app.route('/products',methods=['GET'])
def products():
   with open('products.json') as json_file:
    data = json.load(json_file)
   return jsonify(data)

@app.route('/result',methods=['GET','POST'])
def result():
   response=requests.get('http://127.0.0.1:5000/products')
   data=response.json()
   return render_template('comp.html', data=data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)