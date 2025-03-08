import pandas as pd

# Function to calculate Accessibility Index and update combined dataset
def calculate_accessibility_index():
        """
        Computes the Accessibility Index using essential service counts per ZIP code and updates the combined dataset.
        """
        # Load the combined dataset
        df = pd.read_csv("data/preprocessed/zipatlas_bulk_merge.csv")
        
        # Compute total services count per ZIP code
        df["total_services"] = (
            df["total_healthcare_services"]
            + df["park_count"]
            + df["grocery_store_count"]
            + df["num_public_transit_stops"]
           # + df["school_count"]
        )
        
        # Compute Accessibility Index
        df["Accessibility Index"] = df["total_services"] / df["Population"]
        
        # Save updated combined dataset
        df.to_csv("data/preprocessed/zipatlas_bulk_merge.csv", index=False)
        print("Accessibility Index calculated and added to combined dataset.")
        return df[["Zip Code", "Accessibility Index"]]
    
    # Compute Accessibility Index and update combined dataset
calculate_accessibility_index()

