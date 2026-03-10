from playwright.sync_api import sync_playwright
from get_electronics_cat import get_device_data
from save_to_db import save_to_postgres, save_to_csv


def getFlipkartData():
    categories = ["laptop", "mobile", "tablet", "monitor", "camera"]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.flipkart.com/")

        page.wait_for_timeout(2500)
        
        # Handle login popup safely
        close_btn = page.query_selector('span[role="button"].b3wTlE')
        if close_btn:
            close_btn.click()
            
        page.wait_for_timeout(2500)
        
        all_devices = []
        
        for category in categories:
            print(f"Starting scraping for category: {category}")
            page_num = 1
            
            while True:
                next_url = f"https://www.flipkart.com/search?q={category}&page={page_num}"
                page.goto(next_url)
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(3000)
                
                print(f"Scraping {category} page {page_num}...")
                current_page_devices = get_device_data(page, category_name=category.capitalize())
                print(f"Scraped {len(current_page_devices)} items from {category} page {page_num}")
                
                if len(current_page_devices) == 0:
                    print(f"No items found on this page. Scraping finished for {category}.")
                    break
                    
                all_devices.extend(current_page_devices)
                
                page_num += 1
                # Maximum limit safeguard
                if page_num > 120:
                    break
                
        save_to_postgres(all_devices)
        save_to_csv(all_devices, "flipkart_electronics.csv")
        browser.close()


if __name__ == "__main__":
    getFlipkartData()