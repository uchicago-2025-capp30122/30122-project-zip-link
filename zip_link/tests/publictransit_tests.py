import pytest
import pandas as pd
from unittest.mock import patch
from zip_link.cleaning_analysis.bulk_data_processing import clean_publictransit_data

@pytest.fixture
def sample_publictransit_data():
    """Fixture to provide sample public transit data for tests."""
    data = {
        "ZCTA20": ["60601", "60602", "60603", "70123", "60604", "123"],
        "COUNT_NTM_STOPS": [10, 15, 20, 5, 25, 50],
    }
    return pd.DataFrame(data)

def test_606_zip_codes(sample_publictransit_data, tmpdir):
    """Test if only ZIP codes starting with '606' are included."""
    # Save the sample data to a CSV
    path = tmpdir.join("sample_publictransit.csv")
    sample_publictransit_data.to_csv(path, index=False)

    with patch.object(pd.DataFrame, 'to_csv') as mock_to_csv:
        mock_to_csv.return_value = None  # Mock to do nothing when calling to_csv
        result = clean_publictransit_data(str(path))
    
    # Assert that only ZIP codes starting with '606' are included
    assert result['Zip Code'].str.startswith('606').all()


def test_column_selection_and_renaming(sample_publictransit_data, tmpdir):
    """Test if the correct columns are selected and renamed properly."""
    # Save the sample data to a CSV
    path = tmpdir.join("sample_publictransit.csv")
    sample_publictransit_data.to_csv(path, index=False)
    
    with patch.object(pd.DataFrame, 'to_csv') as mock_to_csv:
        mock_to_csv.return_value = None  # Mock to do nothing when calling to_csv
        result = clean_publictransit_data(str(path))
    
    # Assert columns are renamed correctly
    assert list(result.columns) == ['Zip Code', 'num_public_transit_stops']

def test_zip_code_formatting(sample_publictransit_data, tmpdir):
    """Test if ZIP codes are formatted to 5 digits."""
    # Save the sample data to a CSV
    path = tmpdir.join("sample_grocery.csv")
    sample_publictransit_data.to_csv(path, index=False)

    with patch.object(pd.DataFrame, 'to_csv') as mock_to_csv:
        mock_to_csv.return_value = None  # Mock to do nothing when calling to_csv
        result = clean_publictransit_data(str(path))

    # Assert ZIP code is 5 digits
    assert result['Zip Code'].apply(lambda x: len(x) == 5).all()



