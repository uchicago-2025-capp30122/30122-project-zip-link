# Project Repository Template

This template is intentionally mostly empty, to give you experience starting a project from scratch.

A good first command would be to run `uv init` and add some libraries and tools that you are using.

Before the final milestone submission, you will need to replace this file with a README as described here: https://capp30122.netlify.app/coursework/project/#readmemd

# Zip & Link

## Abstract

In this project we will consider the effect of essential services on housing affordability in the neighbourhoods of Chicago. We will consider essential services such as access to schools, healthcare, public transport, groceries, and green spaces. This information will be obtained from various sources such as City of Chicago for Parks and Grocery Stores, and other studies/datasets as explained below. Additionally, the financial housing data will come from ZipAtlas and all of this will be web scraped. We plan to explore this correlation between housing prices and essential services using an 'accessibility index' that will be calculated using the number of facilities in a given zip code. Hence, Zip and Link. The goal of this project is to develop an interface that would enable the end user to understand key indicators of housing affordability as well as identify neighbourhoods that need better urban planning.

## Data Sources

Data Reconciliation Plan
Our data sources will be joined by the zipcode. Each of our data sources includes an address/zip code component, which makes it easy for us to merge these datasets together. We can then combine zip codes, housing prices data, and the essential services data. Using this, we can develop our Accessibility Index for each zip code for end-users, so that they can get a better understanding of how each neighbourhood’s median housing prices are affected by the accessibility index.

### Data Source #1: 
Zip Atlas: https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-property-prices.htm
The data comes from a webpage, which we plan on scraping. We ran a sample using Beautiful Soup and were able to extract the data in the format we wanted with no issues. We will replicate this with the lxml.html methods soon.



### Data Source #2: Health Services
Health services will be considered to be hospitals and community health centers. We have identified two sources:

Hospitals: https://health.usnews.com/best-hospitals/area/chicago-il
This data will be web scraped from the above URL, as opposed to using the Google Maps API we initially planned on (due to the cost).

Challenges: We anticipate some time will be spent in cleaning the list of hospitals as it consists of some that are out of Chicago city. The scraping would also have to be written in a way to allow the page to load a few more of the data once we have scrolled to the end of the page and do so continually until there is no more data to be loaded.

Rows: There are 117 records included for the Chicago area with the zip code indicated, from which we expect to use around 100 records for the project.

Properties to be extracted: 2 - Zip Code and Number of Hospitals

Community Health Centers: https://www.chicago.gov/content/dam/city/depts/cdph/policy_planning/PP_Web%20Health%20Care%20Facilities%20by%20Zip%20Code.pdf https://findahealthcenter.hrsa.gov/?zip=Chicago%252C%2BIL%252C%2BUSA&radius=5&incrementalsearch=true
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
https://data.cityofchicago.org/Health-Human-Services/Grocery-Store-Status-Map/rish-pa6g This data is available from the City of Chicago on the locations of the grocery stores with the zip codes, and this can be downloaded as bulk data in the form of a csv file.

Challenges: This data looks clean and pre-processed. However, it was last updated in 2020, which means it is not the latest version. That said, given that grocery stores typically tend to be around for a while, we consider this recent enough to be used in the project.

Rows: 264

Properties: 2 - Zip Code and Store Name

### Data Source #5: Parks and green spaces
https://data.cityofchicago.org/Parks-Recreation/Parks-Chicago-Park-District-Park-Boundaries-curren/ej32-qgdr

This data is also downloaded as bulk data from the City of Chicago, which contains the locations of parks in Chicago with their respective zip codes. This data was last updated in 2024 which is ideal in terms of recency.

Challenges: None, as we are not anticipating any significant issues in cleaning this data set.

Rows: There are 617 rows of data.

Properties: 2 - Zip Code and Park Name

### Data Source #6: Schools
Current sources for schooling information: https://www.niche.com/k12/search/best-private-schools/t/chicago-cook-il/ and https://www.niche.com/k12/search/best-private-schools/t/chicago-cook-il/ respectively through web scraping.

Challenges:
At this stage, we have a challenge that we're looking into:
1. scraping data on schools: there was a challenge in accessing and scraping the necessary details as we have to circumvent the security measures added by the website. These include the details on the user-agent and cookie sent when accessing the website.
2. also, looking at alternative sites for data and the ease of scraping:
   private schools: https://www.privateschoolreview.com/illinois/chicago
   public schools: https://www.cps.edu/search/?pageNumber=1&context=Schools&sortId=a-z

## Visualization
We have added code for the visualizaton and have generated a map on the zip codes of Chicago using demo data. We have a few improvements that we wanted to make for the final presentation. Including:
1. adding the zip code as a label to the map
2. adding more points of information as we hover over the zip code areas
3. change colour to reflect a gradient



