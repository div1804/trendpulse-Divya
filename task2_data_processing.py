# Import required libraries

import pandas as pd
import json
import os

print("Libraries imported successfully!")
# Step 1: Load JSON data from Task 1

json_file = "data/trends_20261030.json"

# Load JSON file into a Pandas DataFrame
df = pd.read_json(json_file)

# Print the number of rows loaded
print("Loaded", len(df), "stories from", json_file)

# Display the first five rows
print("\nFirst five stories:")
print(df.head())
# Step 2: Remove duplicate stories using post_id

df = df.drop_duplicates(subset="post_id")

# Print the number of rows after removing duplicates
print("\nAfter removing duplicates:", len(df))
# Step 3: Remove rows with missing important values

df = df.dropna(subset=["post_id", "title", "score"])

# Print the number of rows after removing missing values
print("\nAfter removing nulls:", len(df))
# Step 4: Convert score and num_comments into integers

df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Display the data types after conversion
print("\nData types after conversion:")
print(df[["score", "num_comments"]].dtypes)
# Step 5: Remove stories with a score below 5

df = df[df["score"] >= 5]

# Print number of rows after removing low-score stories
print("\nAfter removing low scores:", len(df))
# Step 6: Remove extra spaces from story titles

df["title"] = df["title"].str.strip()

# Print the number of rows remaining after cleaning
print("\nRows remaining after cleaning:", len(df))
# Step 7: Save cleaned data as CSV

# Create the data folder if it does not exist
os.makedirs("data", exist_ok=True)

# Set the CSV file path
csv_file = "data/trends_clean.csv"

# Save the cleaned DataFrame
df.to_csv(csv_file, index=False)

# Print confirmation message
print("\nSaved", len(df), "rows to", csv_file)

# Display stories per category
print("\nStories per category:")
print(df["category"].value_counts())