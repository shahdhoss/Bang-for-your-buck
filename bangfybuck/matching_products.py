import json
import csv
from ml_model_training import predict

with open('amazon.json') as amazon_file:
    amazon_json = json.load(amazon_file)
amazon_titles = []
amazon_prices = []
amazon_prod = []
for item in amazon_json:
    amazon_titles.append(item['name'])
    amazon_prices.append(item['price'])
    amazon_prod.append(item['href'])

with open("noon.json") as noon_file:
    noon_json = json.load(noon_file)
noon_titles = []
prices = []
product_ref = []
for item in noon_json:
    noon_titles.append(item['name'])
    prices.append(item['price'])
    product_ref.append(item['href'])

matched_products = []
for noonItem in range(len(noon_titles)):
    for amazonItem in range(len(amazon_titles)):
        result = predict.predicts(noon_titles[noonItem], amazon_titles[amazonItem])
        if result == 'matching':
            matched_products.append({
                'original_product': noon_titles[noonItem],
                'best_match': amazon_titles[amazonItem],
                'noon_ref': product_ref[noonItem],
                'noon_prices': prices[noonItem],
                'amazon_ref': amazon_prod[amazonItem],
                'amazon_prices': amazon_prices[amazonItem]
            })
with open("bang-for-your-buck\\bangfybuck\\products.csv", "w", newline="") as file:
    writer = csv.writer(file)
    field = ["original_product", "best_match", "noon_ref", "noon_prices", "amazon_ref", "amazon_prices"]
    writer.writerow(field)
    for item in matched_products:
        writer.writerow([
            item['original_product'],
            item['best_match'],
            item['noon_ref'],
            item['noon_prices'],
            item['amazon_ref'],
            item['amazon_prices']
        ])