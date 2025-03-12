import pdfplumber
import csv
import pandas as pd
import re
import tabula
import jellyfish 

def convert_pdf_to_csv(pdf_path, csv_path):
    """
    Converts a pdf into csv

    Input: 
    pdf_path (path): path of the pdf to be converted
    csv_path (path): path of where the converted pdf is to be stored

    """
    df = tabula.read_pdf(pdf_path, pages='all')[0]
    tabula.convert_into(pdf_path, csv_path, output_format="csv", pages='all')
    print(f"Successfully converted '{pdf_path}' to '{csv_path}'")
    
def process_health_data(input_file):
    """
    Processes the community health center data from the pdf. 
    - Filters relevant columns and renames them
    - Drops rows where 'Health Center Facility' column is null
    - Fill NaN values in the rest of the DataFrame with an empty string
    - Remove trailing and leading spaces in the dataset
    - Extract Telephone Number by removing extra spaces and getting format XXX-XXX-XXXX
    - Extract 5-digit zip code using regex and drop rows with invalid zip codes

    Input: 
    input_file (path): path of the converted pdf on health centers

    Returns: 
    df (dataframe): preprocessed dataset

    """
    # Load the dataset
    df = pd.read_csv(input_file)

    # Filter out relevant columns and rename them
    df = df.iloc[:, :3].set_axis(['Health Center Facility', 'Address', 'Telephone Number'], axis=1)

    # Drop rows where where 'Health Center Facility' is null, fill NaNs with empty strings and remove trailing/leading spaces
    df = (df.dropna(subset=["Health Center Facility"]).fillna("")  
        .map(lambda x: x.strip() if isinstance(x, str) else x))  

    # Get Telephone Number in the desired format 
    df["Telephone Number"] = df["Telephone Number"].str.replace(r"\s+", "", regex=True).str.extract(r"(\d{3}-\d{3}-\d{4})")

    # Extract any 5-digit ZIP code using regex
    df["Zip Code"] = df["Address"].str.extract(r"\b(\d{5})\b")

    # Remove rows without valid ZIP codes
    df = df.dropna(subset=["Zip Code"]) 

    return df 

def get_hrsa_data(path):

    """
    Processes the HRSA data  
    - Filters relevant columns, drop duplicates and rename them
    - Extract 5-digit ZIP code and remove trailing and leading spaces across df
    - Extract Telephone Number by removing extra spaces and getting format XXX-XXX-XXXX
    - Subset data and rename columns to standardize with other data source 

    Input: 
    input_file (path): path of the raw HRSA data

    Returns: 
    df (dataframe): preprocessed dataset

    """
    # Load Data
    df = pd.read_csv(path)

    # Filter Chicago rows only, drop duplicates over combination of columns and rename ZIP Code to Zip Code
    df = df[df["City"].str.lower() == "chicago"].drop_duplicates(
        ["Health Center Name", "Operated By", "ZIP Code", "Telephone Number"]
    ).rename(columns={"ZIP Code": "Zip Code"})  

    # Extract 5-digit ZIP code and remove trailing and leading spaces across df
    df.loc[:, "Zip Code"] = df["Zip Code"].astype(str).str[:5]
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

    # Get Telephone Number
    df["Telephone Number"] = df["Telephone Number"].str.replace(r"\s+", "", regex=True
                                                                ).str.extract(r"(\d{3}-\d{3}-\d{4})")

    # Subset data and rename columns to standardize with other data source 
    df = df[['Health Center Name', 'Street Address', 'Telephone Number', 'Zip Code']]
    df.columns = ['Health Center Facility', 'Address', 'Telephone Number', 'Zip Code']
    return df

def fuzzy_match(df, threshold=0.85):
    """
    Deduplicates health centers within combined dataset using jaro_winkler_similarity.
    If name_sim or addr_sim is greater than the threshold, AND if telephone_sim is True between 2 rows, second row is considered a duplicate

    Input: 
    df (dataframe): combined_df with all rows from the pdf and HRSA data
    threshold (int): Cut off for similarity (anything beyond this value is considered a match)

    Returns:
    df (dataframe) with only unique records
    
    """
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
    """
    Joins both sources of community health centers by using all the functions written above
    and returns a count of all community_health_centers for a zip code.

    Returns:
    df (dataframe): 2 columns: Zip Code and count of unique community health centers 
    
    """
    convert_pdf_to_csv("data/raw/community_health_ctr/HealthCentre1.pdf", "data/raw/community_health_ctr/healthcentre_pdf.csv")
    pdf_data = process_health_data("data/raw/community_health_ctr/healthcentre_pdf.csv")
    hrsa_data = get_hrsa_data("data/raw/community_health_ctr/HRSA_Data.csv")
    combined_data = pd.concat([pdf_data, hrsa_data], ignore_index=True)
    cleaned_data = fuzzy_match(combined_data)
    cleaned_data.to_csv("data/preprocessed/unified_community_health_data.csv", index=False)
    zip_counts = cleaned_data["Zip Code"].value_counts().reset_index()
    zip_counts.columns = ["Zip Code", "cnt_comm_health_ctr"]
    zip_counts.to_csv("data/preprocessed/unified_community_health_count.csv", index=False)
    return zip_counts







