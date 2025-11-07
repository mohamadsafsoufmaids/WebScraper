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
    scroll_attempts = 0
    max_scroll_attempts = 50
    
    while scroll_attempts < max_scroll_attempts:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
        last_height = new_height
        scroll_attempts += 1
    
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

def extract_product_data(driver, product_element):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Title - try multiple selectors
    title = "N/A"
    title_selectors = [
        "h3.ebayui-ellipsis-2",
        "h3.dne-itemtile-title",
        "h3[class*='title']",
        "h3",
        ".dne-itemtile-title",
        "[class*='title']"
    ]
    for selector in title_selectors:
        try:
            elem = product_element.find_element(By.CSS_SELECTOR, selector)
            if elem.text.strip():
                title = elem.text.strip()
                break
        except NoSuchElementException:
            continue
    
    # Price - try multiple selectors
    price = "N/A"
    price_selectors = [
        ".dne-itemtile-price",
        ".first",
        "[class*='price']",
        ".notranslate",
        "span[class*='price']"
    ]
    for selector in price_selectors:
        try:
            elem = product_element.find_element(By.CSS_SELECTOR, selector)
            text = elem.text.strip()
            if text and ("$" in text or "US $" in text or "£" in text or "€" in text):
                price = text
                break
        except NoSuchElementException:
            continue
    
    # Original price - try multiple selectors
    original_price = "N/A"
    original_price_selectors = [
        ".dne-itemtile-original-price",
        ".strikethrough",
        "[class*='original-price']",
        "[class*='strikethrough']",
        "span[class*='original']",
        ".ebayui-ellipsis-2 .strikethrough"
    ]
    for selector in original_price_selectors:
        try:
            elems = product_element.find_elements(By.CSS_SELECTOR, selector)
            for elem in elems:
                text = elem.text.strip()
                if text and ("$" in text or "US $" in text or "£" in text or "€" in text):
                    original_price = text
                    break
            if original_price != "N/A":
                break
        except NoSuchElementException:
            continue
    
    # Shipping - try multiple selectors
    shipping = "N/A"
    shipping_selectors = [
        ".dne-itemtile-delivery",
        ".u-flL.shipping",
        "[class*='shipping']",
        "[class*='delivery']",
        ".shipping",
        "span[class*='shipping']"
    ]
    for selector in shipping_selectors:
        try:
            elems = product_element.find_elements(By.CSS_SELECTOR, selector)
            for elem in elems:
                text = elem.text.strip()
                if text and len(text) > 0:
                    shipping = text
                    break
            if shipping != "N/A":
                break
        except NoSuchElementException:
            continue
    
    # URL
    item_url = "N/A"
    try:
        link_elem = product_element.find_element(By.CSS_SELECTOR, "a")
        href = link_elem.get_attribute("href")
        if href and "ebay.com" in href:
            item_url = href
    except NoSuchElementException:
        pass
    
    return {
        "timestamp": timestamp,
        "title": title,
        "price": price,
        "original_price": original_price,
        "shipping": shipping,
        "item_url": item_url
    }

def scrape_ebay_deals():
    import os
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    chrome_bin = os.environ.get('CHROME_BIN')
    chrome_paths = [
        '/usr/bin/google-chrome-stable',
        '/usr/bin/google-chrome',
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/snap/bin/chromium'
    ]
    
    if chrome_bin and os.path.exists(chrome_bin):
        options.binary_location = chrome_bin
    else:
        for path in chrome_paths:
            if os.path.exists(path):
                options.binary_location = path
                break
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get("https://www.ebay.com/globaldeals/tech")
        time.sleep(3)
        
        scroll_page(driver)
        time.sleep(3)
        
        
        products = driver.find_elements(By.CSS_SELECTOR, ".ebayui-dne-summary-card__wrapper")
        
        if len(products) == 0:
            products = driver.find_elements(By.CSS_SELECTOR, "[class*='dne-itemtile']")
        
        if len(products) == 0:
            products = driver.find_elements(By.CSS_SELECTOR, "[class*='itemtile']")
        
        if len(products) == 0:
            products = driver.find_elements(By.CSS_SELECTOR, "[data-testid*='item']")
        
        if len(products) == 0:
            products = driver.find_elements(By.CSS_SELECTOR, "article, [role='listitem']")
        
        file_exists = False
        try:
            with open("ebay_tech_deals.csv", "r"):
                file_exists = True
        except FileNotFoundError:
            pass
        
        products_scraped = 0
        with open("ebay_tech_deals.csv", "a", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["timestamp", "title", "price", "original_price", "shipping", "item_url"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            for product in products:
                try:
                    data = extract_product_data(driver, product)
                    if data["title"] != "N/A" or data["price"] != "N/A":
                        writer.writerow(data)
                        products_scraped += 1
                except Exception as e:
                    continue
        
        print(f"Scraped {products_scraped} products successfully out of {len(products)} found")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_ebay_deals()

