import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from .notifier import send_notification
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Automatically install the correct ChromeDriver
chromedriver_autoinstaller.install()

# Load products CSV
df = pd.read_csv("products.csv", quotechar='"')  # columns: url,name,desired_price,last_price

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # comment this line to see the browser
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# List of standard price selectors
price_selectors = [
    "#priceblock_ourprice",
    "#priceblock_dealprice",
    "#priceblock_saleprice",
    ".a-price .a-offscreen",
    ".priceToPay .a-offscreen",
    ".apexPriceToPay .a-offscreen",
]

for index, row in df.iterrows():
    url = row['url'].strip()
    product_name = str(row.get('name', url))
    try:
        desired_price = float(row['desired_price'])
    except ValueError:
        print(f"Invalid desired price for {product_name}. Skipping.")
        continue

    print(f"\nChecking {product_name}...")
    print(f"URL: {url}")

    try:
        driver.get(url)
        time.sleep(2)  # small wait to ensure page loads

        price_text = None
        price_element = None

        # Try standard selectors first
        for selector in price_selectors:
            try:
                price_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if price_element and price_element.text.strip():
                    price_text = price_element.text
                    break
            except TimeoutException:
                continue

        # Fallback to a-price-whole + a-price-fraction
        if not price_text:
            try:
                whole = driver.find_element(By.CSS_SELECTOR, ".a-price-whole").text
                fraction = driver.find_element(By.CSS_SELECTOR, ".a-price-fraction").text
                price_text = f"{whole}.{fraction}"
            except NoSuchElementException:
                print(f"Price not found for {product_name}. Skipping.")
                continue

        # Clean and convert price to float
        price_text = price_text.replace("$", "").replace(",", "").strip()
        try:
            current_price = float(price_text)
        except ValueError:
            print(f"Could not convert price text '{price_text}' for {product_name}. Skipping.")
            continue

        print(f"Current price of {product_name}: ${current_price}")
        df.at[index, 'last_price'] = current_price

        # Send notification if price is below desired
        if current_price <= desired_price:
            print(f"Price alert! {product_name} is now ${current_price}")
            send_notification(product_name, url, current_price)

    except Exception as e:
        print(f"Error checking {product_name}: {e}")

# Quit browser and save CSV
driver.quit()
df.to_csv("products.csv", index=False)
print("\nDone checking all products.")
