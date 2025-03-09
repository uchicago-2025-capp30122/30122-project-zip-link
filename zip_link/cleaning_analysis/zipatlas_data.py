import requests
import lxml.html as lh
import pandas as pd
import re
from functools import reduce
from zip_link.cleaning_analysis.bulk_data_processing import clean_parks_data, clean_grocery_data, clean_publictransit_data, clean_hospital_data, clean_school_data, clean_population_data
from zip_link.cleaning_analysis.unified_community_health import join_health_df 


def scrape_zipatlas(url, output_csv):
    """
    Scrapes a table with id 'comp' from the given URL where zip-specific 
    housing-related attributes are present and saves it as a CSV file.
    
    Inputs:
    url: The webpage URL to scrape.
    output_csv: The name of the output CSV file.
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        root = lh.fromstring(response.text)
        
        # Locate the table by its ID
        table = root.xpath("//table[@id='comp']")
        
        if table:
            table = table[0]  # Get the first matching table
            
            # Extract headers
            headers = [th.text_content().strip() for th in table.xpath(".//thead//td")]

            # Extract table rows
            rows = []
            for tr in table.xpath(".//tbody//tr"):
                cells = [td.text_content().strip() for td in tr.xpath(".//td")]
                rows.append(cells)
            
            # Convert to DataFrame
            df = pd.DataFrame(rows, columns=headers)
            df = df.iloc[:, 1:3] # Retain 2nd and 3rd rows 
            col_name = re.search(r'/([^/]+)\.csv', output_csv).group(1) # Name column based on output_csv name
            df.columns = ['Zip Code', col_name]

            # Save to CSV
            df.to_csv(output_csv, index=False)
            print(f"Data successfully saved to '{output_csv}'.")
        else:
            print(f"Table with id 'comp' not found in {url}.")
    else:
        print(f"Failed to fetch {url}, status code: {response.status_code}")

def create_zipatlas_data():
    # List of URLs and corresponding output filenames
    urls = [
        ("https://zipatlas.com/us/il/chicago/zip-code-comparison/lowest-property-prices.htm", "data/raw/zipatlas_data/median_property_prices.csv"),
        ("https://zipatlas.com/us/il/chicago/zip-code-comparison/lowest-housing-costs.htm", "data/raw/zipatlas_data/median_housing_costs.csv"),
        ("https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-owner-occupied-housing-costs.htm", "data/raw/zipatlas_data/owner_median_housing_costs.csv"),
        ("https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-renter-occupied-housing-costs.htm", "data/raw/zipatlas_data/renter_median_housing_costs.csv"),
        ("https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-housing-cost-as-percentage-of-income.htm", "data/raw/zipatlas_data/housing_cost_perc_income.csv"),
        ("https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-unemployment-rate.htm", "data/raw/zipatlas_data/unemployment_rates.csv"),
        ("https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-poverty.htm", "data/raw/zipatlas_data/poverty_levels.csv")
    ]

    # Scrape each URL
    for url, filename in urls:
        scrape_zipatlas(url, filename)

     # Read and merge data
    dfs = [pd.read_csv(f) for _, f in urls]
    df_merged = reduce(lambda left, right: pd.merge(left, right, on="Zip Code", how="inner"), dfs)

    return df_merged 

# Merge all data - ZipAtlas and All Other Data Sources

def zip_bulk_data():
    # Load the datasets into DataFrames
    zipatlas_df = create_zipatlas_data()
    comm_health_df = join_health_df()
    parks_count = clean_parks_data("data/raw/parks/CPD_Parks_2025.csv")
    grocery_store_count = clean_grocery_data("data/raw/grocery_stores/grocery_stores_data.csv")
    public_transit_count = clean_publictransit_data("data/raw/public_transit/publictransit_2024.csv")
    hospital_count = clean_hospital_data("data/raw/Hospitals/hospitals.csv")
    school_count = clean_school_data("data/raw/Schools/schools_data.csv")
    Population = clean_population_data("data/raw/Population/Population_Data.csv")


    dfs = [zipatlas_df, comm_health_df, parks_count, grocery_store_count, public_transit_count, hospital_count, school_count, Population]
    dfs = [df.astype({'Zip Code': 'str'}) for df in dfs] # Ensure Zip Code is a string in all dfs
    # Perform left joins iteratively
    final_df = reduce(lambda left, right: pd.merge(left, right, on='Zip Code', how='left'), dfs)
    final_df = final_df.fillna(0)
    final_df['total_healthcare_services'] = final_df['cnt_comm_health_ctr'] + final_df['hospital_count']
    final_df = final_df.drop(['cnt_comm_health_ctr', 'hospital_count'], axis=1)

    # Convert all columns other than Zip Code to float
    for col in final_df.columns:
        if col != "Zip Code":
            final_df[col] = (final_df[col].astype(str)  # Ensure strings for cleaning
                .str.replace(r'[^0-9.-]', '', regex=True)  # Remove non-numeric chars
                .astype(float)
            )

    final_df.to_csv("data/preprocessed/zipatlas_bulk_merge.csv", index=False)
    print(f"Zip and Bulk Data merged and successfully saved.")

zip_bulk_data()

def calculate_accessibility_index():
    """
    Computes the Accessibility Index using essential service counts per ZIP code, normalizes it, and updates the combined dataset.
    """
    df = pd.read_csv("data/preprocessed/zipatlas_bulk_merge.csv")

    # Compute total services count per ZIP code
    df["total_services"] = (
        df["total_healthcare_services"]
        + df["park_count"]
        + df["grocery_store_count"]
        + df["num_public_transit_stops"]
        + df["school_count"]
    )

    # Compute Accessibility Index
    df["Accessibility Index"] = df["total_services"] / df["Population"]

    # Debugging: Print min/max values
    min_index = df["Accessibility Index"].min()
    max_index = df["Accessibility Index"].max()
    
    # Round (max - min) to 6 decimal places for better precision
    max_min_diff = round(max_index - min_index, 6)
    print(f"Min Accessibility Index: {min_index}, Max Accessibility Index: {max_index}, Difference: {max_min_diff}")

    # Normalize the Accessibility Index 
    df["Normalized Accessibility Index"] = (
        (df["Accessibility Index"] - min_index) / max_min_diff
    ).round(2)
    
    # Save updated combined dataset
    df.to_csv("data/preprocessed/zipatlas_bulk_merge.csv", index=False)
    print("Accessibility Index calculated, normalized, and added to combined dataset.")
    return df[["Zip Code", "Accessibility Index", "Normalized Accessibility Index"]]

calculate_accessibility_index()



