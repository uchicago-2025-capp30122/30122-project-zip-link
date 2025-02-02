# Zip & Link

## Abstract

In this project we will consider the effect of essential services on housing affordability in the neighbourhoods of Chicago. We will consider essential services such as access to schools, healthcare, public transport, groceries, and green spaces. This information will be obtained from various sources such as City of Chicago for Parks and Grocery Stores, and other studies/datasets as explained below. Additionally, the financial housing data will come from ZipAtlas and all of this will be web scraped. We plan to explore this correlation between housing prices and essential services using an 'accessibility index' that will be calculated using the number of facilities in a given zip code. Hence, Zip and Link. The goal of this project is to develop an interface that would enable the end user to understand key indicators of housing affordability as well as identify neighbourhoods that need better urban planning.

## Data Sources

### Data Reconciliation Plan

Our data sources will be joined by the zipcode. Each of our data sources includes an address/zip code component, which makes it easy for us to merge these datasets together. We can then combine zip codes, housing prices data, and the essential services data. Using this, we can develop our Accessibility Index for each zip code for end-users, so that they can get a better understanding of how each neighbourhood’s median housing prices are affected by the accessibility index. 

### Data Source #1: Zip Atlas: https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-property-prices.htm 

The data comes from a webpage, which we plan on scraping. We ran a sample using Beautiful Soup and were able to extract the data in the format we wanted with no issues. We will replicate this with the lxml.html methods soon.

Challenges: 
1. The data seems to be missing some relevant zip codes in Chicago (only 54 are present). As such, for this project, we are planning to focus on these 54 zip codes. 
2. ZipAtlas was temporarily down earlier on 2nd Feb 2025, but it is back up now. In the case that this repeats, we will have a backup data source from Zillow, where we will use Zillow’s Home Value Index to reflect housing prices in different neighbourhoods. https://www.zillow.com/research/data/ 

Rows: 54
Properties: 7 - Median Housing Costs, Property Prices, Owner Housing Costs, Renter Housing Costs, Housing Costs/Income, Unemployment Rates, Poverty Levels. We will be able to join all relevant columns using the zip codes. 

As mentioned above, we have done a preliminary scraping of the dataset from ZipAtlas, and were able to obtain 54 zip codes for Property Prices, but there were some other variables such as Median Housing Costs that had data on 56 zip codes. Thus, we will have to drop the zip codes that do not have all the variables we desire to extract. 

### Data Source #2: Health Services
Health services will be considered to be hospitals and community health centers. We have identified two sources:

1. Hospitals: https://health.usnews.com/best-hospitals/area/chicago-il 

This data will be web scraped from the above URL, as opposed to using the Google Maps API we initially planned on (due to the cost). 

Challenges: We anticipate some time will be spent in cleaning the list of hospitals as it consists of some that are out of Chicago city. The scraping would also have to be written in a way to allow the page to load a few more of the data once we have scrolled to the end of the page and do so continually until there is no more data to be loaded. 

Rows: There are 117 records included for the Chicago area with the zip code indicated, from which we expect to use around 100 records for the project. 

Properties to be extracted: 2 - Zip Code and Number of Hospitals 

2. Community Health Centers:
https://www.chicago.gov/content/dam/city/depts/cdph/policy_planning/PP_Web%20Health%20Care%20Facilities%20by%20Zip%20Code.pdf
https://findahealthcenter.hrsa.gov/?zip=Chicago%252C%2BIL%252C%2BUSA&radius=5&incrementalsearch=true

Challenges: We have two sources of data for community health centers, which we will amalgamate and drop the duplicates, once scraped. The zip code level information is available for each health care center which can be used to merge with the overall data set. 

Rows: There are currently 373 rows of data, but we anticipate some time used to clean this data set as it has health care centers from Indiana and Wisconsin. 

Properties: 2 - Zip Code and List of Healthcare Centers

### Data Source #3: Transportation data
https://archive.icpsr.umich.edu/view/studies/38605/data-documentation

We were able to get the raw data used for this project by the Institute of Social Research at the University of Michigan. This dataset entails the number of public transit stops amalgamated for each zip code, as well as the total population, stops per capita and stops per sq.mile. This will be directly downloaded as bulk data in the form of an excel file. 

Challenges: There should be minimal challenges with this data source as it is rather straight-forward. However, there may be similar issues of not all zip codes being represented in the data. In such a situation, we will have to do some data pre-processing and cleaning to ensure the data point can be used.

Rows: 56 Chicago Zip Codes

Properties: 4 - Total Population, Stops Per Capita, Stops per Square Mile and Count of Public Transit Stops 
  
### Data Source #4: Grocery stores
https://data.cityofchicago.org/Health-Human-Services/Grocery-Store-Status-Map/rish-pa6g
This data is available from the City of Chicago on the locations of the grocery stores with the zip codes, and this can be downloaded as bulk data in the form of a csv file. 

Challenges: This data looks clean and pre-processed. However, it was last updated in 2020, which means it is not the latest version. That said, given that grocery stores typically tend to be around for a while, we consider this recent enough to be used in the project. 

Rows: 264

Properties: 2 - Zip Code and Store Name 

### Data Source #5: Parks and green spaces
https://data.cityofchicago.org/Parks-Recreation/Parks-Chicago-Park-District-Park-Boundaries-curren/ej32-qgdr 

This data is also downloaded as bulk data from the City of Chicago, which contains the locations of parks in Chicago with their respective zip codes. This data  was last updated in 2024 which is ideal in terms of recency.

Challenges: None, as we are not anticipating any significant issues in cleaning this data set.

Rows: There are 617 rows of data. 

Properties: 2 - Zip Code and Park Name 

### Data Source #6: Schools

The data for public schools and private schools will be extracted from 
https://www.niche.com/k12/search/best-private-schools/t/chicago-cook-il/
and https://www.niche.com/k12/search/best-private-schools/t/chicago-cook-il/ respectively through web scraping. 

Challenges: The scraping would require us to go to the link on the name of the school and get the zip code from the address provided. We would have to scrape the whole address as an element and further clean it to obtain the zip code, which may be a tedious process. 

Rows: Public Schools - There are 729 rows of data on the Niche website that include traditional, charter and magnet schools for public schools. 
Private Schools - There are 764 rows of data in the Niche website. These will be scraped and added to the data set.

Properties - 3 - Zip Code and Counts of Public/Private Schools 

## Project Plan

1. Data Preparation/Scraping: Schools Data - Nelu , Hospitals - Pragya, Community Health centers - Vyshnavi
2. Data Cleaning - Ensuring all the data flows into one comprehensive cleaned dataset (Pragya)
3. From the cleaned data, developing the Accessibility index (While the team will decide how the index will be created, implementation - Nelu)
4. Writing Tests for different data sources - Everyone will be in charge of the data they were working on
By Milestone 3 we will have the data set scraped and cleaned, and the Index will be implemented. 
After ensuring our data is pre-processed and cleaned, we will start developing the interface/app. 
5. Code Structure for Interface - Nelu 
6. Visualization (We will have a table view where the user will input a zip code and the output would be the data and the index. There will be additional functionality where the user will be able to compare up to three neighbourhoods. - Pragya and Vyshnavi).
7. Optionally, to explore visualizations through maps as well

## Questions

1. If we were to explore visualizations in the form of a map for the various zip codes, we are still unclear as to how to map a zip code to a visual representation geographically. Would this be something we will learn in class? Is there any suggested way to move forward with this?
2. What packages are typically used for building an app interface in Python? 
3. Does it matter if we code on the CAPP servers or do we need to run anything locally?

