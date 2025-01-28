from typing import List, Dict

def get_adjustments_data() -> List[Dict[str, str]]:
    """Return list of recent protocol adjustments."""
    return [
        {
            "date": "2024-03-15",
            "type": "Power Adjustment",
            "impact": "Increased treatment effectiveness",
            "details": "Increased power output from 100mW to 150mW based on tissue response"
        },
        {
            "date": "2024-03-10", 
            "type": "Duration Change",
            "impact": "Reduced treatment time while maintaining efficacy",
            "details": "Decreased session duration to 10 minutes per area based on healing progress"
        },
        {
            "date": "2024-03-05",
            "type": "Area Addition",
            "impact": "Better coverage of affected region",
            "details": "Added upper trapezius to treatment protocol to address referred pain"
        }
    ] 