import pandas as pd
from typing import Dict
import os

class DataExporter:
    @staticmethod
    def export_to_excel(data_dict: Dict[str, pd.DataFrame], output_path: str) -> None:
        """Export multiple DataFrames to Excel sheets"""
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for sheet_name, df in data_dict.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    @staticmethod
    def export_to_csv(data_dict: Dict[str, pd.DataFrame], output_dir: str) -> None:
        """Export multiple DataFrames to CSV files"""
        os.makedirs(output_dir, exist_ok=True)
        for name, df in data_dict.items():
            df.to_csv(os.path.join(output_dir, f'{name}.csv'), index=False) 