from flask import Flask, render_template, request
import json
import os
from collections import defaultdict

app = Flask(__name__)

# Load products from single JSON file
def load_products():
    with open('products.json', 'r') as file:
        return json.load(file)

@app.route('/')
def home():
    products = load_products()
    # Sort products by ranking (higher first) and take top 5
    top_products = sorted(products, key=lambda x: x.get('ranking', 0), reverse=True)[:5]
    return render_template('index.html', products=top_products)

@app.route('/brands')
def brands():
    products = load_products()
    brand_map = defaultdict(list)
    for p in products:
        brand_map[p['brand']].append(p)
    return render_template('brands.html', brands=brand_map)

@app.route('/brand/<brand_name>')
def brand_detail(brand_name):
    products = load_products()
    filtered = [p for p in products if p['brand'].lower() == brand_name.lower()]
    return render_template('category.html', products=filtered, category=brand_name)

@app.route('/categories')
def categories():
    products = load_products()
    category_map = defaultdict(list)
    for p in products:
        category_map[p['category']].append(p)
    return render_template('categories.html', categories=category_map)

@app.route('/product/<product_id>')
def product_detail(product_id):
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    return render_template('product.html', product=product)

@app.route('/marketing/<product_id>')
def marketing(product_id):
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    return render_template('marketing.html', product=product)

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    products = load_products()
    results = [p for p in products if query in p['title'].lower() or query in p['description'].lower() or query in p['brand'].lower()]
    return render_template('search_results.html', products=results, query=query)

if __name__ == '__main__':
    app.run(debug=True)
