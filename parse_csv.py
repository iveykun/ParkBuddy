import csv
import re
import sqlite3

db_filename = "data.db"

# Establish a connection to the database
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# Create a table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS data (
    description_rpa TEXT,
    description_rep TEXT,
    x REAL,
    y REAL,
    longitude REAL,
    latitude REAL
);
"""
cursor.execute(create_table_query)
conn.commit()

csv_filename = "your_file.csv"

# Open the CSV file for reading
with open(csv_filename, "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    for row in csv_reader:
        description_rpa = row["DESCRIPTION_RPA"]
        description_rep = row["DESCRIPTION_REP"]
        x = float(row["X"])  # Convert to appropriate data type
        y = float(row["Y"])  
        longitude = float(row["Longitude"])  
        latitude = float(row["Latitude"]) 
        
        # Extract parking information using regular expressions
        parking_pattern = r"\\([Pp]) ([\d\w\s\-:]+) ([A-ZÉ.\s]+\.\s\d+ [A-ZÉ.]+\. \d+ [A-ZÉ.]+)"
        parking_match = re.search(parking_pattern, description_rpa)
        
        parking_allowed = False
        parking_times = ""
        parking_dates = ""
        
        if parking_match:
            parking_allowed = parking_match.group(1).upper() == "P"
            parking_times = parking_match.group(2)
            parking_dates = parking_match.group(3)
        
        # Insert data into the database
        insert_query = "INSERT INTO data VALUES (?, ?, ?, ?, ?, ?)"
        data_tuple = (description_rpa, description_rep, x, y, longitude, latitude)
        cursor.execute(insert_query, data_tuple)
        conn.commit()

# Close the database connection
conn.close()
