import unittest
import pandas as pd
import os
from data.data_manager import DataManager

class TestDataLoading(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager("data/raw")
    
    def test_csv_files_exist(self):
        """Test if all required CSV files are created"""
        expected_files = [
            'lllt_daily.csv',
            'lllt_supplements.csv',
            'mobility_program.csv'
        ]
        
        for filename in expected_files:
            filepath = os.path.join(self.data_manager.data_dir, filename)
            self.assertTrue(os.path.exists(filepath), f"Missing file: {filename}")
    
    def test_data_integrity(self):
        """Test if loaded data maintains integrity"""
        df = self.data_manager.load_from_csv('lllt_daily.csv')
        required_columns = ['Days', 'Day Type', 'Session']
        for col in required_columns:
            self.assertIn(col, df.columns)

if __name__ == '__main__':
    unittest.main() 