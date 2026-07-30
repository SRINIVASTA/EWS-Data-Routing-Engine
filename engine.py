import numpy as np

class EWSDecisionEngine:
    def __init__(self, base_income_limit=800000):
        self.base_income_limit = base_income_limit

    def calculate_ppp_adjusted_limit(self, tier):
        """Dynamic Tiering Logic based on Purchasing Power Parity (PPP)"""
        weights = {'Tier-1': 1.25, 'Tier-2': 1.00, 'Tier-3': 0.75}
        return self.base_income_limit * weights.get(tier, 1.00)

    def resolve_ancestral_assets(self, grandfather_acres, living_status, siblings):
        """Calculates Notional Inheritance Share to close the grandfather loophole"""
        if grandfather_acres == 0:
            return 0
        if living_status == 'Deceased':
            # split evenly among father's siblings
            return grandfather_acres / siblings
        else:
            # If grandfather is alive, model a 25% future probability asset weight
            return (grandfather_acres / siblings) * 0.25

    def evaluate_applicant(self, data, tier):
        adjusted_income_limit = self.calculate_ppp_adjusted_limit(tier)
        notional_land = self.resolve_ancestral_assets(
            data['Grandfather_Land_Acres'], 
            data['Grandfather_Living_Status'], 
            data['Father_Siblings_Count']
        )
        
        total_effective_land = data['Nuclear_Property_SqFt'] / 43560 + notional_land # Convert Sqft to Acres
        
        # Anomaly / Risk Scoring Logic
        risk_score = 0
        if data['UPI_Transaction_Volume_INR'] > (data['Reported_Income_INR'] * 2.5):
            risk_score += 40  # Massive hidden digital cash flow
        if data['Annual_Utility_Bills_INR'] > (data['Reported_Income_INR'] * 0.4):
            risk_score += 30  # High lifestyle consumption proxy
        if total_effective_land > 5:
            risk_score += 30  # Land limit breach
            
        # Decision Matrix
        if risk_score >= 60 or data['Reported_Income_INR'] > adjusted_income_limit:
            status = "FLAGGED_FOR_AUDIT"
        elif risk_score >= 30:
            status = "MANUAL_REVIEW_REQUIRED"
        else:
            status = "ELIGIBLE"
            
        return {
            "Status": status,
            "Risk_Score": risk_score,
            "Effective_Land_Acres": round(total_effective_land, 2),
            "Adjusted_Income_Threshold": adjusted_income_limit
        }
