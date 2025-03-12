import pdfplumber
import csv
import pandas as pd
import re
import tabula
import jellyfish 

def convert_pdf_to_csv(pdf_path, csv_path):
    df = tabula.read_pdf(pdf_path, pages='all')[0]
    tabula.convert_into(pdf_path, csv_path, output_format="csv", pages='all')
    print(f"Successfully converted '{pdf_path}' to '{csv_path}'")

# if __name__ == "__main__":
#     pdf_file_path = 'data/raw/community_health_ctr/HealthCentre1.pdf'
#     csv_file_path = 'data/raw/community_health_ctr/healthcentre_pdf.csv'
#     convert_pdf_to_csv(pdf_file_path, csv_file_path)
#     print(f"Successfully converted '{pdf_file_path}' to '{csv_file_path}'")
    
def process_health_data(input_file):
    # Load the dataset
    df = pd.read_csv(input_file)
    df = df.iloc[:, :3] # Filter out first 3 columns only as the rest are empty
    df.columns = ['Health Center Facility', 'Address', 'Telephone Number'] # Rename
    # Drop rows where 'Health Center Facility' column is null
    df = df.dropna(subset=["Health Center Facility"])
    # Fill NaN values in the rest of the DataFrame with an empty string
    df = df.fillna("")
    # Remove trailing and leading spaces
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    # Get phone number 
    df['Telephone Number'] = df['Telephone Number'].apply(
    lambda x: re.sub(r'\s+', '', x) if pd.notnull(x) else ''  # Remove all spaces
    )
    df['Telephone Number'] = df['Telephone Number'].str.extract(r"(\d{3}-\d{3}-\d{4})")
    # Extract any 5-digit ZIP code using regex
    df["Zip Code"] = df["Address"].apply(
        lambda x: re.search(r"\b\d{5}\b", x).group() if re.search(r"\b\d{5}\b", x) else None
    )
    # Remove rows without valid ZIP codes
    df = df.dropna(subset=["Zip Code"]) 
    return df 

def get_hrsa_data(path):
    # Load Data
    df = pd.read_csv(path)
     # Keep only Chicago rows
    df_chicago = df[df["City"].str.lower() == "chicago"]
    # Drop duplicates across combination of Health Center Name, Operated By, ZIP Code and Telephone Number and rename ZIP Code to Zip Code
    df_chicago_unique = df_chicago.drop_duplicates(['Health Center Name', 'Operated By', 'ZIP Code', 'Telephone Number']) 
    df_chicago_unique = df_chicago_unique.rename(columns={'ZIP Code': 'Zip Code'})
    df_chicago_unique.loc[:, "Zip Code"] = df_chicago_unique["Zip Code"].astype(str).str[:5]
    # Remove trailing and leading spaces
    df_chicago_unique = df_chicago_unique.map(lambda x: x.strip() if isinstance(x, str) else x)
    # Get phone number 
    df_chicago_unique['Telephone Number'] = df_chicago_unique['Telephone Number'].apply(
    lambda x: re.sub(r'\s+', '', x) if pd.notnull(x) else ''  # Remove all spaces
    )    
    df_chicago_unique['Telephone Number'] = df_chicago_unique['Telephone Number'].str.extract(r"(\d{3}-\d{3}-\d{4})")
    # Subset data and rename columns to standardize with other data source 
    df_chicago_unique = df_chicago_unique[['Health Center Name', 'Street Address', 'Telephone Number', 'Zip Code']]
    df_chicago_unique.columns = ['Health Center Facility', 'Address', 'Telephone Number', 'Zip Code']
    return df_chicago_unique

def fuzzy_match(df, threshold=0.85):
    """Deduplicates health centers within combined dataset using fuzzy matching."""
    matched_indices = set()
    records = df.to_dict(orient="records")
    unique_records = []

    for i, rec1 in enumerate(records):
        if i in matched_indices:
            continue  # Skip already matched records
        
        for j, rec2 in enumerate(records[i+1:], start=i+1):
            if j in matched_indices:
                continue
            
            # Compare health center names and addresses
            name_sim = jellyfish.jaro_winkler_similarity(rec1["Health Center Facility"], rec2["Health Center Facility"])
            addr_sim = jellyfish.jaro_winkler_similarity(rec1["Address"], rec2["Address"]) if rec1["Address"] and rec2["Address"] else 0
            telephone_sim = rec1["Telephone Number"] == rec2["Telephone Number"]

            
            # If similarity is above threshold for both entities, mark as duplicate
            if (name_sim > threshold or addr_sim > threshold) and telephone_sim:
                matched_indices.add(j)
        
        unique_records.append(rec1)  # Keep the first unique record
    return pd.DataFrame(unique_records) 

def join_health_df():
    convert_pdf_to_csv("data/raw/community_health_ctr/HealthCentre1.pdf", "data/raw/community_health_ctr/healthcentre_pdf.csv")
    pdf_data = process_health_data("data/raw/community_health_ctr/healthcentre_pdf.csv")
    hrsa_data = get_hrsa_data("data/raw/community_health_ctr/HRSA_Data.csv")
    combined_data = pd.concat([pdf_data, hrsa_data], ignore_index=True)
    cleaned_data = fuzzy_match(combined_data)
    #combined_data = combined_data.drop_duplicates(['Health Center Facility', 'Address'])
    cleaned_data.to_csv("data/preprocessed/unified_community_health_data.csv", index=False)
    zip_counts = cleaned_data["Zip Code"].value_counts().reset_index()
    zip_counts.columns = ["Zip Code", "cnt_comm_health_ctr"]
    zip_counts.to_csv("data/preprocessed/unified_community_health_count.csv", index=False)
    return zip_counts







