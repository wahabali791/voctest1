import pandas as pd
import re
import numpy as np

# Read the CSV file, skipping the initial lines until the header row
input_csv_path = 'analytics-download.csv'
output_csv_path = 'survey stores3.csv'

# Skip lines until the header row
skip_rows = 6
df = pd.read_csv(input_csv_path,  delimiter=',', header=None)
# Extract header from the second row
header_row = df.iloc[0]
df = df[1:]
df.columns = header_row


# Function to extract Brand and BUcode using regex
def extract_brand_bucode(link):

    if isinstance(link, str):
        # brand_pattern = r'brand|Band|Brand'
        # bucode_pattern = r'BUCode|bucode|BUcode'
        brand_match = re.search(fr'Brand=([^&]+)| brand=([^&]+) | Band=([^&]+)', link, flags=re.IGNORECASE)
        bucode_match = re.search(fr'BUCode=([^&]+)', link, flags=re.IGNORECASE)

        brand = brand_match.group(1) if brand_match else None
        bucode = bucode_match.group(1).replace('%20', '') if bucode_match else None
        
        modified_brand = None
        if bucode == '10PULL46':
            brand = 'Paul'
        if brand:
            # Remove '%' and digits from the modified brand name
            modified_brand = re.sub(r'[%\d+]', ' ', brand)
            modified_brand = re.sub(r'\s+', ' ',  modified_brand)

            if "VirginMegastore" in modified_brand:
                modified_brand = "Virgin Megastore"
            # Convert "PullBear" to "Pull&Bear"
            if "Pull Bear" in modified_brand:
                modified_brand = "Pull & Bear"
                
            # If "Pull" is present in modified brand, add "& Bear" to it
            elif "Pull " in modified_brand:
                modified_brand += "& Bear"

            # If the modified brand is "BusinessType=FB", set it to None
            if modified_brand == "BusinessType=F B":
                modified_brand = None
            if modified_brand == "W ite":
                modified_brand = "Wite"

        return modified_brand, bucode
    else:
        return None, None

# Apply the function to the "Landing page" column
df['Brand'], df['BUcode'] = zip(*df['Landing page + query string'].apply(extract_brand_bucode))

# Write the result to a new CSV file
df.to_csv(output_csv_path, index=False)

print(f"Results saved to {output_csv_path}")
