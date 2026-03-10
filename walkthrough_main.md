# Walkthrough: main.py

The `main.py` file acts as the primary controller for this data scraping project. It implements a robust workflow using Playwright to navigate the Flipkart website and coordinate the extraction and saving processes.

## Step-by-Step Logic

### 1. Initialization and Imports
```python
from playwright.sync_api import sync_playwright
from get_electronics_cat import get_device_data
from save_to_db import save_to_postgres, save_to_csv
```
The script begins by importing Playwright for browser automation, the data extraction logic from `get_electronics_cat.py`, and the database saving functions from `save_to_db.py`.

### 2. Defining Categories
```python
def getFlipkartData():
    categories = ["laptop", "mobile", "tablet", "monitor", "camera"]
```
It defines a list of five distinct electronic product categories to scrape data for. This simple list guides the main loop.

### 3. Launching the Browser
```python
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.flipkart.com/")
```
Playwright spins up a Chromium browser (visible to the user, not headless) and navigates to the Flipkart homepage. 

### 4. Handling Popups safely
```python
        close_btn = page.query_selector('span[role="button"].b3wTlE')
        if close_btn:
            close_btn.click()
```
Flipkart often displays a login popup perfectly obstructing the page. Playwright attempts to find the "Close" button using its CSS class and clicks it if it is displayed.

### 5. Iterating Over Categories
The script enters a master `for` loop, dynamically creating search URLs:
```python
        for category in categories:
            page_num = 1
            while True:
                next_url = f"https://www.flipkart.com/search?q={category}&page={page_num}"
                page.goto(next_url)
```
Instead of manually typing into search bars, Playwright navigates directly to the proper URL parameters, `?q=[keyword]&page=[num]`, ensuring clean traversal entirely bypassing Flipkart's potentially volatile UI.

### 6. Calling the Extraction Logic
```python
                current_page_devices = get_device_data(page, category_name=category.capitalize())
```
With the fully loaded catalog page, the active `page` context is injected straight into the `get_device_data` function inside `get_electronics_cat.py`.

### 7. Verifying Termination and Safeguards
```python
                if len(current_page_devices) == 0:  
                    break
```
If the extraction yields literally `0` items, the project assumes it has struck the end of Flipkart's search results or bumped back to the first page incorrectly, safely breaking the `while` loop to progress to the next category.
Additionally, a strict `if page_num > 40: break` safeguard is implemented to cap resource usage and prevent infinite scraping traps over ambiguous URLs.

### 8. Finalizing the Output
```python
        save_to_postgres(all_devices)
        save_to_csv(all_devices, "flipkart_electronics.csv")
        browser.close()
```
When all categories yield all possible valid paginations, the massive `all_devices` list is finally processed identically by both Postgres and CSV functions to finalize the task.
