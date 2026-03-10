# Walkthrough: get_electronics_cat.py

The `get_electronics_cat.py` file holds the pure front-end DOM extraction logic for parsing products off a loaded Flipkart page snippet. It uses comprehensive CSS selector queries and regex text cleaning to safely structure messy web data.

## Step-by-Step Logic

### 1. Identifying the Universal Product Container
```python
    device_all = page.query_selector_all('div[data-id]')
```
Flipkart utilizes two distinct frontend React views: A **List View** for specific search categories (Mobiles/Laptops) and a **Grid View** (Monitors/Tablets). Using `div[data-id]` universally matches every single product unit regardless of view type layout padding classes. 

### 2. Multi-Class Fallback Querying
Since various elements share wildly different obfuscated CSS classes between grid and list views, the script implements wide multi-class searches using the comma syntax for standard DOM inspection:
```python
        try:
            title_el = device.query_selector('div.RG5Slk, div.KzDlHZ, a.WKTcLC, a.IRpwTa, a.s1Q9rs, a.wjcEIp, div.syl9yP')
```
If the first `div.RG5Slk` doesn't exist, playwright checks the next class `div.KzDlHZ` and so forth, effectively wrapping 5 distinct element shapes into a robust search strategy.

### 3. Capturing Prices
```python
        try:
            price_el = device.query_selector('div.hZ3P6w.DeU9vF, div.Nx93j0, div._30jeq3, div.hl05eU')
            current_price = price_el.inner_text() if price_el else "N/A"
```
It reliably pulls the deeply nested formatted string for current sale pricing. 

### 4. Parsing Rating Counts using Advanced String Manipulation
```python
                if 'Ratings' in rating_text and '&' in rating_text:
                    num_ratings = rating_text.split('Ratings')[0].strip()
                    num_reviews = rating_text.split('&')[1].replace('Reviews', '').strip()
                elif 'Ratings' in rating_text:
                    num_ratings = rating_text.split('Ratings')[0].strip()
```
The exact strings look messy like `"14,321 Ratings & 345 Reviews"`. The logic heavily relies on `split()` using the explicit string literals "Ratings" and "&" to separate them, or handles cases where products might dynamically only have Ratings and zero Reviews.

### 5. Cleaning Prices using Regular Expressions 
```python
        def format_price(price_str):
            if price_str == "N/A" or not price_str:
                return "N/A"
            match = re.search(r'[\d,]+', str(price_str))
            if match:
                return f"₹{match.group()}"
```
Python's built-in `re` strictly grabs numerical values with matching commas: `[\d,]+` completely disregarding surrounding messy unicode spaces, re-attaching a uniform Rupee `₹` symbol before dict injection.

### 6. Constructing and Returning the Dictionary
```python
        devices.append({
                "Category": category_name,
                "Title": device_title,
                "Current_Price": current_price,
...
            })
```
Finally, all heavily scrubbed textual strings are compiled directly into a cleanly formatted Python Dictionary. Appending the user-injected string `category_name` tags the dictionary unit natively to maintain identity parity when shipped downstream to Databases.
