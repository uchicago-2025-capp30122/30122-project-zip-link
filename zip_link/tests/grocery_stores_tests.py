import pytest
import pandas as pd
from unittest.mock import patch
from zip_link.cleaning_analysis.bulk_data_processing import clean_grocery_data  

@pytest.fixture
def sample_grocery_data():
    """Fixture to provide sample grocery data for tests."""
    data = {
        "Store Name": ["Store A", "Store B", "Store C", "Store D", "Store E"],
        "Address": ["Address A", "Address B", "Address C", "Address D", "Address E"],
        "Zip": ["123", "456", "60647", "60611", "60621"],
        "New status": ["OPEN", "CLOSED", "OPEN", "OPEN", "CLOSED"]
    }
    return pd.DataFrame(data)

def test_filter_open_stores(sample_grocery_data, tmpdir):
    """Test if only stores with 'OPEN' status are retained."""
    # Save the sample data to a CSV
    path = tmpdir.join("sample_grocery.csv")
    sample_grocery_data.to_csv(path, index=False)

    with patch.object(pd.DataFrame, 'to_csv') as mock_to_csv:
        mock_to_csv.return_value = None  # Mock to do nothing when calling to_csv

        # Run the clean_grocery_data function
        result = clean_grocery_data(str(path))

    # Assert that only 'OPEN' stores remain
    assert result.shape[0] == 3  # There should be 3 open stores after filtering

def test_zip_code_formatting(sample_grocery_data, tmpdir):
    """Test if ZIP codes are formatted to 5 digits."""
    # Save the sample data to a CSV
    path = tmpdir.join("sample_grocery.csv")
    sample_grocery_data.to_csv(path, index=False)

    with patch.object(pd.DataFrame, 'to_csv') as mock_to_csv:
        mock_to_csv.return_value = None  # Mock to do nothing when calling to_csv

        # Run the clean_grocery_data function
        result = clean_grocery_data(str(path))

    # Assert ZIP code is 5 digits
    assert result['Zip Code'].apply(lambda x: len(x) == 5).all()

def test_drop_duplicates(sample_grocery_data, tmpdir):
    """Test if duplicate stores are removed."""
    # Add a duplicate row to the data
    new_row = pd.DataFrame([{
    "Store Name": "Store C",
    "Address": "Address C",
    "Zip": "60647",
    "New status": "OPEN"
    }])
    
    sample_grocery_data = pd.concat([sample_grocery_data, new_row], ignore_index=True)

    # Save the sample data to a CSV
    path = tmpdir.join("sample_grocery.csv")
    sample_grocery_data.to_csv(path, index=False)

    with patch.object(pd.DataFrame, 'to_csv') as mock_to_csv:
        mock_to_csv.return_value = None  # Mock to do nothing when calling to_csv

        # Run the clean_grocery_data function
        result = clean_grocery_data(str(path))

    # Assert there are no duplicate stores
    assert result.loc[result['Zip Code'] == '60647', 'grocery_store_count'].values[0] == 1

