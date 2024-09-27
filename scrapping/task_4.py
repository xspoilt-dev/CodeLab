import requests
from bs4 import BeautifulSoup
import sys

def extract_products(html):
    soup = BeautifulSoup(html, 'html.parser')
    products = []
    
    for item in soup.select('.p-item'):
        name = item.select_one('.p-item-name a').text.strip()
        price = item.select_one('.p-item-price span').text.strip()
        link = item.select_one('.p-item-name a')['href']
        
        products.append({
            'name': name,
            'price': price,
            'link': link
        })
    
    return products

keyword = "laptop"
crawl_count = 20
page_number = 1
all_products = []

while page_number <= crawl_count:
    url = f'https://www.startech.com.bd/product/search?&search={keyword}&page={page_number}'
    resp = requests.get(url).text
    products = extract_products(resp)
    all_products.extend(products)
    page_number += 1

sys.stdout.reconfigure(encoding='utf-8')

for product in all_products:
    print(f"Name: {product['name']}")
    print(f"Price: {product['price']}")
    print(f"Link: {product['link']}")
    print('-----------------------')