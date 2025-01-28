import pandas as pd
import os
from typing import Dict, Any

class DataManager:
    """Manages data storage and retrieval for health protocols"""
    
    def __init__(self, data_dir: str = "data/raw"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def save_to_csv(self, data: Dict[str, pd.DataFrame]) -> None:
        """Save all DataFrames to CSV files"""
        for name, df in data.items():
            filename = f"{name.lower().replace(' ', '_')}.csv"
            filepath = os.path.join(self.data_dir, filename)
            df.to_csv(filepath, index=False)
            print(f"Saved {filename}")
    
    def load_from_csv(self, filename: str) -> pd.DataFrame:
        """Load DataFrame from CSV file"""
        filepath = os.path.join(self.data_dir, filename)
        return pd.read_csv(filepath) 