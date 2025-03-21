import requests
import lxml.html as lh
import pandas as pd
import re
from functools import reduce
from zip_link.cleaning_analysis.bulk_data_processing import clean_parks_data, clean_grocery_data, clean_publictransit_data, clean_hospital_data, clean_school_data, clean_population_data
from zip_link.cleaning_analysis.unified_community_health import join_health_df 
from zip_link.cleaning_analysis.accessibility_index import calculate_accessibility_index


def scrape_zipatlas(url, output_csv):
    """
    Scrapes a table with id 'comp' from the given URL where zip-specific 
    housing-related attributes are present and saves it as a CSV file.
    
    Inputs:
    url (str): The webpage URL to scrape.
    output_csv (path): The name of the output CSV file.
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
            col_name = re.search(r'/([^/]+)\.csv', output_csv).group(1) 
            df.columns = ['Zip Code', col_name] # Name 2nd column based on output_csv name

            # Save to CSV
            df.to_csv(output_csv, index=False)
            print(f"Data successfully saved to '{output_csv}'.")
        else:
            print(f"Table with id 'comp' not found in {url}.")
    else:
        print(f"Failed to fetch {url}, status code: {response.status_code}")

def create_zipatlas_data():

    """
    Scrape all the 7 urls of relevance from ZipAtlas, and inner joins all the data into one dataframe using Zip Code as the key
    
    Returns: 
    merged_df (DataFrame): merged dataframe with Zip Code and all the housing-related variables of relevance.

    """

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


def zip_bulk_data():

    """
    - Merges all our data sources together but pre-processing each one of them and executing left joins iteratively. The key for these joins will once again be Zip Code.
    - Create a new column called total_healthcare_services which is the sum of hospitals and community health centers. 
    - Convert all columns except Zip Code to floats
    - Saves this data in the data/preprocessed folder
    - Adds the Accessibility Index at the end and also saves the final file to the data/preprocessed folder

    """

    # Load the datasets into DataFrames
    zipatlas_df = create_zipatlas_data()
    comm_health_df = join_health_df()
    parks_count = clean_parks_data("data/raw/parks/CPD_Parks_2025.csv")
    grocery_store_count = clean_grocery_data("data/raw/grocery_stores/grocery_stores_data.csv")
    public_transit_count = clean_publictransit_data("data/raw/public_transit/publictransit_2024.csv")
    hospital_count = clean_hospital_data("data/raw/hospitals/hospitals.csv")
    school_count = clean_school_data("data/raw/schools/schools_data.csv")
    population = clean_population_data("data/raw/population/Population_Data.csv")


    dfs = [zipatlas_df, comm_health_df, parks_count, grocery_store_count, public_transit_count, hospital_count, school_count, population]
    dfs = [df.astype({'Zip Code': 'str'}) for df in dfs] # Ensure Zip Code is a string in all dfs

    # Perform left joins iteratively
    final_df = reduce(lambda left, right: pd.merge(left, right, on='Zip Code', how='left'), dfs)
    final_df = final_df.fillna(0)

    # Sum hospitals and comm_health_ctr count for new column and drop the original 2 
    final_df['total_healthcare_services'] = final_df['cnt_comm_health_ctr'] + final_df['hospital_count'] 
    final_df = final_df.drop(['cnt_comm_health_ctr', 'hospital_count'], axis=1)

    # Convert all columns other than Zip Code to float
    for col in final_df.columns:
        if col != "Zip Code":
            final_df[col] = (final_df[col].astype(str)  # Ensure strings for cleaning
                .str.replace(r'[^0-9.-]', '', regex=True)  # Remove non-numeric units
                .astype(float)
            )

    final_df.to_csv("data/preprocessed/zipatlas_bulk_merge.csv", index=False)
    print(f"Zip and Bulk Data merged and successfully saved.")
    calculate_accessibility_index("data/preprocessed/zipatlas_bulk_merge.csv")


if __name__ == "__main__":
    zip_bulk_data()



