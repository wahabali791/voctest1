import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv("combined_new.csv")

# Concatenate the data from the second and third columns into the first column
df["What can be improved about our Staff &amp; Service?"] = df["What can be improved about our staff &amp; service?_2"].fillna('') + " " + df["What can be improved about our staff & service?_arabic"].fillna('')

# Rename the second column to match the first one
df.rename(columns={"What can be improved about our staff &amp; service?_2": "What can be improved about our Staff &amp; Service?"}, inplace=True)

# Save the modified DataFrame back to a CSV file
df.to_csv("modified_file.csv", index=False)
