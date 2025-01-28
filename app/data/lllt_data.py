"""
LLLT protocol data module.
"""
from typing import Dict, List, Any

def get_lllt_daily_data() -> List[Dict[str, Any]]:
    """Return daily LLLT protocol data."""
    return [
        {
            "name": "Crown Treatment",
            "duration": "120",
            "intensity": "High",
            "equipment": "LLLT Device - High Intensity",
            "steps": "- Position device at crown\n- Move in circular motion\n- Cover entire area"
        },
        {
            "name": "Temporal Treatment",
            "duration": "90",
            "intensity": "Medium",
            "equipment": "LLLT Device - Medium Intensity",
            "steps": "- Target temporal region\n- Use gentle pressure\n- Cover both sides"
        },
        {
            "name": "Occipital Treatment",
            "duration": "90",
            "intensity": "High",
            "equipment": "LLLT Device - High Intensity",
            "steps": "- Focus on occipital area\n- Move in small circles\n- Maintain contact"
        }
    ]

def get_weekly_schedule() -> List[Dict[str, Any]]:
    """Return weekly treatment schedule."""
    return [
        {
            "day": "Monday",
            "treatments": ["Crown", "Temporal"],
            "intensity": "High",
            "notes": "Focus on upper region"
        },
        {
            "day": "Tuesday",
            "treatments": ["Occipital"],
            "intensity": "Medium",
            "notes": "Gentle treatment day"
        },
        {
            "day": "Wednesday",
            "treatments": ["Crown", "Temporal", "Occipital"],
            "intensity": "High",
            "notes": "Full treatment session"
        }
    ]

def get_adjustments_data() -> List[Dict[str, Any]]:
    """Return recent protocol adjustments."""
    return [
        {
            "date": "2024-01-20",
            "change": "Increased crown treatment duration",
            "reason": "Better response observed",
            "notes": "Monitor for 2 weeks"
        }
    ]

def get_progress_metrics() -> Dict[str, Any]:
    """Return progress metrics."""
    return {
        "treatments_completed": 45,
        "total_duration": 2700,  # minutes
        "adherence_rate": 0.92,
        "reported_benefits": [
            "Improved circulation",
            "Better sleep quality"
        ]
    }

def get_supplement_data() -> Dict[str, List[Dict[str, Any]]]:
    """Return supplement schedule."""
    return {
        "Post-AM LLLT": [
            {
                "name": "Vitamin D3",
                "dosage": "5000 IU",
                "notes": "Take with breakfast"
            },
            {
                "name": "Omega-3",
                "dosage": "2000mg",
                "notes": "Take with food"
            }
        ],
        "Post-PM LLLT": [
            {
                "name": "Magnesium",
                "dosage": "400mg",
                "notes": "Take 2 hours after dinner"
            }
        ],
        "Pre-Bed": [
            {
                "name": "Zinc",
                "dosage": "15mg",
                "notes": "Take 30 mins before bed"
            }
        ]
    } 