import os
import pandas as pd
# from slugify import slugify

# Define file paths
promotion_file = "New_Promociones_Catella_Cod.xlsx"
rentroll_file_path = r"c:\Users\sanya\Downloads\Output_Adania2024\Output_Adania2024\07.july\D_240731_Ezcaba I_CWE-06_RR.xlsx"
income_file_path = r"c:\Users\sanya\Downloads\OneDrive_1_9-5-2024\07 July\Ezcaba I\FACTURACION ALQUILER Catella RENTAS JULIO 2024 (Envio CATELLA).xlsx"
input_promotion = "06 Pamplona - Ezcaba I"
sheet_name='Al008-67 Ezcaba'
# Vitoria S
# Vitoria Z
# 06 Pamplona - Sarriguren
# 06 Pamplona - Ezcaba I

# Load the promotion data
extract_promotion = pd.read_excel(promotion_file, dtype=str)

# Filter the promotion data based on the input promotion
# 
filtered_data = extract_promotion[extract_promotion["Promotion path"] == input_promotion].copy()

# Extract relevant columns and rename 'Promotion' to 'Promotion Name'
extracted_columns = filtered_data[["Company", "Asset Catella", "Promotion Code", "Promotion", "Society Extraction"]].copy()
extracted_columns.rename(columns={"Promotion": "Promotion Name"}, inplace=True)

input_income = pd.ExcelFile(income_file_path)
rentroll_df = pd.read_excel(rentroll_file_path, dtype=str)

# Strip and lower the 'Tenant 1 Name' column in the rentroll DataFrame
rentroll_df['Tenant 1 Name'] = rentroll_df['Tenant 1 Name']

# Debug: Print column names of the rentroll DataFrame
print("Rentroll DataFrame Columns:")
print(rentroll_df.columns)

print(input_income.sheet_names,sheet_name)
if 'Al008-67 Ezcaba' in input_income.sheet_names or 'Sarriguren income'  in input_income.sheet_names :
    print(sheet_name,)
    initial_data = input_income.parse(sheet_name=sheet_name, skiprows=0)
    first_value=initial_data['Unnamed: 15'].iloc[1]
    first_values = pd.to_datetime(first_value)    # Print or store the extracted value
    # formatted_first_value = first_value.strftime('%d/%m/%Y')
        
        # Print or store the formatted date value
    print("First value in 'Unnamed: 15':", first_values)
    income_file = input_income.parse(sheet_name=sheet_name,skiprows=4)
    income_file.rename(columns={'Unnamed: 4': 'Tenant'}, inplace=True)
    income_file = income_file.dropna(subset=['Vivienda'])
    income_file = income_file.iloc[:-1]
    income_file.to_excel('ww.xlsx',index=False)
    
        
elif 'AL009-RC-37' in input_income.sheet_names or 'AL010-RC PA2' in input_income.sheet_names:
    print(sheet_name,'ppp')
    initial_data = input_income.parse(sheet_name=sheet_name, skiprows=0)
    first_value=initial_data['Unnamed: 23'].iloc[1]
    print(first_value,'first_valuefirst_valuefirst_value')
    first_values = pd.to_datetime(first_value)    # Print or store the extracted value
    # formatted_first_value = first_value.strftime('%d/%m/%Y')
        
        # Print or store the formatted date value
    print("First value in 'Unnamed: 15':", first_values)
    initial_data = input_income.parse(sheet_name=sheet_name, skiprows=0)
    # print(initial_data['Unnamed: 15'].iloc[1])
        # Extract the first value from 'Unnamed: 15' column
    first_value=initial_data['Unnamed: 15'].iloc[1]
    income_file = input_income.parse(sheet_name=sheet_name, skiprows=4)# manually changed
    income_file.rename(columns={'Unnamed: 10': 'Tenant'}, inplace=True)
    
    # income_file['Date Lease Start'] = pd.to_datetime(income_file['Contrato'], errors='coerce')
    # income_file['Date Lease Start'] = income_file['Date Lease Start'].dt.strftime('%d/%m/%Y')
    income_file = income_file.dropna(subset=['Piso'])
    income_file = income_file.iloc[:-1]
    income_file.to_excel('else.xlsx',index=False)
income_file['Invoice Date'] = first_values
print(income_file['Invoice Date'],'aaaaaaaaaaaaa')
# income_file['Invoice Date'] = income_file['Invoice Date'].dt.strftime('%d/%m/%Y')
income_file['Date Lease Start'] = pd.to_datetime(income_file['Contrato'], errors='coerce')
income_file['Date Lease Start'] = income_file['Date Lease Start'].dt.strftime('%d/%m/%Y')
# Print the 'Tenant' column from the income_file DataFrame
income_file['Tenant'] = income_file['Tenant']

# Perform the filtering based on matching tenant names
filtered_rentroll = rentroll_df[rentroll_df['Tenant 1 Name'].isin(income_file['Tenant'])]


# Extract the relevant columns: Id Asset, Tenant 1 Name, Customer Code
filtered_rentroll = filtered_rentroll[['Id Asset', 'Tenant 1 Customer Code']]
filtered_rentroll = filtered_rentroll.rename(columns={
    'Id Asset': 'Asset',
    'Tenant 1 Customer Code': 'Client Code'
})
# Create new data columns DataFrame
new_data_columns = pd.DataFrame({
'Analitic code': ['NA'] * len(income_file),
    'DNI': ['NA'] * len(income_file),
    'Payment Method': ['NA'] * len(income_file),
    'Tenant':income_file['Tenant'],
    'Invoice Date': income_file['Invoice Date'],
    'Date Lease Start':income_file['Date Lease Start'],
    'House Rent':income_file['Renta Mes'],
    'Total Rent':income_file['Renta Mes'],
   
})
# List of columns to add with default value 0
columns_to_add = ['Storage Room Rent', 'Garage Rent', 'IBI','Rent Insurance','Supplies','IPC','VAT']
# Add columns with default value 0 using a for loop
for column in columns_to_add:
    new_data_columns[column] = [0] * len(income_file)
# Add the columns from extracted_columns to new_data_columns
for col in extracted_columns.columns:
    if not extracted_columns.empty:
        new_data_columns[col] = extracted_columns[col].iloc[0]
    else:
        new_data_columns[col] = 'NA'
# Determine column names based on the sheet name
if sheet_name == sheet_name:
    print('Gtos.Cdad')
    column_name = 'Subv.G.N.'
    sc_column = 'Gtos.Cdad'
else:
    print('Gtos Cdad,else')
    column_name = 'Subvencion'
    sc_column = 'Gtos Cdad'
# Update the 'SC' column based on the determined column name
if sc_column in income_file.columns:
    new_data_columns['SC'] = income_file[sc_column]
else:
    new_data_columns['SC'] = ['NA'] * len(income_file)

# Check if the determined column exists and update columns accordingly
if column_name in income_file.columns:
    new_data_columns['Other Expenses'] = income_file[column_name].astype(str).apply(lambda x: f"-{x.strip()}")
else:
    new_data_columns['Other Expenses'] = ['NA'] * len(income_file)
# Convert 'Invoice Date' to datetime

# Convert 'Date Lease Start' to datetime
new_data_columns['Date Lease Start'] = pd.to_datetime(new_data_columns['Date Lease Start'], errors='coerce')
# Convert 'Other Expenses' to numeric, with errors coerced to NaN
new_data_columns['Other Expenses'] = pd.to_numeric(new_data_columns['Other Expenses'], errors='coerce')

# Calculate 'Final Amount'
new_data_columns['Final Amount'] = new_data_columns['Total Rent']+new_data_columns['SC'] + new_data_columns['Other Expenses']
new_data_columns['Invoice Date'] = pd.to_datetime(new_data_columns['Invoice Date'], errors='coerce')
print(new_data_columns['Invoice Date'],'test')
# Set 'Date' column to the last date of the month of the 'Invoice Date'
new_data_columns['Date'] = new_data_columns['Invoice Date'] + pd.offsets.MonthEnd(0)

# Format 'Date' column as DD/MM/YY
new_data_columns['Date'] = new_data_columns['Date'].dt.strftime('%d/%m/%Y')
print(new_data_columns['Date'],'sssssssssssss')

# Optionally, format 'Invoice Date' and 'Date Lease Start' if you need them in a specific string format

new_data_columns['Date Lease Start'] = new_data_columns['Date Lease Start'].dt.strftime('%d/%m/%Y')
new_data_columns['Invoice Date'] = new_data_columns['Invoice Date'].dt.strftime('%d/%m/%Y')
print(new_data_columns['Invoice Date'],'okkk')




# Concatenate extracted columns with new data columns
final_data = pd.concat([new_data_columns,filtered_rentroll], axis=1)
final_data = final_data.fillna('NA')
desired_column_order = [
            "Company",
            "Asset Catella",
            "Date",
            "Asset",
            "Promotion Code",
            "Promotion Name",
            "Analitic code",
            "Date Lease Start",
            "Invoice Date",
            "Client Code",
            "Tenant",
            "DNI",
            "Payment Method",
            "House Rent",
            "Storage Room Rent",
            "Garage Rent",
            "Total Rent",
            "SC",
            "IBI",
            "Rent Insurance",
            "Supplies",
            "Other Expenses",
            "IPC",
            "VAT",
            "Final Amount",

        ]

        # Reorder columns in the DataFrame
final_data = final_data[desired_column_order]
year=2024
output_dir = os.path.join(os.getcwd(), "arrears_op")
os.makedirs(output_dir, exist_ok=True)

Society = extracted_columns['Society Extraction'].iloc[0]

# Define the output file path using the formatted string
output_file_name = f"D_{year}_{final_data['Promotion Name'].iloc[0]}_{Society}_Incomes.xlsx"

# Combine the output file path with the current working directory
output_file_path = os.path.join(output_dir, output_file_name)

# Save the final data to an Excel file
final_data.to_excel(output_file_path, index=False)

print(f"Data successfully extracted to {output_file_path}")