import os
import requests
from lxml import html
import pandas as pd

# URL of the webpage to scrape
url = "https://www.illinois-demographics.com/zip_codes_by_population"

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
    
    # List to store ZIP code and population data
    zip_population_data = []
    
    # Extract ZIP codes and population from table rows
    for row in tree.xpath("//table[contains(@class, 'datatable')]/tbody/tr"):
        zip_code_element = row.xpath("td[1]/a/text()")  # Extract ZIP code from <a> tag inside <td>
        population_element = row.xpath("td[2]/text()")  # Extract population from the second <td>
        
        if zip_code_element and population_element:
            zip_code = zip_code_element[0].strip()
            population = population_element[0].strip().replace(',', '')  # Remove commas from population
            zip_population_data.append((zip_code, population))
    
    # Convert extracted data to a DataFrame
    df = pd.DataFrame(zip_population_data, columns=["Zip Code", "Population"])
    
    # Print the first few rows of extracted data for verification
    print(df.head())
    
    # Define output path and ensure directory exists
    output_dir = "../data/raw"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save extracted data to CSV file
    output_file = os.path.join(output_dir, "zip_population.csv")
    df.to_csv(output_file, index=False)
    
    print(f"Data saved to {output_file}")
    
else:
    print(f"Failed to retrieve the webpage. Status Code: {response.status_code}")
