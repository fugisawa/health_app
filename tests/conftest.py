"""Test configuration and shared fixtures."""
import pytest
import streamlit as st
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_streamlit():
    """Mock Streamlit functions for testing."""
    with patch.object(st, 'session_state', {}) as mock_state:
        yield mock_state

@pytest.fixture
def sample_exercise():
    """Create a sample exercise for testing."""
    return {
        "name": "Test Exercise",
        "duration": "120 seconds",
        "intensity": "Medium",
        "equipment": "None",
        "notes": "Test notes",
        "steps": [
            "Step 1: Do this",
            "Step 2: Do that"
        ],
        "demo_link": "https://example.com/demo"
    }

@pytest.fixture
def sample_rep_exercise():
    """Create a sample exercise with reps for testing."""
    return {
        "name": "Test Rep Exercise",
        "reps": "3x10 reps",
        "equipment": "Dumbbells",
        "notes": "Test notes",
        "steps": [
            "Step 1: Do this",
            "Step 2: Do that"
        ],
        "demo_link": "https://example.com/demo"
    }

@pytest.fixture
def sample_lllt_data():
    """Create sample LLLT protocol data for testing."""
    return {
        "Head": [
            {
                "name": "Test Treatment",
                "duration": "120 seconds",
                "intensity": "High",
                "notes": "Test notes"
            }
        ]
    }

@pytest.fixture
def sample_mobility_data():
    """Create sample mobility protocol data for testing."""
    return {
        "morning": [
            {
                "name": "Test Exercise",
                "reps": "3x10 reps",
                "equipment": "None",
                "notes": "Test notes"
            }
        ]
    } 