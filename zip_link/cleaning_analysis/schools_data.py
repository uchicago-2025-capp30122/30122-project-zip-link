import os
import requests
import json
import time
import pandas as pd

#API link
URL = "https://www.cps.edu/api/v1/search/results"
HEADERS = {"Content-Type": "application/json"}

def fetch_data(page_number):
    """
    Fetching data from the API.
    
    Input: the individual page number
    Output: information in json
    """

    payload = {
        "searchTerm": "",
        "pageSize": 10,
        "pageNumber": page_number,
        "facets": [],
        "context": "Schools",
        "sortField": 1,
        "sortDirection": 1,
        "dateSortRelevanceFilter": 0,
        "contentId": "10375"
    }
    response = requests.post(URL, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def extract_zip(address):
    """
    Extracting the zip code from the address.
    
    Input: an address
    Output: address, zip code
    """
    if not address or "," not in address:
        return "N/A", "N/A"
    
    parts = address.split(",")
    street_address = parts[0].strip()
    rest = parts[-1].strip()

    zip_code = rest.split()[-1] if rest.split()[-1].isdigit() else "N/A"
    return street_address, rest, zip_code

def scrape_api(total_pages=65):
    """
    Iterating through all the pages.
    
    Input: 65 (total nmumber of pages)
    Output: DataFrame with the data
    """
    all_results = []

    for page in range(1, total_pages + 1):
        print(f"Fetching page {page}")
        data = fetch_data(page)

        if data and "results" in data:
            for school in data["results"]:
                title = school.get("title", "N/A")
                full_address = school.get("address", "N/A")
                
                street, rest, zip_code = extract_zip(full_address)

                all_results.append({
                    "School Name": title,
                    "address": street,
                    #"csz": csz,
                    "Zip Code": zip_code
                })
        else:
            print(f"Skipping page {page} due to error or no results.")

        time.sleep(1)
    return pd.DataFrame(all_results)


if __name__ == "__main__":
    df = scrape_api(total_pages=65)

    output_dir = "../data/raw/Schools"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "schools_data.csv")

    #df to CSV
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")
