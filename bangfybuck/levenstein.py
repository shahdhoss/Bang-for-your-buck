import Levenshtein
import json
import csv

def levenshtein_ratio(s1, s2):
    return Levenshtein.ratio(s1, s2)

with open('bangfybuck\\amazon.json') as amazon_file:
    amazon_json = json.load(amazon_file)
amazon_titles = []
amazon_prices = []
amazon_prod = []
for item in amazon_json:
    amazon_titles.append(item['name'])
    amazon_prices.append(item['price'])
    amazon_prod.append(item['href'])

with open("bangfybuck\\noon.json") as noon_file:
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
    best_match = None
    best_score = 0
    noon_ref = product_ref[noonItem]
    noon_price = prices[noonItem]
    og_product = noon_titles[noonItem]
    for amazonItem in range(len(amazon_titles)):
        score = levenshtein_ratio(noon_titles[noonItem], amazon_titles[amazonItem])
        if score > best_score:
            best_score = score
            best_match = amazon_titles[amazonItem]
            amazon_ref = amazon_prod[amazonItem]
            amazon_price = amazon_prices[amazonItem]
    
    matched_products.append({
        'original_product': og_product,
        'best_match': best_match,
        'similarity_score': best_score,
        'noon_ref': noon_ref,
        'noon_prices': noon_price,
        'amazon_ref': amazon_ref,
        'amazon_prices': amazon_price
    })
with open("bangfybuck\\products.csv", "w", newline="") as file:
    writer = csv.writer(file)
    field = ["original_product", "best_match", "similarity_score", "noon_ref", "noon_prices", "amazon_ref", "amazon_prices"]
    writer.writerow(field)
    for item in matched_products:
        writer.writerow([
            item['original_product'],
            item['best_match'],
            item['similarity_score'],
            item['noon_ref'],
            item['noon_prices'],
            item['amazon_ref'],
            item['amazon_prices']
        ])