import pandas as pd
import os

def clean_parks_data(path):

    """
    Preprocesses the raw parks data by:
     - Subsetting relevant columns
     - Dropping rows if PARK or ZIP is empty
     - Ensuring only valid Park Names are included
     - Ensuring Zip Code is 5 digits 
     - Renaming columns and dropping duplications
     - Calculating Park Count for each Zip Code

     Input:
     path (str): Takes the path of the raw parks data 

     Returns:
     zip_counts (dataframe): Zip Code and count of parks

    """

    df = pd.read_csv(path)
    df = df[['PARK', 'LOCATION', 'ZIP', 'PARK_CLASS']] # Subset cols

    # Drop null rows if either PARK or ZIP is empty
    df = df.dropna(subset=['PARK', 'ZIP'])

    # Ensure only valid Park Names are included
    df = df[df['PARK'].str.contains(r'[a-zA-Z]', na=False)]

    # Ensure ZIP is 5 digits
    df['ZIP'] = df['ZIP'].astype(str).str[:5].str.zfill(5)

    # Rename columns and drop duplicates 
    df.columns = ['Park', 'Location', 'Zip Code', 'Park_Class']
    df = df.drop_duplicates()

    # Get park_count for each Zip Code 
    zip_counts = df["Zip Code"].value_counts().reset_index()
    zip_counts.columns = ["Zip Code", "park_count"]
    df.to_csv("data/preprocessed/park_data.csv", index=False)
    return zip_counts
 
def clean_grocery_data(path):

    """
    Preprocesses the raw grocery stores data by:
     - Filtering out OPEN stores only 
     - Ensuring Zip Code is 5 digits 
     - Removing unnecessary spaces from Store Name and Address
     - Dropping duplicates and renaming columns
     - Calculating Grocery Store Count for each Zip Code

     Input:
     path (str): Takes the path of the raw grocery stores data 

     Returns:
     zip_counts (dataframe): Zip Code and count of grocery stores

    """
    df = pd.read_csv(path)
    # Filter open stores only
    df = df[df['New status'] == 'OPEN']
    # Ensure Zip Code is 5 digits long
    df['Zip'] = df['Zip'].astype(str).str[:5].str.zfill(5) 

    # Remove unnecessary spaces
    df['Store Name'] = df['Store Name'].str.replace(r'\s+', ' ', regex=True).str.strip()
    df['Address'] = df['Address'].str.replace(r'\s+', ' ', regex=True).str.strip()

    # Drop duplicates
    df = df.drop_duplicates() 

    # Subset and rename data 
    df = df[['Store Name', 'Address', 'Zip', 'New status']]
    df.columns = ['GroceryStore', 'Address', 'Zip Code', 'Status']

    # Calculate Grocery Store Count for each Zip Code
    zip_counts = df["Zip Code"].value_counts().reset_index()
    zip_counts.columns = ["Zip Code", "grocery_store_count"]
    df.to_csv("data/preprocessed/grocery_store_data.csv", index=False)
    return zip_counts

def clean_publictransit_data(path):

    """
    Preprocesses the public transit data by:
     - Ensuring Zip Codes are 5 digits and extracting relevant ones starting with 606
     - Filtering columns and enaming them

     Input:
     path (str): Takes the path of the raw public transit data 

     Returns:
     df (dataframe): Zip Code and count of public transit stops

    """  
    df = pd.read_csv(path)
    # Filter relevant Zip Codes
    df['ZCTA20'] = df['ZCTA20'].astype(str).str[:5].str.zfill(5)
    df = df[df['ZCTA20'].str.startswith('606')]
    df= df[['ZCTA20', 'COUNT_NTM_STOPS']]
    df.columns = ['Zip Code', 'num_public_transit_stops']
    df.to_csv("data/preprocessed/public_transit_data.csv", index=False)
    return df 

def clean_hospital_data(path):

    """
    Cleans the hospital data by:
    - Dropping missing values
    - Ensuring ZIP code is 5 digits
    - Removing duplicates
    - Saving cleaned data to preprocessed folder

    Input:
    path (str): Takes the path of the raw hospital data 

    Returns:
    zip_hospital_counts (dataframe): Zip Code and count of hospitals

    """
    df = pd.read_csv(path)
    df = df.dropna(subset=['Hospital Name', 'ZIP Code'])  # Drop null values
    df['ZIP Code'] = df['ZIP Code'].astype(str).str[:5].str.zfill(5)  # Standardize ZIP codes
    df.columns = ['Hospital Name', 'Zip Code']  # Rename columns
    df = df.drop_duplicates()  # Remove duplicates
        
    # Count hospitals per ZIP code
    zip_hospital_counts = df["Zip Code"].value_counts().reset_index()
    zip_hospital_counts.columns = ["Zip Code", "hospital_count"]
        
    # Save cleaned data
    df.to_csv("data/preprocessed/hospital_data.csv", index=False)
    return zip_hospital_counts

def clean_school_data(path):
        
    """
    Cleans the school data by:
    - Dropping missing values
    - Ensuring ZIP code is 5 digits
    - Removing duplicates
    - Saving cleaned data to preprocessed folder

    Input:
    path (str): Takes the path of the raw school data 

    Returns:
    zip_school_counts (dataframe): Zip Code and public school count

    """
    df = pd.read_csv(path)
    df = df.dropna(subset=['School Name', 'Zip Code'])  # Drop null values
    df['Zip Code'] = df['Zip Code'].astype(str).str[:5].str.zfill(5)  # Standardize ZIP codes
    df = df.drop_duplicates()  # Remove duplicates
        
    # Count hospitals per ZIP code
    zip_school_counts = df["Zip Code"].value_counts().reset_index()
    zip_school_counts.columns = ["Zip Code", "school_count"]
        
    # Save cleaned data
    df.to_csv("data/preprocessed/school_data.csv", index=False)
    return zip_school_counts



def clean_population_data(path):

    """
    Cleans the population data by:
    - Keeping only relevant columns ('Zip Code' and 'Population')
    - Dropping missing values
    - Standardizing ZIP codes to 5 digits
    - Removing duplicates
    - Aggregating population per ZIP code
    - Saving cleaned data to preprocessed folder
    - Returning the cleaned DataFrame

    Input:
    path (str): Takes the path of the raw population data 

    Returns:
    population_df (dataframe): Zip Code and population

    """
    # Load the dataset
    population_df = pd.read_csv(path)

    # Keep only relevant columns and rename them
    population_df = population_df[['Entity properties name', 'Variable observation value']].rename(columns={
        'Entity properties name': 'Zip Code',
        'Variable observation value': 'Population'
    })

    # Drop missing values
    population_df = population_df.dropna(subset=['Zip Code', 'Population'])

    # Ensure ZIP codes are standardized (5 digits)
    population_df['Zip Code'] = population_df['Zip Code'].astype(str).str[:5].str.zfill(5)

    # Convert Population to integer
    population_df['Population'] = pd.to_numeric(population_df['Population'], errors='coerce').fillna(0).astype(int)

    # Remove duplicates
    population_df = population_df.drop_duplicates()

    # Save cleaned data
    output_path = "data/preprocessed/population_data.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Ensure directory exists
    population_df.to_csv(output_path, index=False)

    return population_df  