import pandas as pd

# Read the CSV file
df = pd.read_csv('combined_new.csv')

# Function to concatenate dial code with phone number in the 'phone' column
def move_digits_with_plus(row):
    phone_number = str(row['phone']).strip() if not pd.isna(row['phone']) else ''  # Convert to string and handle NaN
    dial_code = str(row['DialCode (1)']).strip()  # Convert to string to handle NaN and remove leading/trailing spaces
    if phone_number != '' and dial_code != '' and '+' in dial_code:
        phone_digits = ''.join(filter(lambda x: x.isdigit() or x == '+', dial_code))  # Extract '+' and digits
        if phone_digits:  # Check if there are digits or '+' sign
            return phone_digits + ' ' + phone_number
        else:
            return phone_number
    else:
        return ''

# Apply the function to update 'phone' column
df['phone'] = df.apply(move_digits_with_plus, axis=1)

# Define a function to remove '.0' suffix and handle NaN values
def clean_phone(phone):
    if pd.isna(phone):
        return ''  # Return empty string for NaN values
    else:
        return str(phone).replace('.0', '')  # Remove '.0' suffix

# Apply the function to clean the 'phone' column
df['phone'] = df['phone'].apply(clean_phone)

# Save the updated DataFrame to a new CSV file without NaN values
df.to_csv('combined_new.csv', index=False)

print("CSV file saved successfully!")
