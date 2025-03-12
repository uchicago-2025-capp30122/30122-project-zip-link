import pandas as pd

def calculate_accessibility_index():
    """
     Computes the Accessibility Index by normalizing individual service counts per ZIP code,
     then using these normalized values to compute the index.
    """
    df = pd.read_csv("data/preprocessed/zipatlas_bulk_merge.csv")

    # List of variables to normalize
    service_columns = [
        "total_healthcare_services",
        "park_count",
        "grocery_store_count",
        "num_public_transit_stops",
        "school_count",
    ]

    # Normalize each service variable
    for col in service_columns:
        min_val = df[col].min()
        max_val = df[col].max()
        df[f"normalized_{col}"] = (df[col] - min_val) / (max_val - min_val)

    # Compute total normalized services count per ZIP code
    df["total_normalized_services"] = df[
        [f"normalized_{col}" for col in service_columns]
    ].sum(axis=1)

    # Compute Accessibility Index using normalized values
    df["Accessibility Index"] = df["total_normalized_services"] / df["Population"]

    # Debugging: Print min/max values
    min_index = df["Accessibility Index"].min()
    max_index = df["Accessibility Index"].max()
    
    # Round (max - min) to 6 decimal places for better precision
    max_min_diff = round(max_index - min_index, 6)

    # Normalize the Accessibility Index 
    df["Normalized Accessibility Index"] = (
        (df["Accessibility Index"] - min_index) / max_min_diff
    ).round(2)
    
    # Save updated combined dataset
    df.to_csv("data/preprocessed/zipatlas_bulk_merge.csv", index=False)
    print("Accessibility Index calculated using normalized variables and added to the dataset.")
    return df[["Zip Code", "Accessibility Index", "Normalized Accessibility Index"]]
