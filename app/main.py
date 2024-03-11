import requests
from bs4 import BeautifulSoup

# URL of the item
url = 'http://example.com/item'

# Make a request to get the webpage
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find the element containing the stock status
stock_status_element = soup.find('elementContainingStockStatus', class_='classOfTheElement')

# Check if the item is in stock
if stock_status_element and 'In Stock' in stock_status_element.text:
    print("Item is in stock.")
else:
    print("Item is out of stock.")
