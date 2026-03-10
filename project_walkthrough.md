# Flipkart Web Scraping Project Walkthrough

This project is a web scraper built using Python and Playwright. It extracts electronics product data from Flipkart across multiple categories such as laptops, mobiles, tablets, monitors, and cameras. The extracted data is then stored in both a PostgreSQL database and a CSV file.

## Architecture and Workflow

The project is divided into three main components:

1. **[main.py](./walkthrough_main.md)**: The core script that handles the browser automation using Playwright. It searches for multiple categories, iterates through their pagination, and collects the data.
2. **[get_electronics_cat.py](./walkthrough_get_electronics_cat.md)**: The parsing logic. It receives the HTML page object from Playwright and uses CSS selectors to extract details like title, price, ratings, and features, handling both list and grid layouts.
3. **[save_to_db.py](./walkthrough_save_to_db.md)**: The data storage module. It connects to a robust PostgreSQL database to create tables and insert data securely, and can also output the data as a simple CSV.

## Getting Started

1. **Setup**: Make sure you have `playwright`, `pandas`, and `psycopg2` installed. You will also need to install Playwright browsers via `playwright install`.
2. **Database**: Ensure your local PostgreSQL is running on port `5432` with a database named `flipkart_2026`.
3. **Run**: Execute `python main.py` in your terminal. You will be prompted to enter your PostgreSQL password, after which the headless browser will begin scraping!
