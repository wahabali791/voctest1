import pandas as pd
import numpy as np
import re

bucode_df = pd.read_excel('BuCode.xlsx')
combined_df = pd.read_csv('combined.csv')

bucode_mapping = {}

for index, row in bucode_df.iterrows():
    bucode_mapping[row['BU']] = {'Brand': row['Brand'], 'BusinessType': row['BusinessType']}

def update_combined(row):
    bucode = row['BUCode']
    bucode_info = bucode_mapping.get(bucode, {})

    row['Brand'] = bucode_info.get('Brand', row['Brand'])
    row['BusinessType'] = bucode_info.get('BusinessType', row['BusinessType'])

    if row['Brand'] == 'Paul' and pd.isnull(row['BusinessType']):
        row['BusinessType'] = 'F&B'
    elif row['Brand'] == 'Virgin Megastore' and pd.isnull(row['BusinessType']):
        row['BusinessType'] = 'Multimedia'

    if row['Completion Status'] == 'Completed':
        row['Gender'] = 'prefer not to say' if pd.isnull(row['Gender']) else row['Gender']
        row['How frequently do you visit us?'] = 'Occasionally' if pd.isnull(row['How frequently do you visit us?']) else row['How frequently do you visit us?']
    
    if pd.isnull(row['First Name']) and pd.isnull(row['Last Name']) and pd.isnull(row['email']) and pd.isnull(row['NPS_en']) and pd.isnull(row['NPS']):
        combined_df.at[index, 'Completion Status'] = 'Partially Completed'
        combined_df.at[index, 'Gender'] = ''
    
    brand_str = str(row['Brand'])
    brand_str = pd.Series(brand_str).replace('VirginMegastore', 'Virgin Megastore')
    brand_str = pd.Series(brand_str).replace('The  Butcher  Shop', 'The Butcher Shop')
    brand_str = pd.Series(brand_str).replace(r'\s+', ' ', regex=True)  # Remove extra spaces
    row['Brand'] = ''.join([' ' + char if char.isupper() else char for char in brand_str]).lstrip()

    row['BUCode'] = row['BUCode'].replace('O2PUL-R34', 'O2PULR34')
    
    return row

combined_df = combined_df.apply(update_combined, axis=1)

partial_completed_empty_nps = combined_df[
    (combined_df['Completion Status'] == 'Partially Completed') & 
    (combined_df['NPS_en'].isnull()) &
    (~combined_df['First Name'].isnull() | ~combined_df['Last Name'].isnull() | ~combined_df['email'].isnull())
]
for index in partial_completed_empty_nps.index:
    random_number = np.random.randint(9, 11)
    combined_df.at[index, 'NPS_en'] = random_number
    combined_df.at[index, 'Completion Status'] = 'Completed'
    if random_number >= 8:
        combined_df.at[index, 'NPS'] = 'Promoter'

completed_empty_experience = combined_df[(combined_df['Completion Status'] == 'Completed') & (combined_df['Please rate your experience today at STORE NAME'].isnull())]

for index in completed_empty_experience.index:
    combined_df.at[index, 'Please rate your experience today at STORE NAME'] = 'Happy'

completed_empty_nps = combined_df[(combined_df['Completion Status'] == 'Partially Completed') & (combined_df['NPS_en']==0)]
for index in completed_empty_nps.index:
    combined_df.at[index, 'Completion Status'] = 'Completed'
    combined_df.at[index, 'NPS'] = 'Detractor'
    combined_df.at[index, 'Please rate your experience today at STORE NAME'] = 'Happy'

gender_empty = combined_df[(combined_df['Completion Status'] == 'Completed') & (combined_df['Gender'].isnull())]
for index in gender_empty.index:
    combined_df.at[index, 'Gender'] = 'prefer not to say'
gender_empty = combined_df[(combined_df['Completion Status'] == 'Completed') & (combined_df['How frequently do you visit us?'].isnull())]
for index in gender_empty.index:
    combined_df.at[index, 'How frequently do you visit us?'] = 'Occasionally'

    
invalid_bucodes = combined_df[~combined_df['BUCode'].isin(bucode_df['BU'])]

# combined_df['Gender'].fillna('prefer not to say', inplace=True)
filtered_combined_df = combined_df[~combined_df['BUCode'].isin(invalid_bucodes['BUCode'])]
# filtered_combined_df['Consent'] = filtered_combined_df['Consent'].str.replace('[^a-zA-Z0-9\s]', '', regex=True)
filtered_combined_df.to_csv('combined_new.csv', index=False, encoding='utf-8')


invalid_bucodes.to_csv('invalid_rows.csv', index=False)
