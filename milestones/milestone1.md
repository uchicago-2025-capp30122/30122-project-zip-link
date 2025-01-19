# Zip & Link

## Members

- Nelu Wijegunasekera <neluw@uchicago.edu>
- Pragya Khanal <khanalp@uchicago.edu>
- Vyshnavi Voleti <vyshnaviv@uchicago.edu>

## Abstract

In this project we will consider the effect of essential services on housing affordability in the neighbourhoods of Chicago. We will consider essential services such as access to schools, healthcare, public transport, groceries, and green spaces.  This information will be obtained by scraping Google Maps using an API, and the financial and demographic data will come from ZipAtlas. We plan to explore this correlation using an 'accessibility index' that will be calculated using the number of facilities in a given radius from the coordinates of each neighbourhood. The goal of this project is to develop a visualization or an app that would enable the end user to understand key indicators of housing affordability as well as identify neighbourhoods that need better urban planning. 

## Preliminary Data Sources

### Data Source #1: ZipAtlas

- [https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-housing-costs.htm]
- The data will be scraped from the webpage.
- The data looks clean as of now, but we will have to do some basic data validation to verify this. E.g. checking for missing values, checking if all the zipcodes of Chicago are represented, merging the data sets.

### Data Source #2: Google Maps

- [https://www.google.com/maps]
- The data will be taken using the Google Maps API and a geocoding API to get the approximate coordinates to each zipcode.
- We anticipate this data set would require some cleaning to identify the essential services and classify them accordingly.

## Preliminary Project Plan

Data cleaning, preparation, and ingestion
1. First, get all the neighbourhood data merged into one cohesive dataset. At the moment ZipAtlas has different data points on financial statistics as well as physical characteristics of each neighbourhoods. We want to ensure we can merge all of this data using the zipcode as the primary key. (Vyshnavi and Pragya) 
2. We need to use an API to get the approximate coodinates for the zipcodes. (Nelu)
3. Using Google Maps API, we will then determine what type and number of facilities will be used in this project. For instance, for zipcode 60637, how many hospitals, schools, grocery stores, public transport options and parks are available. (all team members and will take charge of different facilities individually)

Data visualization
4. Using this, we will come up with an accessibility index for each neighbourhood and analyse how it differs across Chicago. (Nelu)
5. This data will then be fed into a visualization that the end user can play around with. (all team members)

## Questions

1. Using an API in general
2. Working with missing data
3. Designing an accessibility index
4. Optimum way to visualize the data for the end user
