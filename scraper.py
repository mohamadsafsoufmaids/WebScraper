import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def scroll_page(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_product_data(driver, product_element):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        title = product_element.find_element(By.CSS_SELECTOR, "h3.dne-itemtile-title").text.strip()
    except NoSuchElementException:
        title = "N/A"
    
    try:
        price_elem = product_element.find_element(By.CSS_SELECTOR, ".dne-itemtile-price")
        price = price_elem.text.strip()
    except NoSuchElementException:
        price = "N/A"
    
    try:
        original_price_elem = product_element.find_elements(By.CSS_SELECTOR, ".dne-itemtile-original-price")
        if original_price_elem:
            original_price = original_price_elem[0].text.strip()
        else:
            original_price = "N/A"
    except NoSuchElementException:
        original_price = "N/A"
    
    try:
        shipping_elem = product_element.find_elements(By.CSS_SELECTOR, ".dne-itemtile-delivery")
        if shipping_elem:
            shipping = shipping_elem[0].text.strip()
        else:
            shipping = "N/A"
    except NoSuchElementException:
        shipping = "N/A"
    
    try:
        link_elem = product_element.find_element(By.CSS_SELECTOR, "a")
        item_url = link_elem.get_attribute("href")
    except NoSuchElementException:
        item_url = "N/A"
    
    return {
        "timestamp": timestamp,
        "title": title,
        "price": price,
        "original_price": original_price,
        "shipping": shipping,
        "item_url": item_url
    }

def scrape_ebay_deals():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get("https://www.ebay.com/globaldeals/tech")
        time.sleep(3)
        
        scroll_page(driver)
        time.sleep(2)
        
        products = driver.find_elements(By.CSS_SELECTOR, ".ebayui-dne-summary-card__wrapper")
        
        file_exists = False
        try:
            with open("ebay_tech_deals.csv", "r"):
                file_exists = True
        except FileNotFoundError:
            pass
        
        with open("ebay_tech_deals.csv", "a", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["timestamp", "title", "price", "original_price", "shipping", "item_url"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            for product in products:
                try:
                    data = extract_product_data(driver, product)
                    writer.writerow(data)
                except Exception:
                    continue
        
        print(f"Scraped {len(products)} products successfully")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_ebay_deals()

