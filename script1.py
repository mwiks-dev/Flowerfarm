import pandas as pd

# Load data from the original Excel file
excel_file = "Nov 2023 Production.xlsx"  
df = pd.read_excel(excel_file)

# Find the row index containing "MM/YY"
date_row_index = df.index[df.eq("MM/YY").any(axis=1)][0]

# Extract the "MM/YY" row
date_row = df.loc[date_row_index]

# Remove the row containing "MM/YY" from the DataFrame
df = df.drop(date_row_index)

# Rename columns to match the database schema
df = df.rename(columns={
    "Green Hse": "greenhouse_number",
    "Length": "length",
    "Variety": "varieties",  # If your Excel data includes variety
    "Total Number": "total_number"
})

# Concatenate the "MM/YY" values with the corresponding columns to create "production_date"
date_row = date_row.dropna().astype(str)  # Remove NaN values and convert to string
df["production_date"] = date_row.str.cat(df.iloc[:, 3:], sep=' ')

# Ensure data types match the schema
df["production_date"] = pd.to_datetime(df["production_date"], format="%b-%y %d")
df["greenhouse_number"] = df["greenhouse_number"].astype(str)
df["length"] = df["length"].astype(str)
df["varieties"] = df["varieties"].astype(str)  # If your Excel data includes variety
df["total_number"] = df["total_number"].fillna(0).astype(int)  # Replace NaN with 0 and convert to int

# Save the edited data to a new Excel file
edited_excel_file = "edited_excel_data.xlsx"  
df.to_excel(edited_excel_file, index=False)

print("Excel data has been edited and saved to", edited_excel_file)