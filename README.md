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

#### 1. Housing Data

ZipAtlas.com. “Highest Median Property Prices in Chicago by Zip Code in 2025 | Zip Atlas.” Zipatlas.com, Zipatlas.com, 2025, [zipatlas.com/us/il/chicago/zip-code-comparison/highest-property-prices.htm](https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-property-prices.htm). Accessed 12 Mar. 2025.

#### 2. Healthcare Data

#### Community Health Centers
City of Chicago Health Facilities:
chicago.gov. https://www.chicago.gov/content/dam/city/depts/cdph/policy_planning/PP_Web%20Health%20Care%20Facilities%20by%20Zip%20Code.pdf. Accessed 12 Mar. 2025. 
 
HRSA Find a Health Center: 
Hrsa.gov. “Find a Health Center.” Hrsa.gov, Hrsa.gov, 2025, [findahealthcenter.hrsa.gov/?zip=Chicago%252C%2BIL%252C%2BUSA&radius=5&incrementalsearch=true](https://findahealthcenter.hrsa.gov/?zip=Chicago%252C%2BIL%252C%2BUSA&radius=5&incrementalsearch=true). Accessed 12 Mar. 2025. 

#### 3. Hospitals
Cook County Sheriff's Office. “Hospitals in Cook County.” Cook County Sheriff’s Office, Cook County Sheriff’s Office, Aug. 2017, [cookcountysheriffil.gov/departments/c-c-s-p-d/cemeteries/hospitals-cook-county/](https://cookcountysheriffil.gov/departments/c-c-s-p-d/cemeteries/hospitals-cook-county/). Accessed 12 Mar. 2025. 

#### 4. Transportation Data
Institute of Social Research, University of Michigan. “National Neighborhood Data Archive (NaNDA): Public Transit Stops by Census Tract and ZIP Code Tabulation Area, United States, 2016-2018 and 2024 | ICPSR.” Umich.edu, Umich.edu, 2016, [archive.icpsr.umich.edu/view/studies/38605/data-documentation](https://archive.icpsr.umich.edu/view/studies/38605/data-documentation). Accessed 12 Mar. 2025.


#### 5. Grocery Stores Data
City of Chicago. “Grocery Store Status Map | City of Chicago | Data Portal.” Data.cityofchicago.org, Cityofchicago, [data.cityofchicago.org/Health-Human-Services/Grocery-Store-Status-Map/rish-pa6g.](https://data.cityofchicago.org/Health-Human-Services/Grocery-Store-Status-Map/rish-pa6g)

#### 6. Parks & Green Spaces
City of Chicago. “Parks - Chicago Park District Park Boundaries (Current) | City of Chicago | Data Portal.” Cityofchicago.org, Cityofchicago, 2018, [data.cityofchicago.org/Parks-Recreation/Parks-Chicago-Park-District-Park-Boundaries-curren/ej32-qgdr.](https://data.cityofchicago.org/Parks-Recreation/Parks-Chicago-Park-District-Park-Boundaries-curren/ej32-qgdr)

#### 7. Education Data (Schools)

Chicago Public Schools. “Search | Chicago Public Schools.” Cps.edu, CPS, 2025, [www.cps.edu/search/?pageNumber=1&context=Schools&sortId=a-z](https://www.cps.edu/search/?pageNumber=1&context=Schools&sortId=a-z). Accessed 12 Mar. 2025.

## Data Integration
All datasets are linked by ZIP code. 


Thank you so much to James Turk, our CAPP 122 lecturer, for making this journey so fruitful and supporting us as we set out on this project. Hope you enjoy interacting with this visualization!
