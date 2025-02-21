import requests
import lxml.html as lh
import pandas as pd
import re
from collections import defaultdict

def scrape_hospitals(url, output_csv):
    """
    Scrapes hospital data across multiple pages, extracts names and ZIP codes,
    filters for hospitals in Chicago (without predefined ZIP codes), and saves the data.

    Inputs:
    - url: The base URL of the hospitals page.
    - output_csv: The name of the output CSV file.
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    hospital_data = defaultdict(int)  # Dictionary to count hospitals per ZIP code

    page_num = 1  # Start with page 1

    while True:
        response = requests.get(f"{url}?page={page_num}", headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch {url}?page={page_num}, status code: {response.status_code}")
            break

        root = lh.fromstring(response.text)
        hospitals = root.xpath("//div[contains(@class, 'hospital-info')]")

        if not hospitals:
            print(f"No more hospitals found. Finished scraping {page_num - 1} pages.")
            break  # Stop if no hospitals are found (end of pagination)

        for hospital in hospitals:
            try:
                # Extract hospital name
                name_element = hospital.xpath(".//h3")
                name = name_element[0].text_content().strip() if name_element else "Unknown Hospital"

                # Extract hospital address
                address_element = hospital.xpath(".//span[contains(@class, 'address')]")
                address = address_element[0].text_content().strip() if address_element else "Unknown Address"

                # Check if the hospital is in Chicago
                if "Chicago, IL" in address:
                    # Extract ZIP code using regex
                    zip_match = re.search(r"\b\d{5}\b", address)
                    zip_code = zip_match.group() if zip_match else "Unknown"

                    # Count hospitals per ZIP code
                    if zip_code != "Unknown":
                        hospital_data[zip_code] += 1

            except Exception as e:
                print(f"Error extracting hospital info on page {page_num}: {e}")

        print(f"Scraped page {page_num} successfully.")
        page_num += 1  # Move to the next page

    # Convert to DataFrame
    df = pd.DataFrame(list(hospital_data.items()), columns=["Zip Code", "Number of Hospitals"])

    # Save to CSV
    df.to_csv(output_csv, index=False)
    print(f"Data successfully saved to '{output_csv}'.")

# Scrape hospitals from the given U.S. News URL
hospital_url = "https://health.usnews.com/best-hospitals/area/chicago-il"
output_file = "chicago_hospitals.csv"
scrape_hospitals(hospital_url, output_file)

# Load and display the data
df_hospitals = pd.read_csv(output_file)

import ace_tools as tools
tools.display_dataframe_to_user(name="Chicago Hospital Data", dataframe=df_hospitals)
