import pytest
import pandas as pd
from zip_link.cleaning_analysis.bulk_data_processing import clean_parks_data  
from unittest.mock import patch

@pytest.fixture
def sample_parks_data():
    """Fixture to provide sample parks data for tests."""
    data = {
        "PARK": ["Park A", "Park B", "Park C", "Park A", None],
        "PARK_NO": ['1','2','3','4','5'],
        "LOCATION": ["Location A", "Location B", "Location C", "Location A", "Location E"],
        "ZIP": ["60601", "60602", "60601", "60603", None],
        "PARK_CLASS": ["COMMUNITY PARK", "REGIONAL PARK", "COMMUNITY PARK", "REGIONAL PARK", "CITYWIDE PARK"]

    }
    return pd.DataFrame(data)

def test_drop_null_values(sample_parks_data, tmpdir):
    """Test if rows with missing PARK or ZIP are dropped."""
    # Save the sample data to a CSV
    path = tmpdir.join("sample_parks.csv")
    sample_parks_data.to_csv(path, index=False)
    
    with patch("os.makedirs") as mock_makedirs, patch.object(pd.DataFrame, 'to_csv') as mock_to_csv:
        mock_makedirs.return_value = None  # Mock to do nothing when trying to create directories
        mock_to_csv.return_value = None  # Mock to do nothing when calling to_csv

        # Run the clean_parks_data function (this won't create directories or save files)
        result = clean_parks_data(str(path))
    
    # Assert there are no rows with missing PARK or ZIP
    assert result['Zip Code'].isnull().sum() == 0

def test_valid_park_names(sample_parks_data, tmpdir):
    """Test if invalid park names (no alphabetic characters) are excluded."""
    # Add a park with an invalid name
    new_row = pd.DataFrame([{
    "PARK": "1234",
    "PARK_NO": "2",
    "LOCATION": "Location F",
    "ZIP": "60611",
    "PARK_CLASS": "COMMUNITY PARK"
    }])
    
    sample_parks_data = pd.concat([sample_parks_data, new_row], ignore_index=True)
    # Save the sample data to a CSV
    path = tmpdir.join("sample_parks.csv")
    sample_parks_data.to_csv(path, index=False)
    with patch.object(pd.DataFrame, 'to_csv') as mock_to_csv:
        mock_to_csv.return_value = None  # Mock to do nothing when calling to_csv

        # Run the clean_parks_data function (this won't create directories or save files)
        result = clean_parks_data(str(path))
    # Assert that the invalid park name is excluded
    assert result[result['Zip Code'] == "60611"].empty

def test_zip_code_formatting(sample_parks_data, tmpdir):
    """Test if ZIP codes are formatted to 5 digits."""
    new_row = pd.DataFrame([{"PARK": "Park D", "PARK_NO":"139", "LOCATION": "Location D", "ZIP": "123", "PARK_CLASS": "COMMUNITY PARK"}])
    sample_parks_data = pd.concat([sample_parks_data, new_row], ignore_index=True)

    # Save the sample data to a CSV
    path = tmpdir.join("sample_parks.csv")
    sample_parks_data.to_csv(path, index=False)
    
    with patch.object(pd.DataFrame, 'to_csv') as mock_to_csv:
        mock_to_csv.return_value = None  # Mock to do nothing when calling to_csv

        # Run the clean_parks_data function (this won't create directories or save files)
        result = clean_parks_data(str(path))

    # Assert ZIP code is 5 digits
    assert result['Zip Code'].apply(lambda x: len(x) == 5).all()


def test_zip_counts(sample_parks_data, tmpdir):
    """Test if the zip_counts DataFrame is generated correctly."""
    # Save the sample data to a CSV
    path = tmpdir.join("sample_parks.csv")
    sample_parks_data.to_csv(path, index=False)
    
    with patch.object(pd.DataFrame, 'to_csv') as mock_to_csv:
        mock_to_csv.return_value = None  # Mock to do nothing when calling to_csv

        # Run the clean_parks_data function (this won't create directories or save files)
        result = clean_parks_data(str(path))
    
    # Assert zip_counts has the correct counts
    assert result.loc[result['Zip Code'] == '60601', 'park_count'].values[0] == 2
    assert result.loc[result['Zip Code'] == '60602', 'park_count'].values[0] == 1
    assert result.loc[result['Zip Code'] == '60603', 'park_count'].values[0] == 1

