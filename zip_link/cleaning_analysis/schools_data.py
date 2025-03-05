import requests
from lxml import html
import csv

def get_school_data(page_url):
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Failed to fetch {page_url}")
        return []
    
    tree = html.fromstring(response.content)
    schools = []
    
    for school in tree.xpath("//div[contains(@class, 'school-result')]"):
        name = school.xpath(".//h3/text()")
        address = school.xpath(".//p[contains(@class, 'address')]/text()")
        phone = school.xpath(".//p[contains(@class, 'phone')]/text()")
        
        schools.append({
            "name": name[0].strip() if name else "",
            "address": address[0].strip() if address else "",
            "phone": phone[0].strip() if phone else ""
        })  
    return schools

def scrape_all_schools(base_url, total_pages):
    all_schools = []
    
    for page in range(1, total_pages + 1):
        url = f"{base_url}&pageNumber={page}"
        print(f"Scraping page {page}")
        all_schools.extend(get_school_data(url))
    return all_schools

# def save_to_csv(data, file_path):
#     keys = ["name", "address", "phone"]
#     with open(file_path, "w", newline="", encoding="utf-8") as file:
#         writer = csv.DictWriter(file, fieldnames=keys)
#         writer.writeheader()
#         writer.writerows(data)

def main():
    base_url = "https://www.cps.edu/search/?pageNumber=1&context=Schools&sortId=a-z"
    total_pages = 65
    schools = scrape_all_schools(base_url, total_pages)
    # file_path = "data/raw/schools.csv"
    # save_to_csv(schools, file_path)
    output_file = "data/raw/schools.csv" 
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "address", "phone"])
        writer.writeheader()
        writer.writerows(schools)

if __name__ == "__main__":
    main()
