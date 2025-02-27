import csv
#import requests
import lxml.html
import httpx
import re

def make_request(url):
    """
    Fetches the content of a webpage and returns the response.
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    print(f"Making request to: {url}")  # Debugging 
    try:
        response = httpx.get(url)#, headers=headers)
    except Exception as err:
        print(err)
        return
    print(response)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")  # Debugging 

    response.raise_for_status()  # Stop if request fails
    return response

def scrape_hospitals(url):
    """
    Scrapes all hospital names and ZIP codes from the U.S. News Chicago hospitals listing page.

    Parameters:
        * url: The URL of the hospital listing page.

    Returns:
        * A list of dictionaries, each containing:
            - name: The hospital's name
            - zip_code: The 5-digit ZIP code of the hospital
    """
    hospitals = []

    # Fetch the webpage
    response = make_request(url)
    tree = lxml.html.fromstring(response.content)

    # Extract hospital names
    name_xpath = "//h2[@class='Heading-sc-1w5xk2o-0 hvUhyf']/a/text()"
    names = tree.xpath(name_xpath)

    # Extract addresses (for ZIP code extraction)
    zip_xpath = "//p[@class='Paragraph-sc-1iyax29-0 hvIgej']/text()"
    addresses = tree.xpath(zip_xpath)

    # Extract only the 5-digit ZIP codes
    zip_codes = []
    for address in addresses:
        match = re.search(r"\b\d{5}\b", address)  # regex to capture the first 5-digit ZIP code
        zip_code = match.group(0) if match else "Unknown ZIP"
        zip_codes.append(zip_code)

    # Combine names & ZIP codes into a list of dictionaries
    for i in range(min(len(names), len(zip_codes))):  # Ensure both lists are aligned
        hospitals.append({
            "name": names[i].strip(),
            "zip_code": zip_codes[i]
        })

    return hospitals

if __name__ == "__main__":
    """
    Runs the hospital scraper.
    Saves the results as a CSV file in data/raw/hospitals.csv.
    """
    start_url = "https://health.usnews.com/best-hospitals/area/chicago-il"
    # Define output file path
    output_file = "data/raw/hospitals.csv"  

    print(f"Scraping page: {start_url}") 

    # Scrape hospitals from the listing page
    hospitals_data = scrape_hospitals(start_url)

   
    # Save data to CSV file
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[" Hospital Name", "Zip Code"])
        writer.writeheader()
        writer.writerows(hospitals_data)

    print(f"Scraping complete! Data saved to '{output_file}'.")
