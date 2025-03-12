import pytest
import pandas as pd
from zip_link.cleaning_analysis.bulk_data_processing import clean_parks_data, clean_grocery_data, clean_publictransit_data, clean_hospital_data, clean_school_data, clean_population_data
from zip_link.cleaning_analysis.zipatlas_data import zip_bulk_data, create_zipatlas_data, scrape_zipatlas
from zip_link.cleaning_analysis.unified_community_health import join_health_df
from functools import reduce

@pytest.fixture
def test_data():
    """Fixture to set up initial data for testing."""
    # Mock or create the DataFrames that are used in the function
    zipatlas_df = create_zipatlas_data()
    comm_health_df = join_health_df()
    parks_count = clean_parks_data("data/raw/parks/CPD_Parks_2025.csv")
    grocery_store_count = clean_grocery_data("data/raw/grocery_stores/grocery_stores_data.csv")
    public_transit_count = clean_publictransit_data("data/raw/public_transit/publictransit_2024.csv")
    hospital_count = clean_hospital_data("data/raw/hospitals/hospitals.csv")
    school_count = clean_school_data("data/raw/schools/schools_data.csv")
    Population = clean_population_data("data/raw/population/Population_Data.csv")

    dfs = [zipatlas_df, comm_health_df, parks_count, grocery_store_count, public_transit_count, hospital_count, school_count, Population]
    dfs = [df.astype({'Zip Code': 'str'}) for df in dfs]  # Ensure Zip Code is a string in all dfs
    # Perform the left joins iteratively
    final_df = reduce(lambda left, right: pd.merge(left, right, on='Zip Code', how='left'), dfs)
    final_df = final_df.fillna(0)
    final_df['total_healthcare_services'] = final_df['cnt_comm_health_ctr'] + final_df['hospital_count']
    final_df = final_df.drop(['cnt_comm_health_ctr', 'hospital_count'], axis=1)

    # Convert all columns other than Zip Code to float
    for col in final_df.columns:
        if col != "Zip Code":
            final_df[col] = (final_df[col].astype(str)
                             .str.replace(r'[^0-9.-]', '', regex=True)
                             .astype(float)
                             )

    return final_df, zipatlas_df

def test_correct_row_count(test_data):
    """Test that the final DataFrame has the same number of rows as zipatlas_df."""
    final_df, zipatlas_df = test_data
    assert len(final_df) == len(zipatlas_df), "The number of rows in the final DataFrame does not match the left DataFrame (zipatlas_df)"

def test_no_unexpected_nans(test_data):
    """Test that there are no unexpected NaN values in the merged DataFrame."""
    final_df, _ = test_data
    for col in final_df.columns:
        assert final_df[col].notna().all(), f"Unexpected NaN values in column {col}"

def test_columns_are_float(test_data):
    """Test that all columns except Zip Code are of type float after the transformation."""
    final_df, _ = test_data
    non_zip_columns = final_df.columns[final_df.columns != 'Zip Code']
    assert (final_df[non_zip_columns].dtypes == 'float').all(), "Not all columns are of type float"

def test_zip_health_bulk_data_not_empty(test_data):
    """Test that the merged DataFrame is not empty."""
    final_df, _ = test_data
    assert not final_df.empty, "The merged DataFrame is empty!"


def test_zip_code_unique(test_data):
    """Test that the 'Zip Code' column has unique values (no duplicates)."""
    final_df, _ = test_data
    assert final_df['Zip Code'].is_unique, "'Zip Code' column contains duplicate values!"


