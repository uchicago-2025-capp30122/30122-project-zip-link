# Zip & Link

# Team Members: Vyshnavi Voleti, Nelu Wijegunasekera, Pragya Khanal

## Overview
Zip & Link analyzes the relationship between essential services and housing affordability across neighborhoods in Chicago. The project explores how accessibility to key services—such as healthcare, public education, public transport, grocery stores, and parks—affects median property prices and other economic indicators. The project involves web scraping, bulk data downloads, data cleaning and preprocessing, and an analysis framework to generate an Accessibility Index for each ZIP code. This index is meant to help users understand the impact of essential services on housing affordability and highlight areas that require better urban planning. Our initial hypothesis was that the housing prices were positively correlated with the Accessibility Index and in order to test and better visualize this, we developed 3 key visualizations on Dash: a choropleth map, a scatterplot and horizontal bar plots that help compare 2 specific zip codes. Interestingly, we found that the converse of our hypothesis was true. 

## Demonstration of Project

< Insert Link>

## How to Run

1. Clone the repo to this project using the url on GitHub
2. In the root directory, run uv sync to install all the necessary packages used for this project
3. Run uv run python -m cleaning_analysis.zipatlas_data to scrape all the data, clean and preprocess data and obtain final dataset with zip code, housing prices and other economic indicators, essential services count and the Accessibility Index
4. Next, run uv run python -m visualization.merge_visualization to get the Dash app running on http://127.0.0.1:8057 
5. Select different variables, explore how the distribution across Chicago changes on the map, see how the variables is related to the Accessibility Index on the scatterplot, and even compare 2 different zip codes!
7. To ensure all our data is running correctly, run our tests uv run python tests/___.py

## Data Citations 

### Housing Data
<<<<<<< HEAD

ZipAtlas.com. “Highest Median Property Prices in Chicago by Zip Code in 2025 | Zip Atlas.” Zipatlas.com, Zipatlas.com, 2025, [zipatlas.com/us/il/chicago/zip-code-comparison/highest-property-prices.htm](https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-property-prices.htm). Accessed 12 Mar. 2025.

### Healthcare Data

#### Community Health Centers
City of Chicago Health Facilities:
chicago.gov. https://www.chicago.gov/content/dam/city/depts/cdph/policy_planning/PP_Web%20Health%20Care%20Facilities%20by%20Zip%20Code.pdf. Accessed 12 Mar. 2025. 
 
HRSA Find a Health Center: 
Hrsa.gov. “Find a Health Center.” Hrsa.gov, Hrsa.gov, 2025, [findahealthcenter.hrsa.gov/?zip=Chicago%252C%2BIL%252C%2BUSA&radius=5&incrementalsearch=true](https://findahealthcenter.hrsa.gov/?zip=Chicago%252C%2BIL%252C%2BUSA&radius=5&incrementalsearch=true). Accessed 12 Mar. 2025. 

#### Hospitals
Cook County Sheriff's Office. “Hospitals in Cook County.” Cook County Sheriff’s Office, Cook County Sheriff’s Office, Aug. 2017, [cookcountysheriffil.gov/departments/c-c-s-p-d/cemeteries/hospitals-cook-county/](https://cookcountysheriffil.gov/departments/c-c-s-p-d/cemeteries/hospitals-cook-county/). Accessed 12 Mar. 2025. 

### Transportation Data
Institute of Social Research, University of Michigan. “National Neighborhood Data Archive (NaNDA): Public Transit Stops by Census Tract and ZIP Code Tabulation Area, United States, 2016-2018 and 2024 | ICPSR.” Umich.edu, Umich.edu, 2016, [archive.icpsr.umich.edu/view/studies/38605/data-documentation](https://archive.icpsr.umich.edu/view/studies/38605/data-documentation). Accessed 12 Mar. 2025.


### Grocery Stores Data
City of Chicago. “Grocery Store Status Map | City of Chicago | Data Portal.” Data.cityofchicago.org, Cityofchicago, [data.cityofchicago.org/Health-Human-Services/Grocery-Store-Status-Map/rish-pa6g.](https://data.cityofchicago.org/Health-Human-Services/Grocery-Store-Status-Map/rish-pa6g)

### Parks & Green Spaces
City of Chicago. “Parks - Chicago Park District Park Boundaries (Current) | City of Chicago | Data Portal.” Cityofchicago.org, Cityofchicago, 2018, [data.cityofchicago.org/Parks-Recreation/Parks-Chicago-Park-District-Park-Boundaries-curren/ej32-qgdr.](https://data.cityofchicago.org/Parks-Recreation/Parks-Chicago-Park-District-Park-Boundaries-curren/ej32-qgdr)

### Education Data (Schools)
=======
- Source: [ZipAtlas](https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-property-prices.htm)
- Method: Web Scraping using lxml.html
- Key Data Points: Median Housing Prices, Owner & Renter Housing Costs, Housing Costs/Income Ratio, Unemployment Rates, Poverty Levels.
- Challenges: Only 54 ZIP codes have property price data. Missing data for some variables in certain ZIP codes.
- Rows: 54
- Citation: ZipAtlas.com. “Highest Median Property Prices in Chicago by Zip Code in 2025 | Zip Atlas.” Zipatlas.com, Zipatlas.com, 2025, zipatlas.com/us/il/chicago/zip-code-comparison/highest-property-prices.htm. Accessed 12 Mar. 2025.

### Healthcare Data
#### 1. Hospitals
- Source: [US News Best Hospitals](https://health.usnews.com/best-hospitals/area/chicago-il)
- Method: Web Scraping using lxml.html
- Key Data Points: ZIP Code & Number of Hospitals.
- Challenges: The dataset includes hospitals outside Chicago, requiring filtering.
- Rows: 117 records included for Chicago, 100 records expected to be used.
- Citation:usnews.com. “Best Hospitals in Chicago, IL Rankings | US News Best Hospitals.” Usnews.com, usnews.com, 2020, health.usnews.com/best-hospitals/area/chicago-il.

#### 2. Community Health Centers
- Sources: 
  - [City of Chicago Health Facilities](https://www.chicago.gov/content/dam/city/depts/cdph/policy_planning/PP_Web%20Health%20Care%20Facilities%20by%20Zip%20Code.pdf)
  - [HRSA Find a Health Center](https://findahealthcenter.hrsa.gov/?zip=Chicago%252C%2BIL%252C%2BUSA&radius=5&incrementalsearch=true)
- Method: Web Scraping & Data Cleaning
- Challenges: Requires data deduplication due to multiple sources.
- Rows: 373, but will require cleaning as some health centers are in Indiana and Wisconsin.
- Citation: chicago.gov. www.chicago.gov/content/dam/city/depts/cdph/policy_planning/PP_Web%20Health%20Care%20Facilities%20by%20Zip%20Code.pdf. Accessed 12 Mar. 2025.

### Transportation Data
- Source: [Institute of Social Research, University of Michigan](https://archive.icpsr.umich.edu/view/studies/38605/data-documentation)
- Method: Bulk Data Download
- Key Data Points: Total Population, Public Transit Stops per Capita, Stops per Square Mile.
- Challenges: Some ZIP codes lack transit data, requiring preprocessing.
- Rows: 56 Chicago ZIP Codes
- Citation: Institute of Social Research, University of Michigan. “National Neighborhood Data Archive (NaNDA): Public Transit Stops by Census Tract and ZIP Code Tabulation Area, United States, 2016-2018 and 2024 | ICPSR.” Umich.edu, Umich.edu, 2016, archive.icpsr.umich.edu/view/studies/38605/data-documentation. Accessed 12 Mar. 2025.

### Grocery Stores Data
- Source: [City of Chicago Open Data](https://data.cityofchicago.org/Health-Human-Services/Grocery-Store-Status-Map/rish-pa6g)
- Method: Bulk CSV Download
- Key Data Points: ZIP Code & Store Names.
- Challenges: Last updated in 2020, requiring assumptions about store continuity.
- Rows: 264
- Citation: City of Chicago. “Grocery Store Status Map | City of Chicago | Data Portal.” Data.cityofchicago.org, Cityofchicago, data.cityofchicago.org/Health-Human-Services/Grocery-Store-Status-Map/rish-pa6g.

### Parks & Green Spaces
- Source: [Chicago Park District Open Data](https://data.cityofchicago.org/Parks-Recreation/Parks-Chicago-Park-District-Park-Boundaries-curren/ej32-qgdr)
- Method: Bulk CSV Download
- Key Data Points: ZIP Code & Park Name.
- Challenges: None, as this dataset is well-maintained.
- Rows: 617
- Citation: City of Chicago. “Parks - Chicago Park District Park Boundaries (Current) | City of Chicago | Data Portal.” Cityofchicago.org, Cityofchicago, 2018, data.cityofchicago.org/Parks-Recreation/Parks-Chicago-Park-District-Park-Boundaries-curren/ej32-qgdr.

### Education Data (Schools)
- Sources:[Public Schools](https://www.cps.edu/search/?pageNumber=1&context=Schools&sortId=a-z)
- Method: Scrsping from an API
- Key Data Points: ZIP Code & Number of Schools.
- Challenges: Extracting ZIP codes from addresses, scraping multiple pages.
- Rows: 
  - Public Schools: 649 records.
- Citation: Chicago Public Schools. “Search | Chicago Public Schools.” Cps.edu, CPS, 2025, www.cps.edu/search/?pageNumber=1&context=Schools&sortId=a-z. Accessed 12 Mar. 2025.
>>>>>>> b168bca43d4bb3013fc19c262c383d8df4c6aaf8

Chicago Public Schools. “Search | Chicago Public Schools.” Cps.edu, CPS, 2025, [www.cps.edu/search/?pageNumber=1&context=Schools&sortId=a-z](https://www.cps.edu/search/?pageNumber=1&context=Schools&sortId=a-z). Accessed 12 Mar. 2025.

## Data Integration
All datasets are linked by ZIP code. 


Thank you so much to James Turk, our CAPP 122 lecturer, for making this journey so fruitful and supporting us as we set out on this project. Hope you enjoy interacting with this visualization!

<<<<<<< HEAD
=======
- Web Scraping (lxml.html): Used for scraping ZipAtlas, US News, Niche, and HRSA.
- Bulk Data Download: Used for Public Transit, Grocery Stores, Parks.
- Regex Extraction: Used to extract ZIP codes from addresses.

2. Data Cleaning
- Handling missing values.
- Removing duplicate records (e.g., community health centers).
- Filtering out-of-area data (e.g., hospitals outside Chicago).
- Standardizing ZIP code formats.

3. Accessibility Index Calculation
The Accessibility Index quantifies service availability by ZIP code. It considers the density of essential services:

Index = (Total Essential Services Count) / (ZIP Code Population)

Where:
- Total Essential Services Count includes hospitals, health centers, grocery stores, public transit stops, schools, and parks.
- ZIP Code Population represents the number of residents in a given ZIP code.


## Correlation with Housing Prices
- A statistical model will be developed to analyze the relationship between property prices and accessibility.
- A user interface will allow users to compare neighborhoods based on housing affordability and service accessibility.


## Visualization
We have added code for the visualization and generated a map of Chicago ZIP codes using demo data. Planned improvements:
1. Adding ZIP codes as labels to the map.
2. Adding more details on hover (e.g., service counts, housing prices).
3. Changing colors to reflect a gradient for better readability.

# Running the project:
1. uv run python -m visualization.merge_visualization
>>>>>>> b168bca43d4bb3013fc19c262c383d8df4c6aaf8
