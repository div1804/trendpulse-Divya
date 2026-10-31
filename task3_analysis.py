# Import required libraries

import pandas as pd
import numpy as np

print("Libraries imported successfully!")
# Step 1: Load the cleaned CSV file from Task 2

csv_file = "data/trends_clean.csv"

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(csv_file)

# Print the first five rows
print("\nFirst 5 rows:")
print(df.head())

# Print the shape (number of rows and columns)
print("\nLoaded data:", df.shape)
# Step 2: Calculate average score and average comments

average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

# Print the average values
print("\nAverage score   :", average_score)
print("Average comments:", average_comments)
# Step 3: Calculate statistics using NumPy

scores = df["score"].to_numpy()

# Calculate mean, median and standard deviation
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

# Calculate highest and lowest scores
max_score = np.max(scores)
min_score = np.min(scores)

# Print NumPy statistics
print("\n--- NumPy Stats ---")
print("Mean score   :", mean_score)
print("Median score :", median_score)
print("Std deviation:", std_score)
print("Max score    :", max_score)
print("Min score    :", min_score)
# Step 4: Find the category with the most stories

category_counts = df["category"].value_counts()

# Get the category with the highest number of stories
most_category = category_counts.idxmax()
most_category_count = category_counts.max()

# Print the result
print("\nMost stories in:", most_category,
      "(", most_category_count, "stories )")
# Step 5: Find the story with the most comments

# Find the index of the maximum comment count
most_commented_index = df["num_comments"].idxmax()

# Get the most-commented story
most_commented_story = df.loc[most_commented_index]

# Print its title and comment count
print("\nMost commented story:")
print("Title:", most_commented_story["title"])
print("Comments:", most_commented_story["num_comments"])
# Step 6: Calculate engagement for each story

# Engagement = number of comments divided by (score + 1)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Display the first five engagement values
print("\nEngagement values:")
print(df[["title", "score", "num_comments", "engagement"]].head())
# Step 7: Identify popular stories

# A story is popular if its score is greater than the average score
df["is_popular"] = df["score"] > average_score

# Display the first five popularity results
print("\nPopularity results:")
print(df[["title", "score", "is_popular"]].head())
# Step 8: Save the analysed data as a new CSV file

# Set the output file path
output_file = "data/trends_analysed.csv"

# Save the updated DataFrame with new columns
df.to_csv(output_file, index=False)

# Print confirmation message
print("\nSaved", len(df), "rows to", output_file)