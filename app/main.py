import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import time

def get_product_details_from_url(url):
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.strip('/').split('/')
    query_params = parse_qs(parsed_url.query)

    if len(path_segments) >= 3 and 'skuId' in query_params:
        return {
            'base_url': f"{parsed_url.scheme}://{parsed_url.netloc}",
            'product_name': path_segments[1],
            'product_id': path_segments[2].split('.')[0],
            'sku_id': query_params['skuId'][0]
        }
    else:
        raise ValueError("URL does not match expected Best Buy product URL pattern.")

def check_stock(url, sku_id):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    stock_status_element = soup.find('button', {"data-sku-id": sku_id})
    
    if stock_status_element and "Add to Cart" in stock_status_element.text:
        return True
    return False

def main():
    user_url = input("Enter the Best Buy product URL: ")
    try:
        product_details = get_product_details_from_url(user_url)
        product_url = f"{product_details['base_url']}/site/{product_details['product_name']}/{product_details['product_id']}.p?skuId={product_details['sku_id']}"

        print("Monitoring stock status. Press Ctrl+C to stop.")
        
        # Loop indefinitely until the user stops the script or an item is found in stock.
        while True:
            in_stock = check_stock(product_url, product_details['sku_id'])

            if in_stock:
                print("The item is in stock.")
                break
            else:
                print("The item is out of stock or the check failed. Checking again in 10 seconds...")
                time.sleep(10)  # Wait for 10 seconds before the next check

    except ValueError as e:
        print(e)
    except KeyboardInterrupt:
        print("Stopped the stock checker.")

if __name__ == "__main__":
    main()
