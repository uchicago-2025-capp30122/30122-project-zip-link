import requests
import lxml.html as lh
import pandas as pd
import re
import os

def scrape_hospitals(url, output_csv_path):
    """
    Scrapes hospital names and ZIP codes from the given URL and saves them as a CSV file.

    Inputs:
    - url: The webpage URL to scrape.
    - output_csv_path: The full path of the output CSV file.
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("[INFO] Successfully fetched the webpage.")
        root = lh.fromstring(response.text)
        
        # Extract hospital names
        hospital_names = root.xpath('//h3[@class="heading-large"]/text()')
        print(f"[DEBUG] Found {len(hospital_names)} hospital names.")

        # Extract hospital addresses (which contain ZIP codes)
        addresses = root.xpath('//div[@class="text-strong text-small"]/text()')
        print(f"[DEBUG] Found {len(addresses)} addresses.")

        # Extract ZIP codes using regex
        zip_codes = [re.search(r'\b\d{5}\b', addr).group() if re.search(r'\b\d{5}\b', addr) else 'N/A' for addr in addresses]

        # Create DataFrame
        df = pd.DataFrame({'Hospital Name': hospital_names, 'Zip Code': zip_codes})

        if df.empty:
            print("[ERROR] No data extracted. The structure of the webpage may have changed.")
            return

        # Ensure the directory exists before saving the file
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

        # Save to CSV
        df.to_csv(output_csv_path, index=False)
        print(f"[INFO] Data successfully saved to '{output_csv_path}'.")
    else:
        print(f"[ERROR] Failed to fetch {url}, status code: {response.status_code}")

# Define parameters
url = "https://health.usnews.com/best-hospitals/area/chicago-il"
output_csv_path = "../data/raw/zipatlas_data/Chicago_hospital.csv"

# Run the scraper
scrape_hospitals(url, output_csv_path)
