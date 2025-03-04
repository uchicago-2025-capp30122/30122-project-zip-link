import os
import requests
from lxml import html
import pandas as pd

# URL of the webpage to scrape
url = "https://cookcountysheriffil.gov/departments/c-c-s-p-d/cemeteries/hospitals-cook-county/"

# Headers to mimic a real browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Request the webpage with headers
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content with lxml
    tree = html.fromstring(response.content)
    
    # Find all hospitals listed under Chicago
    chicago_hospitals = []
    
    # Extract hospital names and ZIP codes from <td> elements
    for entry in tree.xpath("//td"):  # Adjusted to extract from table cells
        text = entry.text_content().strip()
        lines = text.split("\n")
        
        if "Chicago, Illinois" in text:
            name = lines[0].strip()
            zip_code = lines[2].split(" ")[-1]  # Extract ZIP code from "Chicago, Illinois 606XX"
            chicago_hospitals.append((name, zip_code))
    
    # Convert to DataFrame
    df = pd.DataFrame(chicago_hospitals, columns=["Hospital Name", "ZIP Code"])
    
    # Print extracted data for verification
    print(df.head())
    
    # Define output path and ensure directory exists
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "hospitals.csv")
    df.to_csv(output_file, index=False)
    
    print(f"Data saved to {output_file}")
    
else:
    print(f"Failed to retrieve the webpage. Status Code: {response.status_code}")
