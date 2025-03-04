import requests
import lxml.html as lh
import pandas as pd
import re
from functools import reduce
from zip_link.cleaning_analysis.bulk_data_processing import clean_parks_data, clean_grocery_data, clean_publictransit_data


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
        ("https://zipatlas.com/us/il/chicago/zip-code-comparison/lowest-property-prices.htm", "../data/raw/zipatlas_data/median_property_prices.csv"),
        ("https://zipatlas.com/us/il/chicago/zip-code-comparison/lowest-housing-costs.htm", "../data/raw/zipatlas_data/median_housing_costs.csv"),
        ("https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-owner-occupied-housing-costs.htm", "../data/raw/zipatlas_data/owner_median_housing_costs.csv"),
        ("https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-renter-occupied-housing-costs.htm", "../data/raw/zipatlas_data/renter_median_housing_costs.csv"),
        ("https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-housing-cost-as-percentage-of-income.htm", "../data/raw/zipatlas_data/housing_cost_perc_income.csv"),
        ("https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-unemployment-rate.htm", "../data/raw/zipatlas_data/unemployment_rates.csv"),
        ("https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-poverty.htm", "../data/raw/zipatlas_data/poverty_levels.csv")
    ]

    # Scrape each URL
    for url, filename in urls:
        scrape_zipatlas(url, filename)

     # Read and merge data
    dfs = [pd.read_csv(f) for _, f in urls]
    df_merged = reduce(lambda left, right: pd.merge(left, right, on="Zip Code", how="inner"), dfs)

    return df_merged

# Merge all data - ZipAtlas and Community Health Centre Data

def zip_health_bulk_data():
    # Load the datasets into DataFrames
    #zipatlas_df = pd.read_csv("zipatlas.csv")
    zipatlas_df = create_zipatlas_data()
    comm_health_df = pd.read_csv("../data/preprocessed/unified_community_health_count.csv")
    parks_count = clean_parks_data("../data/raw/parks/CPD_Parks_2025.csv")
    grocery_store_count = clean_grocery_data("../data/raw/grocery_stores/grocery_stores_data.csv")
    public_transit_count = clean_publictransit_data("../data/raw/public_transit/publictransit_2024.csv")

    dfs = [zipatlas_df, comm_health_df, parks_count, grocery_store_count, public_transit_count]
    dfs = [df.astype({'Zip Code': 'str'}) for df in dfs] # Ensure Zip Code is a string in all dfs
    # Perform left joins iteratively
    final_df = reduce(lambda left, right: pd.merge(left, right, on='Zip Code', how='left'), dfs)
    final_df = final_df.fillna(0)

    # Convert all columns other than Zip Code to float
    for col in final_df.columns:
        if col != "Zip Code":
            final_df[col] = (final_df[col].astype(str)  # Ensure strings for cleaning
                .str.replace(r'[^0-9.-]', '', regex=True)  # Remove non-numeric chars
                .astype(float)
            )

    final_df.to_csv("../data/preprocessed/zipatlas_bulk_merge.csv", index=False)
    print(f"Zip and Bulk Data merged and successfully saved.")

zip_health_bulk_data()



