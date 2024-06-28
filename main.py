#import gdown
import numpy as np
import pandas as pd
import time
from datetime import datetime
# from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

#url = 'https://docs.google.com/spreadsheets/d/1HVAJDrU3MczXTmdkHu124Bg3C8ovcoA8JfRXtVtlWR0/edit?usp=drive_link'
#file_id = url.split('/')[-2]
#prefix = 'https://drive.google.com/uc?/export=download&id='

# Download the file
#gdown.download(prefix + file_id, 'downloaded_file.xlsx')  # Download as Excel file

# Convert the Excel file to CSV
#excel_file_path = 'downloaded_file.xlsx'
# Get the current date in the format YYYY-MM-DD
file_date = datetime.now().strftime('%Y-%m-%d')

# Construct the file path using the current date
csv_file_path = f"/home/ubuntu/Downloads/Dev_Version_Submissions_{file_date}.csv"

df = pd.read_csv(csv_file_path)  # Read Excel file using pandas
#df.to_csv(csv_file_path, index=False)  # Convert and save as CSV

print(f"Partial Survey file : {csv_file_path}")

# Specify the columns containing the Arabic strings and the replacement mapping
columns_to_replace = ['Gender','Please rate your experience today at STORE NAME','What can be improved for a better experience?','What can be improved about our Value for Money?','What can be improved about our Atmosphere?','What can be improved about our Staff &amp; Service?','What can be improved about our F&amp;B Quality?','Did the manager visit your table?','What can be improved with our products?','What can be improved about the store experience?','What can be improved about our staff &amp; service?','What can be improved about our staff & service?_arabic','What can be improved about our fitting rooms?','How frequently do you visit us?','Do you have additional Feedback for us?']
replacement_mapping = {
    'ذكر': 'Male',
    'أنثى': 'Female', 
    'أفضل ان لا اقول': 'Prefer not to say', 
    'محزن': 'Sad',
    'عادي': 'Normal',
    'سعيد': 'Happy',
    'اسبوعيا': 'Weekly',
    'من حين إلى آخر': 'Occasionally',
    'شهريا': 'Monthly',
    'الموسيقى': 'Music',
    'المنتجات':'Product',
    'التجربة داخل المحل':'Store Experience',
    'الموظفين و الخدمة':'Staff & Services',
    'غرفة القياس':'Fitting Room',
    'طريقة عرض المنتجات': 'Product Display',
    'التكييف': 'Air Conditioning',
    'الإضاءة': 'Lighting',
    'النظافة و الترتيب': 'Cleanliness & tidiness of the store',
    'نظافة القطع': 'Item Cleanliness',
    'الجودة': 'Quality',
    'المقاسات و الألوان': 'Size & color availability',
    'القيمة لنسبة المبلغ': 'Value for money',
    'التنوع و الخيارات': 'Variety & Selection',
    'توافر الموظفين في غرفة القياس': 'Availability of staff at fitting room',
    'النظافة والترتيب': 'Cleanliness & tidiness',
    'قائمة الانتظار ووقت الانتظار': 'Queue & waiting time',
    'الخدمة المقدمة في غرفة القياس': 'Service provided at fitting room',
    'معلومات الموظفين': 'Staff Knowledge',
    'مساعدة الموظفين': 'Staff Helpfulness',
    'إيجابية الموظفين': 'Staff Positivity & attitude',
    'تواجد الموظفين في المتجر': 'Staff Availability in the store',
    'التجربة عند صندوق الدفع': 'Experience at the cash counter',
    'أالأجواء': 'Atmosphere',
    'جودة الأطعمة والمشروبات': 'F&B Quality',
    'السعر مقارنة بالتوقعات' : 'Price vs Expectation',
    'السعر مقارنة بالجودة' : 'Price vs Quality',
    'السعر مقارنة بالكمية' : 'Price vs Portion Size',
    'مستوى الضجيج':'Noise Level',
    'الديكور':'Decor',
    'راحة الجلوس' : 'Seating Comfort',
    'إختيار الموسيقى' : 'Music Selection',
    'مظهر الموظفين' : 'Staff Appearance',
    'الانتباه' : 'Attentiveness',
    'سرعة الخدمة' : 'Speed of Service',
    'الود' : 'Friendliness',
    'دقة الطلب' : 'Accuracy of Order',
    'معرفة قائمة الطعام' : 'Menu Knowledge',
    'الحرارة' : 'Temperature',
    'النكهة':'Taste',
    'التقديم':'Presentation',
    'نظافة القطع' : 'Item Cleanliness',
    'الجودة' : 'Quality',
    'المقاسات و الألوان' : 'Size & color availability',
    'القيمة لنسبة المبلغ' : 'Value for money',
    'التنوع و الخيارات' : 'Variety & Selection',
}

# Function to replace Arabic strings with English strings
def replace_arabic_with_english(text):
    if isinstance(text, str):
        for arabic_str, english_str in replacement_mapping.items():
            text = text.replace(arabic_str, english_str)
    return text

def calculate_nps_final(row):
    if row['Completion Status'] == 'Completed':
        if row['NPS_en'] >= 9:
            return 'Promoter'
        elif row['NPS_en'] in [7, 8]:
            return 'Passive'
        else:
            return 'Detractor'
    else:
        return ''

def apply_custom_logic(row):
    if row['BusinessType'] == 'F&B' and row['survey_language'] == 'Start Survey In English':
        return row['What can be improved for a better experience?F&B']
    elif row['BusinessType'] == 'F&B' and row['survey_language'] == 'ابدأ التصفح':
        return row['What can be improved for a better experience?F&B_arabic']
    elif row['BusinessType'] == 'Multimedia' and row['survey_language'] == 'Start Survey in English':
        return row['What can be improved for a better experience?MM']
    elif row['BusinessType'] == 'Multimedia' and row['survey_language'] == 'ابدأ التصفح':
        return row['What can be improved for a better experience?MM_arabic']
    elif row['BusinessType'] == 'Fashion' and row['survey_language'] == 'ابدأ التصفح':
        return row['What can be improved for a better experience?_arabic']
    else:
        return row['What can be improved for a better experience?']
def apply_manager_logic(row):
    if row['BusinessType'] == 'F&B' and row['survey_language'] == 'ابدأ التصفح':
        return row['Did the manager visit your table?_f&B_arabic']
    else:
        return row['Did the manager visit your table?']

def apply_productimprovemnt_logic(row):
    if row['BusinessType'] == 'Fashion' and row['survey_language'] == 'ابدأ التصفح':
        return row['What can be improved with our products?_arabic']
    else:
        return row['What can be improved with our products?'] 
def apply_NPSrating_logic(row):
    if row['survey_language'] == 'ابدأ التصفح':
        return row['NPS_ar']
    else:
        return row['NPS_en'] 

def apply_completion_logic(row):
    if row['NPS_en'] > 0:
        return "Completed"
    else:
        return "Partially Completed"

def apply_storeExperience_logic(row):
    if row['survey_language'] == 'ابدأ التصفح':
        return row['What can be improved about the store experience?_arabic']
    else:
        return row['What can be improved about the store experience?']

def apply_fittingRoom_logic(row):
    if row['survey_language'] == 'ابدأ التصفح':
        return row['What can be improved about our fitting rooms?_arabic']
    else:
        return row['What can be improved about our fitting rooms?']
    
def apply_rateExperience_logic(row):
    if row['survey_language'] == 'ابدأ التصفح':
        return row['Please rate your experience today at STORE NAME_arabic']
    else:
        return row['Please rate your experience today at STORE NAME']


def apply_dialCode_logic(row):
    if row['survey_language'] == 'ابدأ التصفح':
        return row['DialCode_arabic']
    elif pd.notna(row['DialCode (1)']):
        return row['DialCode (1)']
    else:
        return row['DialCode (2)']

    
def apply_phone_logic(row):
    if row['survey_language'] == 'ابدأ التصفح':
        return row['Phone_arabic']
    else:
        return row['phone']
    
def apply_consent_logic(row):
    if row['survey_language'] == 'ابدأ التصفح':
        return row['Consent_arabic']
    else:
        return row['Consent']

def apply_firstName_logic(row):
    if row['survey_language'] == 'ابدأ التصفح':
        return row['First Name_arabic']
    else:
        return row['First Name']
    
def apply_lastName_logic(row):
    if row['survey_language'] == 'ابدأ التصفح':
        return row['Last Name_arabic']
    else:
        return row['Last Name']
    

def apply_gender_logic(row):
    if row['survey_language'] == 'ابدأ التصفح':
        return row['Gender_arabic']
    else:
        return row['Gender']

def apply_email_logic(row):
    if row['survey_language'] == 'ابدأ التصفح':
        return row['email_arabic']
    else:
        return row['email']



def apply_feedBack_logic(row):
    if row['survey_language'] == 'ابدأ التصفح':
        return row['Please share your feedback here...._arabic']
    else:
        return row['Please share your feedback here....']

  

def apply_additionalFeeback_logic(row):
    if row['survey_language'] == 'ابدأ التصفح':
        return row['Do you have additional Feedback for us?_arabic']
    else:
        return row['Do you have additional Feedback for us?']
    
def apply_frequentlyVisit_logic(row):
    if row['survey_language'] == 'ابدأ التصفح':
        return row['How frequently do you visit us?_arabic']
    else:
        return row['How frequently do you visit us?']

def replace_arabic_phrases(consent_ar):
    # Check if the value is a non-null string before applying the replacement
    if isinstance(consent_ar, str):
        # Replace each Arabic phrase separately
        consent_ar = consent_ar.replace('لا أوافق', 'I don\'t accept.')
        consent_ar = consent_ar.replace('أوافق', 'I Accept')
        
        return consent_ar
    else:
        return consent_ar

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path, encoding='utf-8')

df['NPS_en'] = df.apply(apply_NPSrating_logic, axis=1)

df['Completion Status'] = df.apply(apply_completion_logic, axis=1)

# Apply the custom logic to the "What can be improved for a better experience?" column
df['What can be improved for a better experience?'] = df.apply(apply_custom_logic, axis=1)

# Apply the custom logic to the "Did the manager visit your table?" column
df['Did the manager visit your table?'] = df.apply(apply_manager_logic, axis=1)

# Apply the custom logic to the "What can be improved with our products?" column
df['What can be improved with our products?'] = df.apply(apply_productimprovemnt_logic, axis=1)

# Apply the custom logic to the "What can be improved with our products?" column
df['What can be improved about the store experience?'] = df.apply(apply_storeExperience_logic, axis=1)


# Apply the custom logic to the "What can be improved about our fitting rooms?" column
df['What can be improved about our fitting rooms?'] = df.apply(apply_fittingRoom_logic, axis=1)


# Please rate your experience today at STORE NAME?" column
df['Please rate your experience today at STORE NAME'] = df.apply(apply_rateExperience_logic, axis=1)

df['Consent_arabic'] = df['Consent_arabic'].apply(replace_arabic_phrases)
# Consent" column
df['Consent'] = df.apply(apply_consent_logic, axis=1)


# Dial Code column
df['DialCode (2)'] = df.apply(apply_dialCode_logic, axis=1)

# phone  column
df['phone'] = df.apply(apply_phone_logic, axis=1)

# First Name column
df['First Name'] = df.apply(apply_firstName_logic, axis=1)

# First Name column
df['Last Name'] = df.apply(apply_lastName_logic, axis=1)


# First Name column
df['Gender'] = df.apply(apply_gender_logic, axis=1)

# Email column
df['email'] = df.apply(apply_email_logic, axis=1)


# Feedback column
df['Please share your feedback here....'] = df.apply(apply_feedBack_logic, axis=1)


# visit column
df['How frequently do you visit us?'] = df.apply(apply_frequentlyVisit_logic, axis=1)


# additional feedback column
df['Do you have additional Feedback for us?_arabic'] = df.apply(apply_additionalFeeback_logic, axis=1)


# Create a new column "NPS_final" using the specified conditions
df['NPS'] = df.apply(calculate_nps_final, axis=1)


# Drop the specified columns
columns_to_drop = [
    'What can be improved for a better experience?F&B',
    'What can be improved for a better experience?F&B_arabic',
    'What can be improved for a better experience?MM',
    'What can be improved for a better experience?MM_arabic',
    'Did the manager visit your table?_f&B_arabic',
    'What can be improved about the store experience? (Music)',
    'What can be improved about the store experience? (Product Display)',
    'What can be improved about the store experience? (Air Conditioning)',
    'What can be improved about the store experience? (Lighting )',
    'What can be improved about the store experience? (Cleanliness & tidiness of the store)',
    'What can be improved about the store experience?_arabic (الموسيقى)',
    'What can be improved about the store experience?_arabic (طريقة عرض المنتجات)',
    'What can be improved about the store experience?_arabic (التكييف)',
    'What can be improved about the store experience?_arabic (الإضاءة)',
    'What can be improved about the store experience?_arabic (النظافة و الترتيب)',
    'Location','Store','Country','BackgroundImage','QRCode',
    'What can be improved with our products? (Item Cleanliness)',
    'What can be improved with our products? (Quality)',
    'What can be improved with our products? (Size & color availability)',
    'What can be improved with our products? (Value for money)',
    'What can be improved with our products? (Variety & Selection)',
    'What can be improved with our products?_arabic',
    'What can be improved with our products?_arabic (نظافة القطع)',
    'What can be improved with our products?_arabic (الجودة)',
    'What can be improved with our products?_arabic (المقاسات و الألوان)',
    'What can be improved with our products?_arabic (القيمة لنسبة المبلغ)',
    'What can be improved with our products?_arabic (التنوع و الخيارات)',
    'What can be improved about the store experience?_arabic',
    'What can be improved about our fitting rooms?_arabic',
    'What can be improved about our fitting rooms? (Availability of staff at fitting room)',
    'What can be improved about our fitting rooms? (Cleanliness & tidiness)',
    'What can be improved about our fitting rooms? (Queue & waiting time)',
    'What can be improved about our fitting rooms? (Service provided at fitting room)',
    'What can be improved about our fitting rooms?_arabic (توافر الموظفين في غرفة القياس)',
    'What can be improved about our fitting rooms?_arabic (النظافة والترتيب)',
    'What can be improved about our fitting rooms?_arabic (قائمة الانتظار ووقت الانتظار)',
    'What can be improved about our fitting rooms?_arabic (الخدمة المقدمة في غرفة القياس)',
    'Please rate your experience today at STORE NAME_arabic',
    'What can be improved for a better experience?_arabic',
    'What can be improved about our staff &amp; service? (Staff Knowledge)',
    'What can be improved about our staff &amp; service? (Staff Helpfulness)',
    'What can be improved about our staff &amp; service? (Staff Positivity & attitude)',
    'What can be improved about our staff &amp; service? (Staff Availability in the store)',
    'What can be improved about our staff &amp; service? (Experience at the cash counter)',
    'What can be improved about our staff & service?_arabic (معلومات الموظفين)',
    'What can be improved about our staff & service?_arabic (مساعدة الموظفين)',
    'What can be improved about our staff & service?_arabic (إيجابية الموظفين)',
    'What can be improved about our staff & service?_arabic (تواجد الموظفين في المتجر)',
    'What can be improved about our staff & service?_arabic (التجربة عند صندوق الدفع)',
    'Phone_arabic','DialCode_arabic', 'Consent_arabic','DialCode (1)' , 'Last Name_arabic','First Name_arabic','email_arabic','Gender_arabic',
    'Please share your feedback here...._arabic' , 'How frequently do you visit us?_arabic',
    'Do you have additional Feedback for us?_arabic','NPS_ar'

]

df.drop(columns=columns_to_drop, inplace=True)
df.rename(columns={'DialCode (2)': 'DialCode (1)'}, inplace=True)

# Apply the replacement function to the specified columns
for column in columns_to_replace:
    df[column] = df[column].apply(replace_arabic_with_english)

if 'NPS_en_new' in df.columns:
    # Merge 'NPS_en' and 'NPS_en_new' columns conditionally
    df['NPS_en'] = df.apply(lambda row: row['NPS_en_new'] if pd.notnull(row['NPS_en_new']) else row['NPS_en'], axis=1)

    # Drop the 'NPS_en_new' column as it's no longer needed
    df.drop(columns=['NPS_en_new'], inplace=True)
    

#df['Completion Status'] = 'Completed'
df = df[df['BUCode'].notna() & (df['BUCode'] != '')]

transformed_csv_file_path = 'combined_partial.csv'
df.to_csv(transformed_csv_file_path, index=False, encoding='utf-8')
print("Replacement completed and file saved.")

# Azure Blob Storage details
#azure_connection_string = 'DefaultEndpointsProtocol=https;AccountName=azadea;AccountKey=a3T4kBCWOZJb3ndoPdMYwfyvyAKlQCkBHkqOB6FEeSAf2w2slI0eDwQUtsIdHRQYS4ig5w4OH6miW+FWSRvA2w==;EndpointSuffix=core.windows.net'
#container_name = 'collated-new'
#blob_name = 'combined.csv'

# Upload the transformed CSV file to Azure Blob Storage
#blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)
#container_client = blob_service_client.get_container_client(container_name)
#blob_client = container_client.get_blob_client(blob_name)

#with open(transformed_csv_file_path, 'rb') as data:
#    blob_client.upload_blob(data, overwrite=True)
