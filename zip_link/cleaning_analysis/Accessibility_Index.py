import pandas as pd

def calculate_accessibility_index():
    """
    Computes the Accessibility Index using essential service counts per ZIP code, normalizes it, and updates the combined dataset.
    """
    df = pd.read_csv("data/preprocessed/zipatlas_bulk_merge.csv")

    # Compute total services count per ZIP code
    df["total_services"] = (
        df["total_healthcare_services"]
        + df["park_count"]
        + df["grocery_store_count"]
        + df["num_public_transit_stops"]
        + df["school_count"]
    )

    # Compute Accessibility Index
    df["Accessibility Index"] = df["total_services"] / df["Population"]

    # Debugging: Print min/max values
    min_index = df["Accessibility Index"].min()
    max_index = df["Accessibility Index"].max()
    
    # Round (max - min) to 6 decimal places for better precision
    max_min_diff = round(max_index - min_index, 6)
    print(f"Min Accessibility Index: {min_index}, Max Accessibility Index: {max_index}, Difference: {max_min_diff}")

    # Normalize the Accessibility Index 
    df["Normalized Accessibility Index"] = (
        (df["Accessibility Index"] - min_index) / max_min_diff
    ).round(2)
    
    # Save updated combined dataset
    df.to_csv("data/preprocessed/zipatlas_bulk_merge.csv", index=False)
    print("Accessibility Index calculated, normalized, and added to combined dataset.")
    return df[["Zip Code", "Accessibility Index", "Normalized Accessibility Index"]]

calculate_accessibility_index()