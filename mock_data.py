import numpy as np
import pandas as pd

def generate_synthetic_profile(pincode_tier):
    """
    Generates a single synthetic API data response from linked state registries.
    Tiers: 'Tier-1' (High Cost), 'Tier-2' (Medium), 'Tier-3' (Low)
    """
    profile_type = np.random.choice(['Genuine_Low_Income', 'Wealthy_Evader', 'Middle_Class_Borderline'], p=[0.5, 0.2, 0.3])
    
    # Establish base profiles
    if profile_type == 'Genuine_Low_Income':
        reported_income = np.random.uniform(100000, 350000)
        upi_volume = np.random.uniform(30000, 150000)
        utility_bills = np.random.uniform(3000, 12000)
        nuclear_property_sqft = np.random.uniform(0, 500)
        grandfather_land_acres = np.random.uniform(0, 2)
        
    elif profile_type == 'Wealthy_Evader':
        reported_income = np.random.uniform(150000, 450000)     # Hiding income on paper
        upi_volume = np.random.uniform(1500000, 5000000)        # Massive real digital footprint
        utility_bills = np.random.uniform(90000, 300000)        # High electricity/luxury expenses
        nuclear_property_sqft = np.random.uniform(300, 900)     # Keeps personal property small
        grandfather_land_acres = np.random.uniform(7, 40)       # Multi-crore ancestral land loophole
        
    else: # Middle Class Borderline
        reported_income = np.random.uniform(550000, 850000)
        upi_volume = np.random.uniform(400000, 950000)
        utility_bills = np.random.uniform(20000, 65000)
        nuclear_property_sqft = np.random.uniform(600, 1200)
        grandfather_land_acres = np.random.uniform(1, 4)

    # Geographic adjustments based on Cost of Living
    if pincode_tier == 'Tier-1':
        utility_bills *= 1.4
    elif pincode_tier == 'Tier-3':
        utility_bills *= 0.75

    payload = {
        "Applicant_ID": f"RES_{np.random.randint(100000, 999999)}",
        "Reported_Income_INR": round(reported_income, 2),
        "UPI_Transaction_Volume_INR": round(upi_volume, 2),
        "Annual_Utility_Bills_INR": round(utility_bills, 2),
        "Nuclear_Property_SqFt": round(nuclear_property_sqft, 2),
        "Grandfather_Land_Acres": round(grandfather_land_acres, 2),
        "Grandfather_Living_Status": np.random.choice(['Alive', 'Deceased'], p=[0.6, 0.4]),
        "Father_Siblings_Count": np.random.randint(1, 5),
        "True_Segment": profile_type
    }
    return payload

def generate_bulk_dataset(records_count=1000):
    """
    Generates a bulk pandas DataFrame simulating a state database for analytics.
    """
    tiers = ['Tier-1', 'Tier-2', 'Tier-3']
    data_list = []
    
    for _ in range(records_count):
        selected_tier = np.random.choice(tiers, p=[0.3, 0.4, 0.3])
        profile = generate_synthetic_profile(selected_tier)
        profile['Pincode_Tier'] = selected_tier
        data_list.append(profile)
        
    df = pd.DataFrame(data_list)
    return df

# Local script execution for testing and CSV creation
if __name__ == "__main__":
    print("⏳ Initializing pipeline: Generating 1,000 synthetic EWS application telemetry records...")
    mock_db = generate_bulk_dataset(1000)
    
    # Save the synthetic data pipeline output to a CSV file
    file_name = "synthetic_ews_registry_data.csv"
    mock_db.to_csv(file_name, index=False)
    print(f"✅ Data pipeline generation complete! Saved as '{file_name}'")
    print(mock_db.head(5))
