"""Mobility protocol data and schedules."""

import pandas as pd
from typing import Dict, List, Any
from bs4 import BeautifulSoup
import os

def load_protocol_html(protocol_type: str = "foundation", day_type: str = "lllt_days") -> str:
    """Load protocol HTML file."""
    file_path = f"data/protocols/{protocol_type}_{day_type}.html"
    with open(file_path, 'r') as f:
        return f.read()

def parse_protocol_html(html_content: str) -> Dict[str, Any]:
    """Parse protocol HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get all tables
    tables = soup.find_all('table')
    
    protocol_data = {
        "supplements": [],
        "exercises": []
    }
    
    for table in tables:
        rows = table.find_all('tr')[1:]  # Skip header row
        
        # Check table type by first column header
        header = table.find('th').text.strip()
        
        if "Time" in header:  # Supplements table
            for row in rows:
                cols = row.find_all('td')
                protocol_data["supplements"].append({
                    "time": cols[0].text.strip(),
                    "supplements": cols[1].text.strip(),
                    "purpose": cols[2].text.strip()
                })
        elif "Exercise" in header:  # Exercises table
            for row in rows:
                cols = row.find_all('td')
                protocol_data["exercises"].append({
                    "name": cols[0].text.strip(),
                    "sets_reps": cols[1].text.strip(),
                    "equipment": cols[2].text.strip(),
                    "notes": cols[3].text.strip()
                })
    
    return protocol_data

def get_current_protocol() -> Dict[str, Any]:
    """Get current protocol data."""
    html_content = load_protocol_html()
    return parse_protocol_html(html_content)

def get_phase_details(phase_name: str) -> Dict[str, Any]:
    """Get details for a specific phase from the CSV data."""
    df = pd.read_csv("data/mobility_program.csv")
    phase_data = df[df['Phase'] == phase_name].iloc[0]
    
    # Get current protocol exercises
    protocol = get_current_protocol()
    
    return {
        "description": phase_data['Description'],
        "objectives": [obj.strip() for obj in phase_data['Objectives'].split(',')],
        "recommendations": [rec.strip() for rec in phase_data['Recommendations'].split(',')],
        "duration": phase_data['Duration'],
        "frequency": phase_data['Frequency'],
        "exercises": protocol["exercises"]  # Use actual protocol exercises
    }

def get_current_phase() -> str:
    """Get the current phase name (in practice, this would be determined by progress)."""
    return "Phase 1: Fundamental Mobility"  # Default to Phase 1

def get_supplements() -> List[Dict[str, str]]:
    """Get current protocol supplements."""
    protocol = get_current_protocol()
    return protocol["supplements"]

def get_exercise_details(exercise_name: str) -> Dict[str, Any]:
    """Get details for a specific exercise."""
    exercise_details = {
        # Phase 1 exercises
        "Hip Mobility": {
            "sets_reps": "3 sets x 10 reps each side",
            "equipment": "None",
            "notes": "Focus on controlled movement",
            "duration": "60 seconds"
        },
        "Shoulder Mobility": {
            "sets_reps": "3 sets x 8 reps each side",
            "equipment": "Resistance band",
            "notes": "Full range of motion",
            "duration": "60 seconds"
        },
        "Spine Mobility": {
            "sets_reps": "2 sets x 10 reps",
            "equipment": "Yoga mat",
            "notes": "Keep movements smooth",
            "duration": "60 seconds"
        },
        # Phase 2 exercises
        "Plank with Rotation": {
            "sets_reps": "3 sets x 30 seconds",
            "equipment": "Yoga mat",
            "notes": "Keep core engaged",
            "duration": "30 seconds"
        },
        "Bird Dog": {
            "sets_reps": "3 sets x 10 each side",
            "equipment": "Yoga mat",
            "notes": "Maintain alignment",
            "duration": "45 seconds"
        },
        "Dead Bug": {
            "sets_reps": "3 sets x 10 reps",
            "equipment": "Yoga mat",
            "notes": "Press lower back down",
            "duration": "45 seconds"
        },
        # Phase 3 exercises
        "Yoga Flow": {
            "sets_reps": "2 sets x 5 minutes",
            "equipment": "Yoga mat",
            "notes": "Flow with breath",
            "duration": "300 seconds"
        },
        "Animal Flow": {
            "sets_reps": "2 sets x 3 minutes",
            "equipment": "None",
            "notes": "Smooth transitions",
            "duration": "180 seconds"
        },
        "Mobility Sequence": {
            "sets_reps": "1 set x 10 minutes",
            "equipment": "None",
            "notes": "Combine movements",
            "duration": "600 seconds"
        }
    }
    return exercise_details.get(exercise_name, {})

def get_mobility_phases() -> Dict[str, List[Dict[str, Any]]]:
    """Return mobility exercise phases."""
    return {
        "Phase 1: Fundamental Mobility": [
            # Hip Mobility Section
            {
                "name": "Hip Internal/External Rotation",
                "sets_reps": "3 sets x 10 reps each side",
                "equipment": "None",
                "notes": "Focus on controlled rotation",
                "duration": "60 seconds"
            },
            {
                "name": "Hip Flexor Stretch",
                "sets_reps": "3 sets x 30 seconds each side",
                "equipment": "Yoga mat",
                "notes": "Keep spine neutral",
                "duration": "60 seconds"
            },
            {
                "name": "90/90 Hip Switches",
                "sets_reps": "2 sets x 10 reps each side",
                "equipment": "None",
                "notes": "Control the movement",
                "duration": "90 seconds"
            },
            {
                "name": "Cossack Squats",
                "sets_reps": "3 sets x 8 reps each side",
                "equipment": "None",
                "notes": "Keep heel down",
                "duration": "60 seconds"
            },
            # Shoulder Mobility Section
            {
                "name": "Shoulder CARs",
                "sets_reps": "2 sets x 5 each direction",
                "equipment": "None",
                "notes": "Full range controlled movement",
                "duration": "60 seconds"
            },
            {
                "name": "Wall Slides",
                "sets_reps": "3 sets x 10 reps",
                "equipment": "Wall",
                "notes": "Maintain contact with wall",
                "duration": "45 seconds"
            },
            {
                "name": "Band Pull Aparts",
                "sets_reps": "3 sets x 15 reps",
                "equipment": "Resistance band",
                "notes": "Squeeze shoulder blades",
                "duration": "45 seconds"
            },
            {
                "name": "Thoracic Bridge",
                "sets_reps": "2 sets x 30 seconds",
                "equipment": "Yoga mat",
                "notes": "Focus on thoracic extension",
                "duration": "60 seconds"
            },
            # Spine/Core Section
            {
                "name": "Cat-Cow Flow",
                "sets_reps": "2 sets x 10 cycles",
                "equipment": "Yoga mat",
                "notes": "Coordinate with breath",
                "duration": "60 seconds"
            },
            {
                "name": "Thoracic Rotations",
                "sets_reps": "2 sets x 8 each side",
                "equipment": "None",
                "notes": "Keep hips stable",
                "duration": "45 seconds"
            },
            {
                "name": "Bird Dog",
                "sets_reps": "3 sets x 8 each side",
                "equipment": "Yoga mat",
                "notes": "Maintain neutral spine",
                "duration": "60 seconds"
            },
            {
                "name": "Dead Bug",
                "sets_reps": "3 sets x 10 reps",
                "equipment": "Yoga mat",
                "notes": "Keep low back pressed down",
                "duration": "45 seconds"
            }
        ],
        "Phase 2: Strength & Stability": [
            # Strength Section
            {
                "name": "Goblet Squats",
                "sets_reps": "3 sets x 10 reps",
                "equipment": "Kettlebell",
                "notes": "Keep chest up",
                "duration": "60 seconds"
            },
            {
                "name": "Single-Leg RDL",
                "sets_reps": "3 sets x 8 each side",
                "equipment": "Kettlebell",
                "notes": "Hinge at hips",
                "duration": "90 seconds"
            },
            {
                "name": "Push-Up with Rotation",
                "sets_reps": "3 sets x 6 each side",
                "equipment": "None",
                "notes": "Control the rotation",
                "duration": "60 seconds"
            },
            {
                "name": "Racked Carry",
                "sets_reps": "3 sets x 30 seconds each side",
                "equipment": "Kettlebell",
                "notes": "Stay tall",
                "duration": "60 seconds"
            },
            # Stability Section
            {
                "name": "Turkish Get-Up Progression",
                "sets_reps": "2 sets x 3 each side",
                "equipment": "Light weight",
                "notes": "Focus on each position",
                "duration": "120 seconds"
            },
            {
                "name": "Pallof Press",
                "sets_reps": "3 sets x 10 each side",
                "equipment": "Resistance band",
                "notes": "Resist rotation",
                "duration": "60 seconds"
            },
            {
                "name": "Copenhagen Plank",
                "sets_reps": "3 sets x 20 seconds each side",
                "equipment": "Bench",
                "notes": "Keep hips level",
                "duration": "60 seconds"
            },
            {
                "name": "Bear Crawl",
                "sets_reps": "3 sets x 30 seconds",
                "equipment": "None",
                "notes": "Maintain position",
                "duration": "45 seconds"
            },
            # Integration Section
            {
                "name": "Flow Sequence 1",
                "sets_reps": "2 sets x 1 minute",
                "equipment": "None",
                "notes": "Smooth transitions",
                "duration": "120 seconds"
            },
            {
                "name": "Lateral Lunge to Balance",
                "sets_reps": "3 sets x 6 each side",
                "equipment": "None",
                "notes": "Control the balance",
                "duration": "90 seconds"
            },
            {
                "name": "Rolling Pattern",
                "sets_reps": "2 sets x 5 each side",
                "equipment": "Yoga mat",
                "notes": "Segmental control",
                "duration": "60 seconds"
            },
            {
                "name": "Crawling Complex",
                "sets_reps": "2 sets x 1 minute",
                "equipment": "None",
                "notes": "Coordinate movement",
                "duration": "60 seconds"
            }
        ],
        "Phase 3: Movement Integration": [
            # Movement Flow Section
            {
                "name": "Sun Salutation Flow",
                "sets_reps": "3 rounds",
                "equipment": "Yoga mat",
                "notes": "Connect with breath",
                "duration": "180 seconds"
            },
            {
                "name": "Animal Flow Transitions",
                "sets_reps": "2 sets x 2 minutes",
                "equipment": "None",
                "notes": "Fluid movement",
                "duration": "240 seconds"
            },
            {
                "name": "Ground Flow Sequence",
                "sets_reps": "2 sets x 90 seconds",
                "equipment": "None",
                "notes": "Creative transitions",
                "duration": "180 seconds"
            },
            {
                "name": "Movement Exploration",
                "sets_reps": "2 sets x 2 minutes",
                "equipment": "None",
                "notes": "Free movement practice",
                "duration": "240 seconds"
            },
            # Complex Patterns
            {
                "name": "Get-Up Flow",
                "sets_reps": "3 sets each side",
                "equipment": "Light weight",
                "notes": "Connect positions",
                "duration": "180 seconds"
            },
            {
                "name": "Locomotion Complex",
                "sets_reps": "2 sets x 2 minutes",
                "equipment": "None",
                "notes": "Varied patterns",
                "duration": "240 seconds"
            },
            {
                "name": "Balance Flow",
                "sets_reps": "2 sets x 90 seconds",
                "equipment": "None",
                "notes": "Control transitions",
                "duration": "180 seconds"
            },
            {
                "name": "Handstand Progression",
                "sets_reps": "4 sets x 30 seconds",
                "equipment": "Wall",
                "notes": "Build shoulder stability",
                "duration": "120 seconds"
            },
            # Integration
            {
                "name": "Flow Combination 1",
                "sets_reps": "2 rounds",
                "equipment": "None",
                "notes": "Link movements",
                "duration": "300 seconds"
            },
            {
                "name": "Flow Combination 2",
                "sets_reps": "2 rounds",
                "equipment": "None",
                "notes": "Express movement",
                "duration": "300 seconds"
            },
            {
                "name": "Movement Meditation",
                "sets_reps": "1 set x 5 minutes",
                "equipment": "None",
                "notes": "Mindful practice",
                "duration": "300 seconds"
            },
            {
                "name": "Cooldown Flow",
                "sets_reps": "1 round",
                "equipment": "Yoga mat",
                "notes": "Gentle transitions",
                "duration": "180 seconds"
            }
        ]
    }

def get_progress_metrics() -> pd.DataFrame:
    """Return progress metrics for mobility protocol."""
    metrics = [
        {
            "Metric": "Consistency",
            "Current": "5/6 sessions this week",
            "Target": "6 sessions per week",
            "Progress": 83
        },
        {
            "Metric": "Range of Motion",
            "Current": "Significant improvement",
            "Target": "Full range in all movements",
            "Progress": 75
        },
        {
            "Metric": "Practice Time",
            "Current": "45 minutes per session",
            "Target": "60 minutes per session",
            "Progress": 75
        }
    ]
    return pd.DataFrame(metrics)

def get_key_adjustments() -> pd.DataFrame:
    """Return key adjustments in the mobility protocol."""
    adjustments = [
        {
            "Date": "2024-01-25",
            "Type": "Exercise Progression",
            "Description": "Added advanced phase of integrated movements",
            "Impact": "Increased complexity and challenge"
        },
        {
            "Date": "2024-01-20",
            "Type": "Volume Adjustment",
            "Description": "Increased sets in fundamental exercises",
            "Impact": "Better strength and control development"
        },
        {
            "Date": "2024-01-15",
            "Type": "Sequence Modification",
            "Description": "Reorganized exercise order",
            "Impact": "More efficient movement flow"
        }
    ]
    return pd.DataFrame(adjustments)

def get_mobility_dashboard_data() -> Dict[str, pd.DataFrame]:
    """Return all dashboard data in DataFrame format."""
    phases = get_mobility_phases()
    
    # Convert phases to DataFrames
    phase_dfs = {}
    for phase_name, exercises in phases.items():
        phase_dfs[phase_name] = pd.DataFrame(exercises)
    
    # Add progress metrics and adjustments
    dashboard_data = {
        **phase_dfs,
        "progress_metrics": get_progress_metrics(),
        "key_adjustments": get_key_adjustments()
    }
    
    return dashboard_data 