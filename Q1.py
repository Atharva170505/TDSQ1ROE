import sqlite3
import pandas as pd
import json

# Step 1: Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("retail.db")
cursor = conn.cursor()

# Step 2: Create the table
cursor.execute("""
CREATE TABLE IF NOT EXISTS retail_data (
  Store_ID TEXT,
  Footfall INTEGER,
  Promo_Spend INTEGER,
  Avg_Basket INTEGER,
  Returns INTEGER,
  Net_Sales INTEGER
)
""")

# Step 3: Insert some sample data (only if table is empty)
cursor.execute("SELECT COUNT(*) FROM retail_data")
if cursor.fetchone()[0] == 0:
    sample_data = [
        ('S001', 1000, 5000, 200, 20, 180000),
        ('S002', 800, 3000, 180, 10, 140000),
        ('S003', 1100, 6000, 210, 30, 195000),
        ('S004', 900, 4000, 190, 15, 160000),
        ('S005', 1200, 7000, 220, 35, 210000),
    ]
    cursor.executemany("INSERT INTO retail_data VALUES (?, ?, ?, ?, ?, ?)", sample_data)
    conn.commit()

# Step 4: Load the data into pandas
df = pd.read_sql_query("SELECT * FROM retail_data", conn)

# Step 5: Calculate correlations
cor1 = df['Promo_Spend'].corr(df['Returns'])
cor2 = df['Promo_Spend'].corr(df['Avg_Basket'])
cor3 = df['Returns'].corr(df['Avg_Basket'])

# Step 6: Find strongest correlation
correlations = {
    "Promo_Spend-Returns": cor1,
    "Promo_Spend-Avg_Basket": cor2,
    "Returns-Avg_Basket": cor3
}
strongest = max(correlations.items(), key=lambda x: abs(x[1]))

# Step 7: Save result as JSON
result = {
    "pair": strongest[0],
    "correlation": round(strongest[1], 4)
}
with open("correlation_result.json", "w") as f:
    json.dump(result, f)

print("✅ JSON file generated:", result)
