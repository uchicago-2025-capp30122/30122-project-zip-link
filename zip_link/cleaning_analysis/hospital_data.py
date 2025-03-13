import os
import requests
from lxml import html
import pandas as pd

# URL of the webpage to scrape
url = "https://cookcountysheriffil.gov/departments/c-c-s-p-d/cemeteries/hospitals-cook-county/"

# Headers for a real browser request
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Request the webpage with headers
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content with lxml
    tree = html.fromstring(response.content)
    
    # Find all hospitals listed under Chicago
    chicago_hospitals = []
    
    # Extract hospital names and ZIP codes 
    for entry in tree.xpath("//td"):  
        text = entry.text_content().strip()
        lines = text.split("\n")
        
        if "Chicago, Illinois" in text:
            name = lines[0].strip()
            zip_code = lines[2].split(" ")[-1]  # Extract ZIP"
            chicago_hospitals.append((name, zip_code))
    
    # Convert to DataFrame
    df = pd.DataFrame(chicago_hospitals, columns=["Hospital Name", "ZIP Code"])
     
    # Define output path and ensure directory exists
    output_dir = "data/raw/Hospitals"
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "hospitals.csv")
    df.to_csv(output_file, index=False)
    


          

