import numpy as np
import pandas as pd

def generate_synthetic_profile(pincode_tier):
    """
    Generates a single synthetic API data response from linked state registries.
    Tiers: 'Tier-1' (High Cost), 'Tier-2' (Medium), 'Tier-3' (Low)
    """
    profile_type = np.random.choice(['Genuine_Low_Income', 'Wealthy_Evader', 'Middle_Class_Borderline'])
    
    # Establish base profiles
    if profile_type == 'Genuine_Low_Income':
        reported_income = np.random.uniform(150000, 350000)
        upi_volume = np.random.uniform(50000, 200000)
        utility_bills = np.random.uniform(5000, 15000)
        nuclear_property_sqft = np.random.uniform(0, 400)
        grandfather_land_acres = np.random.uniform(0, 1.5)
        
    elif profile_type == 'Wealthy_Evader':
        reported_income = np.random.uniform(200000, 500000) # Reports low income
        upi_volume = np.random.uniform(1200000, 4500000)    # Massive digital cash flows
        utility_bills = np.random.uniform(80000, 250000)    # High luxury footprint
        nuclear_property_sqft = np.random.uniform(200, 800) # Small personal property
        grandfather_land_acres = np.random.uniform(8, 45)   # Hiding wealth behind grandfather
        
    else: # Middle Class
        reported_income = np.random.uniform(500000, 780000)
        upi_volume = np.random.uniform(400000, 900000)
        utility_bills = np.random.uniform(20000, 60000)
        nuclear_property_sqft = np.random.uniform(500, 1100)
        grandfather_land_acres = np.random.uniform(1, 4)

    # Adjust spending slightly based on geographic location
    if pincode_tier == 'Tier-1':
        utility_bills *= 1.5
    elif pincode_tier == 'Tier-3':
        utility_bills *= 0.7

    payload = {
        "Reported_Income_INR": round(reported_income, 2),
        "UPI_Transaction_Volume_INR": round(upi_volume, 2),
        "Annual_Utility_Bills_INR": round(utility_bills, 2),
        "Nuclear_Property_SqFt": round(nuclear_property_sqft, 2),
        "Grandfather_Land_Acres": round(grandfather_land_acres, 2),
        "Grandfather_Living_Status": np.random.choice(['Alive', 'Deceased']),
        "Father_Siblings_Count": np.random.randint(1, 4)
    }
    return payload
