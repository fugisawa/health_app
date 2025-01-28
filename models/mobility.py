from dataclasses import dataclass
from typing import Dict, List
import pandas as pd
import os
from .base import BaseProtocol

class MobilityProtocol:
    def __init__(self, name: str, description: str, phases: dict, phase_details: dict, progress_metrics: list):
        self.name = name
        self.description = description
        self.phases = phases
        self.phase_details = phase_details
        self.progress_metrics = progress_metrics

    def to_dataframe(self) -> dict:
        dfs = {}
        for phase_name, sessions in self.phases.items():
            dfs[f'phase_{phase_name}'] = {}
            for session_name, exercises in sessions.items():
                # Validate exercise structure first
                validated = []
                for ex in exercises:
                    if not all(k in ex for k in ['Exercise', 'Sets/Reps/Duration', 'Equipment', 'Key Notes']):
                        raise ValueError(f"Invalid exercise format in {phase_name}/{session_name}")
                    validated.append({
                        'Exercise': ex.get('Exercise', ''),
                        'Duration': ex.get('Sets/Reps/Duration', ''),
                        'Equipment': ex.get('Equipment', 'None'),
                        'Notes': ex.get('Key Notes', '')
                    })
                dfs[f'phase_{phase_name}'][session_name] = pd.DataFrame(validated)
        return dfs

    def validate_data(self) -> bool:
        """Validate the mobility protocol data"""
        try:
            # Check required fields
            assert self.name, "Protocol name is required"
            assert self.description, "Protocol description is required"
            assert isinstance(self.phases, dict), "Phases must be a dictionary"
            assert isinstance(self.phase_details, dict), "Phase details must be a dictionary"
            
            # Validate exercises in each phase
            for phase_name, exercises in self.phases.items():
                if exercises:  # Only validate if there are exercises
                    for exercise in exercises:
                        assert isinstance(exercise, dict), f"Exercise in {phase_name} must be a dictionary"
                        assert "Exercise" in exercise, f"Exercise name is required in {phase_name}"
                        assert "Sets/Reps/Duration" in exercise, f"Sets/Reps/Duration is required in {phase_name}"
            
            return True
        except AssertionError as e:
            print(f"Validation error: {str(e)}")
            return False

    def save_to_csv(self, output_dir: str) -> None:
        """Save mobility data to CSV files"""
        dfs = self.to_dataframe()
        
        for name, df in dfs.items():
            df.to_csv(f"{output_dir}/{name}.csv", index=False)
            print(f"Saved {name}.csv") 