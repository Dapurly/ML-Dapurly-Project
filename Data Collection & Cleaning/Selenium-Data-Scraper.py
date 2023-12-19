import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re

# Function to initialize the WebDriver
def init_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver

# Function to scrape data for a given keyword
def scrape_data(driver, keyword):
    print(f"Processing keyword: {keyword}")
    driver.get("https://shopping.google.com/")
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.send_keys(keyword + Keys.RETURN)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sh-pr__product-results-grid")))

    items = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-docid]")))

    all_titles = []
    all_quantities = []
    all_prices = []

    for item in items[:30]:  # Processing first 30 items for each keyword
        try:
            title = item.find_element(By.CSS_SELECTOR, 'div.EI11Pd h3.tAxDx').text
            price = item.find_element(By.CSS_SELECTOR, 'span.a8Pemb.OFFNJ').text
            price_text = re.sub(r'[^\d,.]', '', price)

            quantity_match = re.search(r'\b\d+\s*(kg|g|l|ml)\b', title, re.IGNORECASE)
            if quantity_match and keyword.lower() in title.lower():
                all_titles.append(title)
                all_quantities.append(quantity_match.group(0))
                all_prices.append(price_text)

        except Exception as e:
            print(f"Error processing item for {keyword}: {e}")

    print(f"Keyword '{keyword}' processed. {len(all_titles)} items found.")
    return keyword, all_titles, all_quantities, all_prices

# Function to save data to an Excel file
def save_to_excel(data, filepath):
    df = pd.DataFrame(data)
    df.to_excel(filepath, index=False)

# Main script execution
def main():
    file_path = 'harga_bahan.xlsx'  # Replace with the actual path to your Excel file
    df = pd.read_excel(file_path)

    output_filepath = 'finalized_cleaned_data.xlsx'  # Output file
    data = {'nama_bahan': [], 'nama_bahan_mentah': [], 'jumlah_bahan_mentah': [], 'harga_bahan_mentah': []}

    driver = init_driver()

    for keyword in df['nama_bahan']:
        try:
            keyword, names, quantities, prices = scrape_data(driver, keyword)
            data['nama_bahan'].append(keyword)
            data['nama_bahan_mentah'].append(names)
            data['jumlah_bahan_mentah'].append(quantities)
            data['harga_bahan_mentah'].append(prices)

            # Save data to Excel after processing each keyword
            save_to_excel(data, output_filepath)
        except Exception as e:
            print(f"Error processing keyword {keyword}: {e}")
            continue  # Continue with the next keyword in case of an error

    driver.quit()
    print("Data scraping completed.")

# Run the main script
main()
