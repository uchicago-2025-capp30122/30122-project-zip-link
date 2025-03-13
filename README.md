# Zip & Link

#### Team Members: Vyshnavi Voleti, Nelu Wijegunasekera, Pragya Khanal

### Overview
Zip & Link analyzes the relationship between essential services and housing affordability across neighborhoods in Chicago. The project explores how accessibility to key services—such as healthcare, public education, public transport, grocery stores, and parks—affects median property prices and other economic indicators. The project involves web scraping, bulk data downloads, data cleaning and preprocessing, and an analysis framework to generate an Accessibility Index for each ZIP code. This index is meant to help users understand the impact of essential services on housing affordability and highlight areas that require better urban planning. Our initial hypothesis was that the housing prices were positively correlated with the Accessibility Index and in order to test and better visualize this, we developed 3 key visualizations on Dash: a choropleth map, a scatterplot and horizontal bar plots that help compare 2 specific zip codes. Interestingly, we found that the converse of our hypothesis was true. 

### Demonstration of Project

[Demonstration of Zip & Link](https://www.youtube.com/watch?v=O-PwBeorkRI&ab_channel=Vyshnavi)

### How to Run

1. Clone the repo to this project using the url on GitHub
2. From the zip_link director, run ```uv sync``` to install all the necessary packages 
3. Run ```uv run python -m cleaning_analysis.zipatlas_data``` to scrape the data, clean and preprocess the data and obtain the final dataset
4. Next, run ```uv run python -m visualization.merge_visualization``` to get the Dash app running on http://127.0.0.1:8051
5. Select different variables, explore how the distribution across Chicago changes, visualize how the housing-related variables are related to the Accessibility Index on the scatterplot, and compare 2 different zip codes!
6. To ensure all our data is running correctly, run our tests 
```
uv run pytest tests/final_join_tests.py 
tests/healthctr_tests.py 
tests/parks_tests.py 
tests/grocery_stores_tests.py 
tests/merge_visualization_tests.py 
tests/publictransit_tests.py 
tests/schools_tests.py 
tests/zipatlas_scrape_tests.py 
tests/Hospitals_test.py
```
We have provided tests for the ingestion of all our data sources, data reconciliation as well as data visualizations.

### Data Citations 

#### 1. Housing Data

ZipAtlas.com. “Highest Median Property Prices in Chicago by Zip Code in 2025 | Zip Atlas.” Zipatlas.com, Zipatlas.com, 2025, [zipatlas.com/us/il/chicago/zip-code-comparison/highest-property-prices.htm](https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-property-prices.htm). Accessed 12 Mar. 2025.

#### 2. Healthcare Data

##### Community Health Centers
City of Chicago Health Facilities:
chicago.gov. https://www.chicago.gov/content/dam/city/depts/cdph/policy_planning/PP_Web%20Health%20Care%20Facilities%20by%20Zip%20Code.pdf. Accessed 12 Mar. 2025. 
 
HRSA Find a Health Center: 
Hrsa.gov. “Find a Health Center.” Hrsa.gov, Hrsa.gov, 2025, [findahealthcenter.hrsa.gov/?zip=Chicago%252C%2BIL%252C%2BUSA&radius=5&incrementalsearch=true](https://findahealthcenter.hrsa.gov/?zip=Chicago%252C%2BIL%252C%2BUSA&radius=5&incrementalsearch=true). Accessed 12 Mar. 2025. 

##### Hospitals
Cook County Sheriff's Office. “Hospitals in Cook County.” Cook County Sheriff’s Office, Cook County Sheriff’s Office, Aug. 2017, [cookcountysheriffil.gov/departments/c-c-s-p-d/cemeteries/hospitals-cook-county/](https://cookcountysheriffil.gov/departments/c-c-s-p-d/cemeteries/hospitals-cook-county/). Accessed 12 Mar. 2025. 

#### 3. Transportation Data
Institute of Social Research, University of Michigan. “National Neighborhood Data Archive (NaNDA): Public Transit Stops by Census Tract and ZIP Code Tabulation Area, United States, 2016-2018 and 2024 | ICPSR.” Umich.edu, Umich.edu, 2016, [archive.icpsr.umich.edu/view/studies/38605/data-documentation](https://archive.icpsr.umich.edu/view/studies/38605/data-documentation). Accessed 12 Mar. 2025.


#### 4. Grocery Stores Data
City of Chicago. “Grocery Store Status Map | City of Chicago | Data Portal.” Data.cityofchicago.org, Cityofchicago, [data.cityofchicago.org/Health-Human-Services/Grocery-Store-Status-Map/rish-pa6g.](https://data.cityofchicago.org/Health-Human-Services/Grocery-Store-Status-Map/rish-pa6g)

#### 5. Parks & Green Spaces
City of Chicago. “Parks - Chicago Park District Park Boundaries (Current) | City of Chicago | Data Portal.” Cityofchicago.org, Cityofchicago, 2018, [data.cityofchicago.org/Parks-Recreation/Parks-Chicago-Park-District-Park-Boundaries-curren/ej32-qgdr.](https://data.cityofchicago.org/Parks-Recreation/Parks-Chicago-Park-District-Park-Boundaries-curren/ej32-qgdr)

#### 6. Education Data (Schools)

Chicago Public Schools. “Search | Chicago Public Schools.” Cps.edu, CPS, 2025, [www.cps.edu/search/?pageNumber=1&context=Schools&sortId=a-z](https://www.cps.edu/search/?pageNumber=1&context=Schools&sortId=a-z). Accessed 12 Mar. 2025.

#### 8. Population
Illinois Demographics. “Illinois ZIP Codes by Population.” Illinois-Demographics.com, 2025,[www.illinois-demographics.com/zip_codes_by_population](https://www.illinois-demographics.com/zip_codes_by_population). Accessed 12 Mar. 2025.  


### Data Integration
All datasets are linked by ZIP code. 

### Acknowledgement 
Thank you so much to James Turk, our CAPP 122 lecturer, and to Hieu Nguyen, our CAPP 122 TA, for supporting and helping us as we set out on this project. We couldn't have done this without them, and are incredibly grateful :) Hope you enjoy exploring our visualization!
