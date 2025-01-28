"""Data loading utilities for the Health Protocol Dashboard."""
from pathlib import Path
from typing import Dict
import pandas as pd

class DataLoader:
    """Data loader for protocol data."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the data loader.
        
        Args:
            data_dir: Directory containing the data files
        """
        self.data_dir = Path(data_dir)
    
    def load_phase_data(self, phase: int, session: str) -> pd.DataFrame:
        """Load data for a specific phase and session.
        
        Args:
            phase: Phase number
            session: Session name (morning, lunch, evening)
            
        Returns:
            DataFrame containing the phase data
        """
        file_path = self.data_dir / f"phase{phase}_{session}_df.csv"
        try:
            return pd.read_csv(file_path)
        except FileNotFoundError:
            return pd.DataFrame()
    
    def load_supplements_data(self) -> pd.DataFrame:
        """Load supplements data.
        
        Returns:
            DataFrame containing supplements data
        """
        file_path = self.data_dir / "supplements_df.csv"
        try:
            return pd.read_csv(file_path)
        except FileNotFoundError:
            return pd.DataFrame()
    
    def load_all_mobility_data(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        """Load all mobility protocol data.
        
        Returns:
            Dictionary containing all mobility data organized by phase and session
        """
        data = {}
        phases = [1]  # Currently only phase 1
        sessions = ["morning", "lunch", "evening"]
        
        for phase in phases:
            phase_key = f"phase{phase}"
            data[phase_key] = {}
            
            for session in sessions:
                df = self.load_phase_data(phase, session)
                if not df.empty:
                    data[phase_key][session] = df
        
        return data
    
    def load_lllt_data(self) -> Dict[str, pd.DataFrame]:
        """Load LLLT protocol data.
        
        Returns:
            Dictionary containing LLLT data organized by type
        """
        data_files = {
            "lllt_days": "lllt_days_df.csv",
            "adjustments": "adjustments_df.csv",
            "weekly": "weekly_df.csv"
        }
        
        data = {}
        for key, filename in data_files.items():
            file_path = self.data_dir / filename
            try:
                data[key] = pd.read_csv(file_path)
            except FileNotFoundError:
                data[key] = pd.DataFrame()
        
        if all(df.empty for df in data.values()):
            raise FileNotFoundError("No LLLT data files found")
        
        return data 