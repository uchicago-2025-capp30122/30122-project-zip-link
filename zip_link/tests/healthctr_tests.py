import pytest
import pandas as pd
import re
from zip_link.cleaning_analysis.unified_community_health import process_health_data, get_hrsa_data, fuzzy_match  

@pytest.fixture
def health_data():
    """Fixture to provide health data for tests."""
    return pd.DataFrame({
        "Health Center Facility": ["Test Clinic", "Test Clinic 2"],
        "Address": ["123 Main St, Chicago, IL 60601", "789 Oak St, Chicago, IL"],
        "Telephone Number": ["312-555-1234", " "]
    })

@pytest.fixture
def hrsa_data():
    """Fixture to provide HRSA data for tests."""
    return pd.DataFrame({
        "Health Center Name": ["HRSA Clinic"],
        "Operated By": ["ABC CENTER INC"],
        "City": ["Chicago"],
        "State": ["IL"],
        "Street Address": ["123 HRSA St, Chicago, IL 60603"],
        "ZIP Code": ["60603-1234"],
        "Telephone Number": ["312-555- 9876"]
    })

@pytest.mark.parametrize(
    "address, expected_zip",
    [
        ("123 Main St, Chicago, IL 60601", "60601"),
        ("456 Elm St, Chicago, IL 60602", "60602"),
        ("789 Oak St, Chicago, IL", "N/A"),  
    ]
)
def test_extract_zip(address, expected_zip):
    """Tests if ZIP codes are correctly extracted."""
    zip_code = re.search(r"\b\d{5}\b", address)
    zip_code = zip_code.group() if zip_code else "N/A"
    assert zip_code == expected_zip, f"Expected {expected_zip}, got {zip_code}"

@pytest.mark.parametrize(
    "phone, expected_phone",
    [
        ("312-555-1234", "312-555-1234"),
        ("  312-555-5678  ", "312-555-5678"),
        (" ", ""),  
    ]
)
def test_format_phone(phone, expected_phone):
    """Tests if phone numbers are correctly formatted."""
    formatted_phone = re.sub(r'\s+', '', phone) 
    formatted_phone = re.match(r"\d{3}-\d{3}-\d{4}", formatted_phone)
    formatted_phone = formatted_phone.group() if formatted_phone else ""
    assert formatted_phone == expected_phone, f"Expected {expected_phone}, got {formatted_phone}"

# def test_process_health_data(health_data):
#     """Tests the process_health_data function."""
#     health_data.to_csv("test_health_data.csv", index=False)
#     result = process_health_data("test_health_data.csv")
#     assert list(result["Zip Code"]) == ["60601"]  # Should exclude missing ZIP row

def test_process_health_data(health_data, tmpdir):
    """Tests the process_health_data function using a temporary file."""
    path = tmpdir.join("test_health_data.csv")  # Create a temp file path
    health_data.to_csv(path, index=False)  # Save test data to temp file

    # Run the function with the temp file path
    result = process_health_data(str(path))

    # Assert the expected output
    assert list(result["Zip Code"]) == ["60601"]  # Should exclude missing ZIP row


# def test_get_hrsa_data(hrsa_data):
#     """Tests the get_hrsa_data function."""
#     hrsa_data.to_csv("test_hrsa_data.csv", index=False)
#     result = get_hrsa_data("test_hrsa_data.csv")
#     assert list(result["Zip Code"]) == ["60603"]
#     assert list(result["Telephone Number"]) == ["312-555-9876"]

def test_get_hrsa_data(hrsa_data, tmpdir):
    """Tests the get_hrsa_data function using a temporary file."""
    path = tmpdir.join("test_hrsa_data.csv")  # Create a temp file path
    hrsa_data.to_csv(path, index=False)  # Save test data to temp file

    # Run the function with the temp file path
    result = get_hrsa_data(str(path))

    # Assert expected output
    assert list(result["Zip Code"]) == ["60603"]
    assert list(result["Telephone Number"]) == ["312-555-9876"]

def test_fuzzy_match():
    """Tests the fuzzy_match function."""
    df = pd.DataFrame({
        "Health Center Facility": ["ABC Health", "A B C Health"],
        "Address": ["100 Main St", "100 Main Street"],
        "Telephone Number": ["312-555-1111", "312-555-1111"]
    })
    result = fuzzy_match(df, threshold=0.9)
    assert len(result) == 1  # Should merge duplicates
 