# Flipkart Product Scraper

## Overview
This project is an automated web scraper built with Python, Playwright, and BeautifulSoup. It dynamically navigates the Flipkart website to extract product information across multiple categories, handling pagination and login popups automatically. The extracted data is then processed and stored simultaneously in a PostgreSQL database and exported as a CSV file using Pandas.

## Features
- **Dynamic Web Scraping:** Uses **Playwright** to headlessly navigate the browser and wait for content loading.
- **Data Parsing:** Parses web page content to extract product titles, current prices, original prices, discounts, ratings, review counts, and features.
- **Categorical Scraping:** Pre-configured to scrape multiple key categories (e.g., laptop, mobile, tablet, monitor, camera).
- **Pagination Support:** Automatically iterates through multiple pages (up to 120 pages per category) until no more products are found.
- **Data Persistence (PostgreSQL):** Dynamically creates an `electronics` table and records the scraped data in a structured format into a local PostgreSQL database (`flipkart_2026`).
- **Data Persistence (CSV Export):** Generates a CSV backup format automatically (`flipkart_electronics.csv`).

## Prerequisites
Before running the scraper, assure you have the following installed:
- Python 3.8+
- PostgreSQL (Local server installed and running)

**Python Packages:**
You can install the required packages using pip:
```bash
pip install playwright beautifulsoup4 pandas psycopg2-binary
playwright install
```

## Setup & Configuration

### PostgreSQL Database Initialization
1. Ensure your local PostgreSQL server is running.
2. Create a database named `flipkart_2026` via pgAdmin or your terminal:
   ```sql
   CREATE DATABASE flipkart_2026;
   ```
3. The table (`electronics`) will automatically be created by the script on the first run. 
4. The default connection configures `user='postgres'`, `host='localhost'`, `port='5432'`.
5. Upon running the script, the system will prompt you for your `postgres` password in the terminal.

## Usage

Run the main scraper entry point:
```bash
python main.py
```

### What happens when you run it?
1. The script will open a Playwright Chromium browser instance.
2. It closes any login popups on the Flipkart homepage.
3. It iterates through the defined search categories.
4. It extracts relevant details for each product on the page.
5. Once all categories/pages are scraped, it prompts for the database password.
6. Saves the dataset to the PostgreSQL DB and locally to `flipkart_electronics.csv`.

## Project Structure
- `main.py` - Application entry point. Handles browser initialization, category loops, page iteration, and invoking data scraping/saving handlers.
- `get_electronics_cat.py` - Contains the `get_device_data` function that parses Playwright page DOM elements into clean Python dictionaries.
- `save_to_db.py` - Contains database logic (`save_to_postgres`) and file export logic (`save_to_csv`).
- `walkthrough_*.md` - Auxiliary documentation detailing the flow of each major module.
