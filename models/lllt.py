from dataclasses import dataclass
from typing import List, Dict, Any
import pandas as pd
import os
from .base import BaseProtocol

@dataclass
class LLLTProtocol(BaseProtocol):
    """LLLT (Low-Level Light Therapy) protocol implementation"""
    daily_schedule: List[Dict[str, Any]]
    supplement_schedule: List[Dict[str, Any]]
    weekly_schedule: List[Dict[str, Any]]
    
    def to_dataframe(self) -> Dict[str, pd.DataFrame]:
        """Convert LLLT data to DataFrames"""
        return {
            'daily': pd.DataFrame(self.daily_schedule),
            'supplements': pd.DataFrame(self.supplement_schedule),
            'weekly': pd.DataFrame(self.weekly_schedule)
        }
    
    def validate(self) -> bool:
        """Validate LLLT protocol data"""
        validations = {
            'daily': ['Days', 'Day Type', 'Session', 'Device Mode'],
            'supplements': ['Time', 'Supplements', 'Purpose'],
            'weekly': ['Day Type', 'Frequency', 'Focus']
        }
        
        dfs = self.to_dataframe()
        return all(
            all(field in df.columns for field in required_fields)
            for df_name, required_fields in validations.items()
            if df_name in dfs
        )
    
    def save_to_csv(self, output_dir: str) -> None:
        """Save LLLT data to CSV files"""
        dfs = self.to_dataframe()
        for name, df in dfs.items():
            df.to_csv(os.path.join(output_dir, f'lllt_{name}.csv'), index=False) 