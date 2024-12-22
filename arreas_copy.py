import pandas as pd
import os

# Define the path to your source Excel file
source_file = "Pinto I_Madrid/Arrears/Deuda_Pinto_I_4900_20240531_V7.xlsx"

# Check if there is a V7 version of the file
use_v7 = "V7" in source_file

# Define the sheets you want to extract
sheets_to_extract = ["RETAINER", "FINISHED", "RENTED"]  # Add more sheet names as needed

# Define the path for the combined output file
output_file = "combined_sheets.xlsx"

# Create an empty DataFrame to hold the combined data
combined_data = pd.DataFrame()

# Create a new Excel writer object for the combined output file
with pd.ExcelWriter(output_file) as combined_writer:
    # Loop through the sheets and write each one to the new Excel file
    for sheet_name in sheets_to_extract:
        # Read the specific sheet from the source file, skipping the first 8 rows
        df = pd.read_excel(source_file, sheet_name=sheet_name, skiprows=8)
        
        # Ensure the required columns are present in the DataFrame
        required_columns = ['Tenant', 'DNI/NIF', 'Asset', 'Sheet', 'Lease contract start', 'Day of report', 'Invoice date', 'Due date days', 'Total Debt Receipt']
        for col in required_columns:
            if col not in df.columns:
                df.insert(len(df.columns), col, None)  # Insert the missing column with None values
        
        # Filter out rows where 'Tenant' starts with 'Total'
        df = df[~df['Tenant'].astype(str).str.startswith('Total')]
        
        # Modify 'Asset' column if using the V7 file
        if use_v7:
            print('offrkre')
            df['Asset'] = df['Asset'].apply(lambda x: x.rsplit('-', 1)[0].strip() if (isinstance(x, str) and '/' in x ) else x)
        # df['Asset'] = df['Asset'].apply(lambda x: 'NA' if (isinstance(x, str) and len(x.split('-')) == 2) else x)
        # Extract the desired columns and add them to the combined DataFrame
        extracted_data = df[required_columns].copy()
        extracted_data['Sheet'] = sheet_name  # Add a column to indicate the sheet name
    
        combined_data = pd.concat([combined_data, extracted_data], ignore_index=True)
        
        # Write the original DataFrame to the combined Excel file
        df.to_excel(combined_writer, sheet_name=sheet_name, index=False)
        print(f"Extracted and combined {sheet_name} into {output_file}")
    
    # Write the combined data to a new sheet in the combined output file
    combined_data.to_excel(combined_writer, sheet_name='Combined_Data', index=False)
    print(f"Extracted columns and combined data into 'Combined_Data' sheet in {output_file}")

# Define the path for the output file containing the combined data
combined_output_file = "Arreas_data.xlsx"

# Save the combined data into a new Excel file
combined_data.to_excel(combined_output_file, index=False)
print(f"Saved combined data into {combined_output_file}")
