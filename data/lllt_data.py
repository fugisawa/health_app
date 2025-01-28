"""LLLT protocol data and schedules."""

from datetime import datetime
from typing import Dict, List, Any

def get_lllt_daily_data() -> Dict[str, List[Dict[str, Any]]]:
    """Return daily LLLT protocol data."""
    return {
        "Head": [
            {
                "name": "Crown and Temporal Treatment",
                "intensity": "High",
                "duration": "120 seconds",
                "equipment": "LLLT Device - High Intensity",
                "notes": "Focus on crown and temporal areas",
                "steps": [
                    "Position device at crown of head",
                    "Hold steady for 60 seconds",
                    "Move to right temporal area for 30 seconds",
                    "Move to left temporal area for 30 seconds"
                ]
            },
            {
                "name": "Occipital Treatment",
                "intensity": "Medium",
                "duration": "90 seconds",
                "equipment": "LLLT Device - Medium Intensity",
                "notes": "Focus on occipital area",
                "steps": [
                    "Position device at occipital area",
                    "Hold steady for full duration",
                    "Ensure good contact with scalp"
                ]
            }
        ],
        "Neck": [
            {
                "name": "Cervical Spine Treatment",
                "intensity": "High",
                "duration": "120 seconds",
                "equipment": "LLLT Device - High Intensity",
                "notes": "Focus on cervical spine",
                "steps": [
                    "Start at base of skull",
                    "Move slowly down cervical spine",
                    "Cover both sides of neck"
                ]
            },
            {
                "name": "Trapezius Treatment",
                "intensity": "Medium",
                "duration": "90 seconds",
                "equipment": "LLLT Device - Medium Intensity",
                "notes": "Focus on trapezius area",
                "steps": [
                    "Position on upper trapezius",
                    "Treat both sides equally",
                    "Maintain light pressure"
                ]
            }
        ],
        "Back": [
            {
                "name": "Thoracic Spine Treatment",
                "intensity": "High",
                "duration": "180 seconds",
                "equipment": "LLLT Device - High Intensity",
                "notes": "Focus on thoracic spine",
                "steps": [
                    "Start at top of thoracic spine",
                    "Move slowly down the spine",
                    "Cover adjacent muscle areas"
                ]
            },
            {
                "name": "Lumbar Treatment",
                "intensity": "Medium",
                "duration": "120 seconds",
                "equipment": "LLLT Device - Medium Intensity",
                "notes": "Focus on lumbar area",
                "steps": [
                    "Position at lumbar spine",
                    "Treat both sides of spine",
                    "Maintain consistent contact"
                ]
            }
        ]
    }

def get_weekly_schedule() -> List[Dict[str, str]]:
    """Return weekly LLLT treatment schedule."""
    return [
        {
            "name": "Monday",
            "frequency": "Full Session",
            "example_days": "Every Monday",
            "focus": "Head, Neck, Back - Full Protocol",
            "key_principle": "Complete coverage of all treatment areas"
        },
        {
            "name": "Tuesday",
            "frequency": "Rest Day",
            "example_days": "Every Tuesday",
            "focus": "Recovery",
            "key_principle": "Allow tissue response and adaptation"
        },
        {
            "name": "Wednesday",
            "frequency": "Focused Session",
            "example_days": "Every Wednesday",
            "focus": "Head, Neck - Focused Session",
            "key_principle": "Targeted treatment of priority areas"
        },
        {
            "name": "Thursday",
            "frequency": "Rest Day",
            "example_days": "Every Thursday",
            "focus": "Recovery",
            "key_principle": "Allow tissue response and adaptation"
        },
        {
            "name": "Friday",
            "frequency": "Full Session",
            "example_days": "Every Friday",
            "focus": "Head, Neck, Back - Full Protocol",
            "key_principle": "Complete coverage of all treatment areas"
        },
        {
            "name": "Saturday",
            "frequency": "Recovery Session",
            "example_days": "Every Saturday",
            "focus": "Back - Recovery Session",
            "key_principle": "Support weekend recovery"
        },
        {
            "name": "Sunday",
            "frequency": "Rest Day",
            "example_days": "Every Sunday",
            "focus": "Recovery",
            "key_principle": "Complete rest and adaptation"
        }
    ]

def get_adjustments_data() -> List[Dict[str, str]]:
    """Return recent protocol adjustments."""
    return [
        {
            "date": "2024-01-20",
            "type": "Intensity Increase",
            "impact": "Head and Neck treatments increased to high intensity",
            "details": "Improved response observed with higher intensity"
        },
        {
            "date": "2024-01-15",
            "type": "Duration Adjustment",
            "impact": "Extended back treatment duration",
            "details": "Better coverage of thoracic and lumbar areas"
        },
        {
            "date": "2024-01-10",
            "type": "Schedule Optimization",
            "impact": "Added Saturday recovery session",
            "details": "Enhanced recovery between training sessions"
        }
    ]

def get_progress_metrics() -> List[Dict[str, Any]]:
    """Return progress metrics for LLLT protocol."""
    return [
        {
            "name": "Treatment Consistency",
            "value": "4/4 sessions",
            "delta": "+1 session"
        },
        {
            "name": "Protocol Adherence",
            "value": "95%",
            "delta": "+5%"
        },
        {
            "name": "Recovery Time",
            "value": "24 hours",
            "delta": "-6 hours"
        }
    ]

def get_supplement_data() -> List[Dict[str, Any]]:
    """Return supplement schedule data"""
    return [
        {
            "Time": "Post-AM LLLT",
            "Supplements": "Collagen + vitamin C + silicium",
            "Purpose": "Skin/hair collagen synthesis."
        },
        {
            "Time": "Post-PM LLLT",
            "Supplements": "Omega-3s + magnesium",
            "Purpose": "Muscle recovery + anti-inflammatory."
        },
        {
            "Time": "Pre-Bed",
            "Supplements": "L-theanine + tryptophan",
            "Purpose": "Stress reduction + sleep."
        }
    ] 