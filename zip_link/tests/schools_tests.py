
import pytest
import pandas as pd
import re
from zip_link.cleaning_analysis.schools_data import extract_zip


@pytest.mark.parametrize(
    "address, expected_zip",
    [
        ("615 W Kemper Pl, Chicago, IL 60614", "60614"),  #valid ZIP
        ("24 W Walton St, Chicago, IL 60610", "60610"),   #valid ZIP
        ("700 S State St, Chicago, IL 60605", "60605"),   #valid ZIP
        ("100 Main St, Springfield, IL 62701", "62701"),  #valid ZIP
        ("500 E Randolph St, Chicago, IL 60601", "60601"),#valid ZIP
        ("400 W Diversey Pkwy, Chicago, IL", "N/A"),      #missing ZIP
    ]
)
def test_extract_zip(address, expected_zip):
    """Tests if extract_zip correctly extracts a 5-digit ZIP code."""
    _, _, zip_code = extract_zip(address)
    
    if zip_code != "N/A":
        assert re.match(r'^\d{5}$', zip_code), f"Assertion failed: Expected a 5-digit ZIP code, but got '{zip_code}'"
    
    assert zip_code == expected_zip, f"Expected {expected_zip}, got {zip_code}"


#list of valid ZIP codes
valid_zip_codes = {
    "60601", "60602", "60603", "60604", "60605", "60606", "60607", "60608", 
    "60609", "60610", "60611", "60612", "60613", "60614", "60615", "60616", 
    "60617", "60618", "60619", "60620", "60621", "60622", "60623", "60624", 
    "60625", "60626", "60628", "60629", "60630", "60631", "60632", "60633", 
    "60634", "60636", "60637", "60638", "60639", "60640", "60641", "60642", 
    "60643", "60644", "60645", "60646", "60647", "60649", "60651", "60652", 
    "60653", "60654", "60655", "60656", "60657", "60659", "60660", "60661", 
    "60664", "60666", "60668", "60669", "60670", "60673", "60674", "60675", 
    "60677", "60678", "60680", "60681", "60682", "60684", "60685", "60686", 
    "60687", "60688", "60689", "60690", "60691", "60693", "60694", "60695", 
    "60696", "60697", "60699", "60701", "60707", "60827"
}

#validity of zip codes
def test_zip_codes_in_valid_range():
    df = pd.read_csv("../data/raw/Schools/schools_data.csv")
    zip_codes = df['Zip Code'].astype(str).tolist()
    
    # Assert that every zip code is in the valid_zip_codes list
    for zip_code in zip_codes:
        assert zip_code in valid_zip_codes, f"Invalid zip code found: {zip_code}"
