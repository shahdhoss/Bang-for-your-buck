from flask import Flask, request, jsonify, render_template
import json
import requests
# from spiders import run_scrapy

app=Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/search', methods=['GET','POST'])
def search():
   if request.method == 'POST': 
      text = request.form.get('textarea')
   # run_scrapy.search(text) 
   return render_template('comp.html') 

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