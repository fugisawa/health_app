import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path

from app.utils.state import AppState
from app.data.data_loader import DataLoader
from app.utils.timer import parse_duration

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.data_loader = DataLoader()
    
    def test_load_phase_data(self):
        """Test loading phase data."""
        with self.assertRaises(FileNotFoundError):
            self.data_loader.load_phase_data(999, "nonexistent")
    
    def test_load_supplements_data(self):
        """Test loading supplements data."""
        with self.assertRaises(FileNotFoundError):
            self.data_loader.load_supplements_data()

class TestAppState(unittest.TestCase):
    def setUp(self):
        with patch('streamlit.session_state', MagicMock()) as mock_session_state:
            self.state = AppState()
            self.mock_session_state = mock_session_state
    
    def test_switch_protocol(self):
        """Test protocol switching."""
        self.state.switch_protocol("mobility")
        self.assertEqual(self.state.selected_protocol, "mobility")
        
        self.state.switch_protocol("lllt")
        self.assertEqual(self.state.selected_protocol, "lllt")
    
    def test_reset_session(self):
        """Test session reset."""
        self.state.session_start = datetime.now()
        self.state.completed_exercises = {"test"}
        self.state.current_exercise = {"name": "test"}
        
        self.state.reset_session()
        
        self.assertIsNone(self.state.session_start)
        self.assertEqual(len(self.state.completed_exercises), 0)
        self.assertIsNone(self.state.current_exercise)

class TestTimer(unittest.TestCase):
    def test_parse_duration(self):
        """Test duration string parsing."""
        test_cases = [
            ("60 seconds", 60),
            ("5 minutes", 300),
            ("3 mins/side", 360),
            ("10 reps", 50),
            ("2 sets x 30 seconds", 60),
            ("invalid", 60),  # default value
        ]
        
        for duration_str, expected in test_cases:
            with self.subTest(duration_str=duration_str):
                self.assertEqual(parse_duration(duration_str), expected)

def run_tests():
    unittest.main()

if __name__ == '__main__':
    run_tests() 