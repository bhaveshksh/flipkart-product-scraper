# Walkthrough: save_to_db.py

The `save_to_db.py` handles persistent data structuring using both local CSV files (via Pandas) and robust remote databases (using PostgreSQL via `psycopg2`). 

## Step-by-Step Logic

### 1. Database Connection Definition
```python
        conn = {
            "dbname": "flipkart_2026",
            "user": 'postgres',
            "password": input("Enter your PostgreSQL password: "),
            "host": 'localhost',
            "port": '5432'
        }
```
The script requires direct communication credentials pointing to local Postgres configurations. Crucially, the password is manually prompted over standard input securely at runtime to prevent leaking plaintext credentials into Git repositories.

### 2. Establishing the Connection and Cursor Tracker
```python
            conn = psycopg2.connect(**conn)
            cursor = conn.cursor()
```
The Python script fundamentally establishes communication over Postgres protocol. Using `**conn` elegantly unpacks the hardcoded dictionary credentials straight into authentication parameters. A `cursor` object is launched to interact dynamically via SQL execute blocks. 

### 3. Dynamic Database Schema Instantiation
```python
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS electronics (
                id SERIAL PRIMARY KEY,
                category TEXT,
                name TEXT,
                price TEXT,
...
            );
            ''')
```
Instead of assuming a table is properly configured from beforehand, the driver robustly injects a `CREATE TABLE IF NOT EXISTS` schema instruction guaranteeing flawless runtime data injection using standard text formats. The `SERIAL PRIMARY KEY` is an important SQL standard forcing unique auto-calculating ID increments across mass product dumps perfectly avoiding collision arrays.

### 4. Injecting Dictionary values Iteratively
```python
            insert_query = """
            INSERT INTO electronics (category, name, price, rating, ratings_count, reviews_count, features, original_price, discount) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            for item in data_list:
                cursor.execute(insert_query, (
                    item.get("Category", "N/A"),
...
                    item["Features"].split(" | "),
...
                ))
```
Using PostgreSQL `%s` text parameters implicitly secures the insertion from Malformed String bugs or SQL Insertion attack formatting, safely sanitizing the Python Dictionary items row-by-row sequentially. 
Noticeably `item["Features"].split(" | ")` correctly reconverts the pipe-structured string format back into a PostgreSQL-friendly actual Array `TEXT[]` structure natively matching its SQL Table configurations accurately.

### 5. Committing Validations
```python
            conn.commit()
            cursor.close()
            conn.close()
```
Because SQL acts exclusively over Transaction pools, the massive executed data blocks aren't intrinsically locked onto disk memory until specifically committed. Once written completely, standard python garbage closing ends connection hooks completely freeing OS memory limits safely. 

### 6. Writing to Fallback CSV
```python
    df = pd.DataFrame(data_list)
    df.to_csv(filename, index=False)
```
The dictionary payload translates natively identically into a 2D Pandas `DataFrame` unit allowing instantaneous hard-save to a local root `flipkart_electronics.csv` backup without external dependencies! The `index=False` parameter prevents double-padding the row identifiers into file columns cleanly.
