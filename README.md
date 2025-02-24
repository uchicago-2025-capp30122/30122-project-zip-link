# Project Repository Template

This template is intentionally mostly empty, to give you experience starting a project from scratch.

A good first command would be to run `uv init` and add some libraries and tools that you are using.

Before the final milestone submission, you will need to replace this file with a README as described here: https://capp30122.netlify.app/coursework/project/#readmemd


### Zip & Link
## Overview
Zip & Link analyzes the relationship between essential services and housing affordability across neighborhoods in Chicago. The project explores how accessibility to key services—such as healthcare, education, public transport, grocery stores, and parks—affects median property prices. The project involves web scraping, data cleaning, and an analysis framework to generate an Accessibility Index for each ZIP code. This index will help users understand the impact of essential services on housing affordability and highlight areas that require better urban planning.

## Data Collection
Our project integrates multiple data sources, each providing ZIP code-based insights into key services and housing prices:

# Housing Data
* Source: ZipAtlas (https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-property-prices.htm )
* Method: Web Scraping using lxml.html
* Key Data Points: Median Housing Prices, Owner & Renter Housing Costs, Housing Costs/Income Ratio, Unemployment Rates, Poverty Levels.
* Challenges: Only 54 ZIP codes have property price data. Missing data for some variables in certain ZIP codes.
* Rows: 54

# Healthcare Data
* Source 1 (Hospitals): US News Best Hospitals (https://health.usnews.com/best-hospitals/area/chicago-il )
* Method: Web Scraping using lxml.html
* Key Data Points: ZIP Code & Number of Hospitals.
* Challenges: The dataset includes hospitals outside Chicago, requiring filtering.
* Rows: There are 117 records included for the Chicago area with the zip code indicated, from which we expect to use around 100 records for the project.

* Source 2 (Community Health Centers):City of Chicago Health Facilities, HRSA Find a Health Center (https://www.chicago.gov/content/dam/city/depts/cdph/policy_planning/PP_Web%20Health%20Care%20Facilities%20by%20Zip%20Code.pdf
https://findahealthcenter.hrsa.gov/?zip=Chicago%252C%2BIL%252C%2BUSA&radius=5&incrementalsearch=true)
* Method: Web Scraping & Data Cleaning
* Challenges: Requires data deduplication as there are multiple sources.
* Rows: There are currently 373 rows of data, but we anticipate some time used to clean this data set as it has health care centers from Indiana and Wisconsin.

# Transportation Data
* Source: Institute of Social Research, University of Michigan  (https://archive.icpsr.umich.edu/view/studies/38605/data-documentation)
* Method: Bulk Data Download
* Key Data Points: Total Population, Public Transit Stops per Capita, Stops per Square Mile.
* Challenges: Some ZIP codes are missing transit data, requiring preprocessing.
* Rows: 56 Chicago Zip Codes

# Grocery Stores Data
* Source: City of Chicago Open Data (https://data.cityofchicago.org/Health-Human-Services/Grocery-Store-Status-Map/rish-pa6g)
* Method: Bulk CSV Download
* Key Data Points: ZIP Code & Store Names.
* Challenges: Last updated in 2020, requiring assumptions about store continuity.
* Rows: 264

# Parks & Green Spaces
* Source: Chicago Park District Open Data (https://data.cityofchicago.org/Parks-Recreation/Parks-Chicago-Park-District-Park-Boundaries-curren/ej32-qgdr )
* Method: Bulk CSV Download
* Key Data Points: ZIP Code & Park Name.
* Challenges: None, as this dataset is well-maintained.
* Rows: There are 617 rows of data.

# Education Data (Schools)
* Source: Public Schools, Private Schools (https://www.niche.com/k12/search/best-private-schools/t/chicago-cook-il/
and https://www.niche.com/k12/search/best-private-schools/t/chicago-cook-il/)
* Method: Web Scraping using lxml.html
* Key Data Points: ZIP Code & Number of Schools.
* Challenges: Extracting ZIP codes from full addresses. Scraping multiple pages systematically.
* Rows: Public Schools - There are 729 rows of data on the Niche website that include traditional, charter and magnet schools for public schools. 
Private Schools - There are 764 rows of data in the Niche website. These will be scraped and added to the data set.

## Data Integration
All datasets are linked by ZIP code. Missing ZIP codes are dropped or supplemented with alternate sources. The final dataset will be preprocessed and cleaned before analysis.

## Methodology
1. Web Scraping & Data Collection
Each data source is processed using different methods:

Web Scraping (lxml.html): Used for scraping ZipAtlas, US News, Niche, and HRSA.
Bulk Data Download: Used for Public Transit, Grocery Stores, Parks.
Regex Extraction: Used to extract ZIP codes from addresses.

2. Data Cleaning
Handling missing values.
Removing duplicate records (e.g., community health centers).
Filtering out-of-area data (e.g., hospitals outside Chicago).
Standardizing ZIP code formats.

3. Accessibility Index Calculation
The Accessibility Index quantifies service availability by ZIP code.
It considers the density of essential services:
he **Accessibility Index** quantifies service availability by ZIP code. It considers the **density of essential services** in a given area:

\[
\text{Index} = \frac{\sum{\text{Essential Services Count}}}{\text{ZIP Code Population}}
\]

Where:
- **Essential Services Count** includes hospitals, health centers, grocery stores, public transit stops, schools, and parks.
- **ZIP Code Population** is the total number of residents in that ZIP code.
​ 
# Correlation with Housing Prices
* A statistical model will be developed to analyze the relationship between property prices and accessibility.
* A user interface will be developed to allow users to compare neighborhoods based on housing affordability and service accessibility.

## Visualization
We have added code for the visualizaton and have generated a map on the zip codes of Chicago using demo data. We have a few improvements that we wanted to make for the final presentation. Including:

1. adding the zip code as a label to the map
2. adding more points of information as we hover over the zip code areas
3. change colour to reflect a gradient
 