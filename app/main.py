import requests
from urllib.parse import urlparse, parse_qs
import time
import sys
from bs4 import BeautifulSoup

def get_product_details_from_url(url):
    """Extracts product details from a given Best Buy product URL."""
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
    """Checks if the product is in stock."""

    headers = {
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36', 
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': url,
        'accept-language': 'en-US,en;q=0.5'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"An error occurred while checking stock status: {response.status_code} {response.reason}")
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        stock_status_element = soup.find('button', {"data-sku-id": sku_id})

        return True
    
def main():
    """Main function to monitor product stock status."""
    if len(sys.argv) > 1:
        user_url = sys.argv[1]
    else:
        user_url = input("Enter the Best Buy product URL: ")
    
    try:
        product_details = get_product_details_from_url(user_url, )
        product_url = f"{product_details['base_url']}/site/{product_details['product_name']}/{product_details['product_id']}.p?skuId={product_details['sku_id']}"

        print("Monitoring stock status. Press Ctrl+C to stop.")
        
        while True:
            in_stock = check_stock(product_url, product_details['sku_id'])

            if in_stock:
                print("The item is in stock.")
                break
            else:
                print("The item is out of stock. Checking again in 10 seconds...")
                time.sleep(10)

    except ValueError as e:
        print(f"An error occurred while checking stock status")
    except KeyboardInterrupt:
        print("Stopped the stock checker.")

if __name__ == "__main__":
    main()
