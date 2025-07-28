from bs4 import BeautifulSoup
import requests
import csv
import time
from datetime import datetime
import os

# 'url' stores the link to the item needed
# Headers to mimic a real browser request and avoid Amazon's bot detection. Contains User-Agent, language preferences, and other HTTP headers
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
}
url = "https://www.amazon.com/adidas-Mens-Falcon-Sneaker-White/dp/B0D3NW5LL7?ref_=pd_bap_d_grid_rp_0_1_ec_pd_hp_d_atf_rp_4_i&psc=1"

def scrape_product():
    # First request to get HTML content
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Second parse for product title
    soup1 = BeautifulSoup(soup.prettify(), "html.parser")
    title = soup1.find(id='productTitle').get_text().strip()

    # Third parse for price components
    soup2 = BeautifulSoup(soup.prettify(), "html.parser")

    # Extract price components
    currency_symbol = soup2.find("span", class_="a-price-symbol")
    whole_part = soup2.find("span", class_="a-price-whole")
    fraction_part = soup2.find("span", class_="a-price-fraction")

    # Combine the price components into one varieble `price` and clean it. '$' symbol was removed for easier use with integer 'price' values
    if currency_symbol and whole_part and fraction_part:
        price = (
                whole_part.get_text(strip=True) + 
                fraction_part.get_text(strip=True)
            )
    else:
        price = "Price not found"
    
    # Extract the date and time when the price was detected
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return title, price, today

# Check if the file is already there. If not, create a .csv file to store the data set
def create_csv():
    if not os.path.exists("C:/Users/user/Desktop/AmazonWebScraperDataset.csv"):
        with open("C:/Users/user/Desktop/AmazonWebScraperDataset.csv", 'w', newline='', encoding='UTF8') as f:
            csv.writer(f).writerow(['Title', 'Price', 'Date'])

# Add new data rows to data set when the time comes
def append_to_csv(title, price, today):
    data = [title, price, today]
    with open("C:/Users/user/Desktop/AmazonWebScraperDataset.csv", 'a+', newline='', encoding='UTF8') as file:
        dataset = csv.writer(file)
        dataset.writerow(data)

# Is like a main function to utilize the defined functions and add new rows
def job():
    title, price, today = scrape_product()
    if title is None:
        return
    append_to_csv(title, price, today)

# Calling main functions. `create_csv` will run only the first time to create the date set but never again
create_csv()
job()

# Start a while loop that repeats the same steps every 24 hours
while True:
    job()
    time.sleep(86400)