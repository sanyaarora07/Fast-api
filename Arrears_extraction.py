import pandas as pd
import numpy as np

# File paths
file_path = r"Promociones_Catella_Cod.xlsx"
income_file_path = r"Pinto I_Madrid/Incomes/Facturacion_Pinto_I_4900_20240531.xlsx"
arreas_output_file = r"Arreas_data.xlsx"
rentroll_file_path = r"Pinto I_Madrid/Rentroll/Rentroll_PintoI_4900_Basico_20240531.xlsx"

# Load the main data
df = pd.read_excel(file_path)

# Filter and extract relevant columns
filtered_data = df[df["Promotion path"] == "04 Pinto - Francisco Farreras"].copy()
columns_to_extract = ["Promotion ", "Company", "Asset Catella", "Promotion Code"]
extracted_data = filtered_data[columns_to_extract]

# Load arreas data
required_columns = ['Tenant', 'DNI/NIF', 'Asset', 'Sheet', 'Lease contract start', 'Day of report', 'Invoice date', 'Due date days', 'Total Debt Receipt']
arreas_output_data = pd.read_excel(arreas_output_file, usecols=required_columns)
conditions = [
    (arreas_output_data['Sheet'] == 'RETAINER'),
    (arreas_output_data['Sheet'] == 'FINISHED'),
    (arreas_output_data['Sheet'] == 'RENTED')
]

# Define corresponding values for each condition
values = ['NA', 'N', 'Y']

# Use numpy.select to assign values based on conditions
arreas_output_data['Actual Tenant'] = np.select(conditions, values, default='')

# Load income data and extract relevant columns
income_data = pd.read_excel(income_file_path)
income_extracted_data = income_data[['CIF', 'Analitica']].copy()

# Extract only the first occurrence of each 'CIF'
first_occurrence_income_data = income_extracted_data.drop_duplicates(subset=['CIF'], keep='first')

# Merge arreas data with the first occurrence of income extracted data
merged_data = pd.merge(arreas_output_data, first_occurrence_income_data, left_on='DNI/NIF', right_on='CIF', how='left')

# Load rentroll data and extract 'Titular 1 Nif' and 'Titular 1 Cod. Cliente'
rentroll_data = pd.read_excel(rentroll_file_path)
rentroll_extracted_data = rentroll_data[['Titular 1 Nif', 'Titular 1 Cod. Cliente']].copy()
first_occurrence_rentrol_data = rentroll_extracted_data.drop_duplicates(subset=['Titular 1 Nif'], keep='first')
# Merge with arreas data on 'Titular 1 Nif'
merged_data = pd.merge(merged_data, first_occurrence_rentrol_data, left_on='DNI/NIF', right_on='Titular 1 Nif', how='left')
merged_data.rename(columns={
    'Analitica': 'Analitic Code',
 'Titular 1 Cod. Cliente': 'Client Code',
     'Tenant':'Tenant Name',
    'DNI/NIF':'Tenant ID',
    'Lease contract start':'Date Lease Start',
    'Day of report':'Date Report', 
    'Due date days':'Due Date Days',
    'Invoice date':'Invoice Date',
    'Total Debt Receipt':'Invoice Amount',
    }, inplace=True)

main_df = pd.concat([extracted_data, merged_data], axis=1)

# Convert 'Due Date Days' to numeric
main_df['Due Date Days'] = pd.to_numeric(main_df['Due Date Days'], errors='coerce')

# Filter rows where 'Due Date Days' is within the range 0-30
main_df['0-30'] = main_df.apply(lambda row: row['Invoice Amount'] if 0 <= row['Due Date Days'] <= 30 else 0, axis=1)
main_df['31-60'] = main_df.apply(lambda row: row['Invoice Amount'] if 31 <= row['Due Date Days'] <= 60 else 0, axis=1)
main_df['61-90'] = main_df.apply(lambda row: row['Invoice Amount'] if 61 <= row['Due Date Days'] <= 90 else 0, axis=1)
main_df['91-120'] = main_df.apply(lambda row: row['Invoice Amount'] if 91 <= row['Due Date Days'] <= 120 else 0, axis=1)
main_df['121-180'] = main_df.apply(lambda row: row['Invoice Amount'] if 121 <= row['Due Date Days'] <= 180 else 0, axis=1)
main_df['180 +'] = main_df.apply(lambda row: row['Invoice Amount'] if row['Due Date Days'] >= 180 else 0, axis=1)
main_df['Asset'] = main_df['Asset'].apply(lambda x: 'NA' if (isinstance(x, str) and len(x.split('-')) == 2) else x)
columns_to_fill_na = ['Analitic Code', 'Client Code', 'Date Lease Start', 'Date Report','Invoice Date']
main_df[columns_to_fill_na] = main_df[columns_to_fill_na].fillna('NA')
date_columns = ['Date Lease Start', 'Date Report', 'Invoice Date']
for col in date_columns:
    main_df[col] = pd.to_datetime(main_df[col], format='%m/%d/%Y %I:%M:%S %p', errors='coerce').dt.strftime('%d/%m/%Y')

new_column_order = [
    'Company',
    'Asset Catella',
    'Promotion Code',
    'Tenant Name',
    'Tenant ID',
    'Asset',
    'Promotion ',
    'Analitic Code',  # Corrected from 'Analitic Code' to 'Analytic Code'
    'Client Code',  # Assuming you want the original CIF column
    'Actual Tenant',
    'Date Lease Start',  # Assuming this is the correct column for 'Date Lease Start'
    'Date Report',  # Assuming this is the correct column for 'Date Report'
    'Invoice Date',  # Assuming this is the correct column for 'Invoice Date'
    'Invoice Amount', 
    'Due Date Days',  # Assuming this is the correct column for 'Due Date Days'
    '0-30',
    '31-60',
    '61-90',
    '91-120',
    '121-180',
    '180 +',  # Assuming this should be '180 +' instead of '181 o +'
]



# # Reindex the DataFrame with the new column order
main_df = main_df.reindex(columns=new_column_order)
# Save main_df to Excel
main_df.to_excel("Output__PintoI_4900_Basico_20240531.xlsx", index=False)

print("Combined data saved to main_combined_data.xlsx")