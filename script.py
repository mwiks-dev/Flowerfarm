import pandas as pd
import mysql.connector

# Load data from the Excel file into a pandas DataFrame
excel_file = "Nov 2023 Production.xlsx"  
df = pd.read_excel(excel_file, header=[2, 3], index_col=[0, 1, 2])

# Create a connection to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Password123",
    database="Flowerfarm"
)

# Create a cursor object to execute SQL commands
cursor = db_connection.cursor()

# Iterate through the DataFrame and insert data into the MySQL database
for index, row in df.iterrows():
    mm_yy = index[0]
    code = index[1]
    greenhouse_number = index[2]
    for col in df.columns:
        if not pd.isna(row[col]):
            production_date = col[0]
            length = col[1]
            total_number = row[col]

            # Handle NaN values by replacing them with 0
            total_number = row[col] if not pd.isna(row[col]) else 0
            

            # Insert data into the database
            insert_query = """
            INSERT INTO greenhouse_production (production_date, greenhouse_number, length, varieties, total_number)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (production_date, greenhouse_number, length, code, total_number))

# Commit changes and close the database connection
db_connection.commit()
db_connection.close()

print("Data has been successfully copied to the database.")
