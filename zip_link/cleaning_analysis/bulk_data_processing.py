import pandas as pd

def clean_parks_data(path):
    df = pd.read_csv(path)
    df = df[['PARK', 'LOCATION', 'ZIP', 'PARK_CLASS']]
    # Drop null rows if either PARK or ZIP is empty
    df = df.dropna(subset=['PARK', 'ZIP'])
    # Ensure only valid Park Names are included
    df = df[df['PARK'].str.contains(r'[a-zA-Z]', na=False)]
    # Ensure ZIP is 5 digits
    df['ZIP'] = df['ZIP'].astype(str).str[:5].str.zfill(5)
    # Rename columns
    df.columns = ['Park', 'Location', 'Zip Code', 'Park_Class']
    # Remove duplicates
    df = df.drop_duplicates()
    zip_counts = df["Zip Code"].value_counts().reset_index()
    zip_counts.columns = ["Zip Code", "park_count"]
    df.to_csv("data/preprocessed/park_data.csv", index=False)
    return zip_counts

def clean_grocery_data(path):
    df = pd.read_csv(path)
    # Filter open stores only
    df = df[df['New status'] == 'OPEN']
    # Ensure Zip Code is 5 digits long
    df['Zip'] = df['Zip'].str[:5].str.zfill(5) 
    df = df.drop_duplicates() # Drop duplicates

    # Subset and rename data 
    df = df[['Store Name', 'Address', 'Zip', 'New status']]
    df.columns = ['GroceryStore', 'Address', 'Zip Code', 'Status']

    # Calculate Grocery Store Count for each Zip Code
    zip_counts = df["Zip Code"].value_counts().reset_index()
    zip_counts.columns = ["Zip Code", "grocery_store_count"]
    df.to_csv("data/preprocessed/grocery_store_data.csv", index=False)
    return zip_counts

def clean_publictransit_data(path):
    df = pd.read_csv(path)
    # Filter relevant Zip Codes
    df['ZCTA20'] = df['ZCTA20'].astype(str).str[:5].str.zfill(5)
    df = df[df['ZCTA20'].str.startswith('606')]
    df= df[['ZCTA20', 'COUNT_NTM_STOPS']]
    df.columns = ['Zip Code', 'num_public_transit_stops']
    return df 

def clean_hospital_data(path):
        """
        Cleans the hospital data by:
        - Dropping missing values
        - Ensuring ZIP code is 5 digits
        - Removing duplicates
        - Saving cleaned data to preprocessed folder
        """
        df = pd.read_csv(path)
        df = df.dropna(subset=['Hospital Name', 'ZIP Code'])  # Drop null values
        df['ZIP Code'] = df['ZIP Code'].astype(str).str[:5].str.zfill(5)  # Standardize ZIP codes
        df.columns = ['Hospital Name', 'Zip Code']  # Rename columns
        df = df.drop_duplicates()  # Remove duplicates
        
        # Count hospitals per ZIP code
        Zip_Hospital_Counts = df["Zip Code"].value_counts().reset_index()
        Zip_Hospital_Counts.columns = ["Zip Code", "hospital_count"]
        
        # Save cleaned data
        df.to_csv("data/preprocessed/hospital_data.csv", index=False)
        return Zip_Hospital_Counts








