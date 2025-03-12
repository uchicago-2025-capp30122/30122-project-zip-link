import pytest
import requests
import pandas as pd
import re
from lxml import html

# URL for the hospital page
URL = "https://cookcountysheriffil.gov/departments/c-c-s-p-d/cemeteries/hospitals-cook-county/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def extract_zip(zip_code):
    """
    Extracts the 5-digit ZIP code from a ZIP string.
    Some ZIP codes may have extensions (e.g., '60616-2477'), so we need to extract only the first 5 digits.
    """
    zip_match = re.match(r"^\d{5}", str(zip_code))
    return zip_match.group() if zip_match else "N/A"

def test_web_scraper_response():
    """
    Tests if the web scraper successfully fetches data from the hospital webpage.
    """
    response = requests.get(URL, headers=HEADERS)
    assert response.status_code == 200, f"Failed to fetch data. Status Code: {response.status_code}"

@pytest.mark.parametrize(
    "zip_code, expected_zip",
    [
        ("60640", "60640"),  # Valid ZIP
        ("60612-2477", "60612"),  # Valid ZIP with extension
        ("60608", "60608"),  # Valid ZIP
        ("60635", "60635"),  # Valid ZIP
        ("", "N/A"),  # Empty ZIP
    ]
)
def test_extract_zip(zip_code, expected_zip):
    """
    Tests if ZIP codes are correctly extracted, especially when they have extensions.
    """
    extracted_zip = extract_zip(zip_code)
    assert extracted_zip == expected_zip, f"Expected {expected_zip}, got {extracted_zip}"

# List of valid Chicago ZIP codes
valid_zip_codes = {
    "60601", "60602", "60603", "60604", "60605", "60606", "60607", "60608",
    "60609", "60610", "60611", "60612", "60613", "60614", "60615", "60616",
    "60617", "60618", "60619", "60620", "60621", "60622", "60623", "60624",
    "60625", "60626", "60628", "60629", "60630", "60631", "60632", "60633",
    "60634", "60635", "60636", "60637", "60638", "60639", "60640", "60641",
    "60642", "60643", "60644", "60645", "60646", "60647", "60649", "60651",
    "60652", "60653", "60654", "60655", "60656", "60657", "60659", "60660",
    "60661"
}

def test_zip_codes_in_valid_range():
    """
    Tests if all extracted ZIP codes belong to valid Chicago ZIP code ranges.
    """
    df = pd.read_csv("data/raw/hospitals/hospitals.csv")  # Change the path if necessary
    zip_codes = df['ZIP Code'].astype(str).apply(extract_zip).tolist()
    
    for zip_code in zip_codes:
        assert zip_code in valid_zip_codes, f"Invalid ZIP code found: {zip_code}"
