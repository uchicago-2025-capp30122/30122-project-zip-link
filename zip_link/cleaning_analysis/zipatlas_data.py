import requests
import lxml.html as lh
import pandas as pd
import re
from functools import reduce


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

# List of URLs and corresponding output filenames
urls = [
    ("https://zipatlas.com/us/il/chicago/zip-code-comparison/lowest-property-prices.htm", "/home/vyshnaviv/capp122/30122-project-zip-link/zip_link/data/raw/zipatlas_data/median_property_prices.csv"),
    ("https://zipatlas.com/us/il/chicago/zip-code-comparison/lowest-housing-costs.htm", "/home/vyshnaviv/capp122/30122-project-zip-link/zip_link/data/raw/zipatlas_data/median_housing_costs.csv"),
    ("https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-owner-occupied-housing-costs.htm", "/home/vyshnaviv/capp122/30122-project-zip-link/zip_link/data/raw/zipatlas_data/owner_median_housing_costs.csv"),
    ("https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-renter-occupied-housing-costs.htm", "/home/vyshnaviv/capp122/30122-project-zip-link/zip_link/data/raw/zipatlas_data/renter_median_housing_costs.csv"),
    ("https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-housing-cost-as-percentage-of-income.htm", "/home/vyshnaviv/capp122/30122-project-zip-link/zip_link/data/raw/zipatlas_data/housing_cost_perc_income.csv"),
    ("https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-unemployment-rate.htm", "/home/vyshnaviv/capp122/30122-project-zip-link/zip_link/data/raw/zipatlas_data/unemployment_rates.csv"),
    ("https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-poverty.htm", "/home/vyshnaviv/capp122/30122-project-zip-link/zip_link/data/raw/zipatlas_data/poverty_levels.csv")
]

# Scrape each URL
for url, filename in urls:
    scrape_zipatlas(url, filename)

def join_data_on_zip():
    filenames = ["/home/vyshnaviv/capp122/30122-project-zip-link/zip_link/data/raw/zipatlas_data/median_property_prices.csv", "/home/vyshnaviv/capp122/30122-project-zip-link/zip_link/data/raw/zipatlas_data/median_housing_costs.csv",
                 "/home/vyshnaviv/capp122/30122-project-zip-link/zip_link/data/raw/zipatlas_data/owner_median_housing_costs.csv","/home/vyshnaviv/capp122/30122-project-zip-link/zip_link/data/raw/zipatlas_data/renter_median_housing_costs.csv",
                 "/home/vyshnaviv/capp122/30122-project-zip-link/zip_link/data/raw/zipatlas_data/housing_cost_perc_income.csv","/home/vyshnaviv/capp122/30122-project-zip-link/zip_link/data/raw/zipatlas_data/poverty_levels.csv",
                 "/home/vyshnaviv/capp122/30122-project-zip-link/zip_link/data/raw/zipatlas_data/unemployment_rates.csv"]
    
    dfs = [pd.read_csv(f) for f in filenames]

    df_merged = reduce(
    lambda left, right: pd.merge(left, right, on="Zip Code", how="inner"),
    dfs)

    # df_merged.to_csv("zipatlas.csv", index=False)
    return df_merged

join_data_on_zip()

# Merge all data - ZipAtlas and Community Health Centre Data

def zip_health_data():
    # Load the datasets into DataFrames
    #zipatlas_df = pd.read_csv("zipatlas.csv")
    zipatlas_df = join_data_on_zip()
    comm_health_df = pd.read_csv("/home/vyshnaviv/capp122/30122-project-zip-link/zip_link/data/preprocessed/unified_community_health_count.csv")
    merged_data = pd.merge(zipatlas_df, comm_health_df, on="Zip Code", how="left")
    merged_data['cnt_comm_health_ctr'] = merged_data['cnt_comm_health_ctr'].fillna(0)
    merged_data.to_csv("/home/vyshnaviv/capp122/30122-project-zip-link/zip_link/data/preprocessed/zipatlas_health.csv", index=False)
    print(f"Zip and Community Health Centre Data successfully saved.")

zip_health_data()

