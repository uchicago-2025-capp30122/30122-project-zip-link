from zip_link.cleaning_analysis.zipatlas_data import scrape_zipatlas, create_zipatlas_data
import os 
import pandas as pd 

def test_scraping_works():
    url = 'https://zipatlas.com/us/il/chicago/zip-code-comparison/lowest-property-prices.htm'
    output_csv = 'data/raw/zipatlas_data/test_output.csv'
    # Test real URL scraping
    scrape_zipatlas(url, output_csv)
    # Check that the file has been created
    assert os.path.exists(output_csv), f"{output_csv} should have been created."
    # Read the CSV and validate its content
    df = pd.read_csv(output_csv)
    assert not df.empty, "Dataframe is empty."

    # Clean up
    os.remove(output_csv)

def test_successful_merge():
    df = create_zipatlas_data()
    assert 'Zip Code' in df.columns, "Zip Code column is missing."
    assert df.shape[1] == 8, f"Expected 8 columns, but got {df.shape[1]} columns."


def test_no_missing_values():
    # Call the function to create the data
    df = create_zipatlas_data()
    # Check that the DataFrame has no missing values
    assert df.isnull().sum().sum() == 0, "There are missing values in the dataframe."



