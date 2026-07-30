import unittest
from engine import EWSDecisionEngine

class TestEWSDecisionEngine(unittest.TestCase):
    
    def setUp(self):
        """Initialize the decision framework router before every verification run."""
        self.engine = EWSDecisionEngine(base_income_limit=800000)

    def test_ppp_tier_adjustments(self):
        """Verify that geographic cost-of-living purchasing parity thresholds adjust accurately."""
        self.assertEqual(self.engine.calculate_ppp_adjusted_limit('Tier-1'), 1000000.0) # 800k * 1.25
        self.assertEqual(self.engine.calculate_ppp_adjusted_limit('Tier-2'), 800000.0)  # 800k * 1.00
        self.assertEqual(self.engine.calculate_ppp_adjusted_limit('Tier-3'), 600000.0)  # 800k * 0.75

    def test_ancestral_grandfather_loophole_resolution(self):
        """Ensure undivided ancestral land is correctly portioned into virtual father-share percentages."""
        # Scenario A: Deceased Grandfather, 20 acres split among 2 siblings = 10 acres direct notional inheritance
        share_deceased = self.engine.resolve_ancestral_assets(20, 'Deceased', 2)
        self.assertEqual(share_deceased, 10.0)

        # Scenario B: Living Grandfather, 20 acres split among 2 siblings with future expectation risk buffer (25%)
        share_living = self.engine.resolve_ancestral_assets(20, 'Alive', 2)
        self.assertEqual(share_living, 2.5)

    def test_wealthy_evader_detection(self):
        """Test if applicants reporting low income but possessing high utility and UPI data are flagged."""
        evader_payload = {
            "Reported_Income_INR": 200000.0,
            "UPI_Transaction_Volume_INR": 3500000.0, # High digital velocity
            "Annual_Utility_Bills_INR": 150000.0,     # Out of bounds consumption footprint
            "Nuclear_Property_SqFt": 200.0,
            "Grandfather_Land_Acres": 0.0,
            "Grandfather_Living_Status": 'Alive',
            "Father_Siblings_Count": 1
        }
        
        result = self.engine.evaluate_applicant(evader_payload, 'Tier-1')
        self.assertEqual(result['Status'], "FLAGGED_FOR_AUDIT")
        self.assertTrue(result['Risk_Score'] >= 60)

if __name__ == '__main__':
    unittest.main()
