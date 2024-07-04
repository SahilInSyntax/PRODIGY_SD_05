import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL of the website to scrape
url = 'https://www.amazon.com/s?k=your+search+term'

# Send an HTTP request to the URL
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(url, headers=headers)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract product information
products = []
for item in soup.find_all('div', {'data-component-type': 's-search-result'}):
    name = item.h2.text
    try:
        price = item.find('span', 'a-price-whole').text
        price_fraction = item.find('span', 'a-price-fraction').text
        price = price + price_fraction
    except AttributeError:
        price = None
    try:
        rating = item.find('span', 'a-icon-alt').text
    except AttributeError:
        rating = None
    products.append({'name': name, 'price': price, 'rating': rating})

# Create a DataFrame and save to CSV
df = pd.DataFrame(products)
df.to_csv('products.csv', index=False)

print('Scraping completed and data saved to products.csv')
