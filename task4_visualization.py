# Import required libraries

import pandas as pd
import matplotlib.pyplot as plt
import os

print("Libraries imported successfully!")

# Load the analysed CSV file from Task 3

csv_file = "data/trends_analysed.csv"

df = pd.read_csv(csv_file)

print("\nCSV loaded successfully!")
print("Total stories:", len(df))

# Create outputs folder if it does not exist

os.makedirs("outputs", exist_ok=True)

print("Outputs folder is ready!")
# Chart 1: Top 10 Stories by Score

# Select the 10 stories with the highest scores
top_stories = df.nlargest(10, "score").copy()

# Shorten titles longer than 50 characters
top_stories["short_title"] = top_stories["title"].apply(
    lambda title: title[:47] + "..." if len(title) > 50 else title
)

# Create a horizontal bar chart
plt.figure(figsize=(12, 7))

plt.barh(top_stories["short_title"], top_stories["score"])

# Display the highest score at the top
plt.gca().invert_yaxis()

# Add chart title and axis labels
plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")

# Adjust layout to prevent text from being cut off
plt.tight_layout()

# Save the chart before displaying it
plt.savefig("outputs/chart1_top_stories.png")

# Display the chart
plt.show()

print("Chart 1 saved successfully!")
# Chart 2: Stories per Category

# Count the number of stories in each category
category_counts = df["category"].value_counts()

# Create a bar chart with different colours
plt.figure(figsize=(10, 6))

plt.bar(
    category_counts.index,
    category_counts.values,
    color=["skyblue", "orange", "green", "purple", "red"]
)

# Add chart title and axis labels
plt.title("Number of Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

# Adjust layout
plt.tight_layout()

# Save the chart before displaying it
plt.savefig("outputs/chart2_categories.png")

# Display the chart
plt.show()

print("Chart 2 saved successfully!")
# Chart 3: Score vs Comments

# Create a scatter plot
plt.figure(figsize=(10, 6))

# Plot non-popular stories
plt.scatter(
    df[df["is_popular"] == False]["score"],
    df[df["is_popular"] == False]["num_comments"],
    color="red",
    label="Not Popular"
)

# Plot popular stories
plt.scatter(
    df[df["is_popular"] == True]["score"],
    df[df["is_popular"] == True]["num_comments"],
    color="blue",
    label="Popular"
)

# Add chart title and axis labels
plt.title("Story Score vs Number of Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")

# Display the legend
plt.legend()

# Adjust layout
plt.tight_layout()

# Save the chart before displaying it
plt.savefig("outputs/chart3_scatter.png")

# Display the chart
plt.show()

print("Chart 3 saved successfully!")
# Bonus: Create TrendPulse Dashboard

# Create one figure with three subplots
fig, axes = plt.subplots(1, 3, figsize=(20, 7))

# Chart 1: Top 10 Stories by Score
axes[0].barh(
    top_stories["short_title"],
    top_stories["score"]
)

axes[0].invert_yaxis()
axes[0].set_title("Top 10 Stories")
axes[0].set_xlabel("Score")
axes[0].set_ylabel("Story Title")

# Chart 2: Stories per Category
axes[1].bar(
    category_counts.index,
    category_counts.values,
    color=["skyblue", "orange", "green", "purple", "red"]
)

axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Number of Stories")
axes[1].tick_params(axis="x", rotation=45)

# Chart 3: Score vs Comments
axes[2].scatter(
    df[df["is_popular"] == False]["score"],
    df[df["is_popular"] == False]["num_comments"],
    color="red",
    label="Not Popular"
)

axes[2].scatter(
    df[df["is_popular"] == True]["score"],
    df[df["is_popular"] == True]["num_comments"],
    color="blue",
    label="Popular"
)

axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Number of Comments")
axes[2].legend()

# Add an overall dashboard title
fig.suptitle("TrendPulse Dashboard", fontsize=18)

# Adjust spacing between charts
plt.tight_layout()

# Save the dashboard before displaying it
plt.savefig("outputs/dashboard.png")

# Display the dashboard
plt.show()

print("TrendPulse Dashboard saved successfully!")