"""Tests for rep counter utilities."""
import pytest
import streamlit as st
from unittest.mock import patch

from app.utils.rep_counter import (
    init_rep_counter,
    start_rep_counter,
    increment_rep,
    complete_set,
    get_rep_display,
    is_set_complete,
    is_exercise_complete,
    parse_reps
)

@pytest.fixture
def mock_session_state():
    """Create a mock session state for testing."""
    with patch.object(st, 'session_state', {}) as mock_state:
        init_rep_counter()
        yield mock_state

def test_init_rep_counter(mock_session_state):
    """Test rep counter initialization."""
    assert mock_session_state.current_reps == 0
    assert mock_session_state.target_reps == 0
    assert mock_session_state.current_set == 1
    assert mock_session_state.target_sets == 1

def test_start_rep_counter(mock_session_state):
    """Test starting a rep counter."""
    start_rep_counter(10, 3)
    assert mock_session_state.current_reps == 0
    assert mock_session_state.target_reps == 10
    assert mock_session_state.current_set == 1
    assert mock_session_state.target_sets == 3

def test_increment_rep(mock_session_state):
    """Test incrementing reps."""
    start_rep_counter(10)
    
    # Increment within target
    for i in range(5):
        increment_rep()
        assert mock_session_state.current_reps == i + 1
    
    # Try to increment beyond target
    for _ in range(10):
        increment_rep()
    assert mock_session_state.current_reps == 10

def test_complete_set(mock_session_state):
    """Test completing sets."""
    start_rep_counter(10, 3)
    
    # Complete first set
    for _ in range(10):
        increment_rep()
    complete_set()
    assert mock_session_state.current_set == 2
    assert mock_session_state.current_reps == 0
    
    # Complete second set
    for _ in range(10):
        increment_rep()
    complete_set()
    assert mock_session_state.current_set == 3
    assert mock_session_state.current_reps == 0
    
    # Try to complete beyond target sets
    for _ in range(10):
        increment_rep()
    complete_set()
    assert mock_session_state.current_set == 3

def test_get_rep_display(mock_session_state):
    """Test rep counter display."""
    # Single set
    start_rep_counter(10)
    display, progress = get_rep_display()
    assert display == "Rep 0/10"
    assert progress == 0
    
    # Multiple sets
    start_rep_counter(10, 3)
    display, progress = get_rep_display()
    assert display == "Set 1/3 - Rep 0/10"
    assert progress == 0
    
    # Progress calculation
    for _ in range(5):
        increment_rep()
    display, progress = get_rep_display()
    assert progress == (5 / (10 * 3)) * 100

def test_is_set_complete(mock_session_state):
    """Test checking if a set is complete."""
    start_rep_counter(10)
    assert not is_set_complete()
    
    for _ in range(9):
        increment_rep()
    assert not is_set_complete()
    
    increment_rep()
    assert is_set_complete()

def test_is_exercise_complete(mock_session_state):
    """Test checking if an exercise is complete."""
    start_rep_counter(10, 2)
    assert not is_exercise_complete()
    
    # Complete first set
    for _ in range(10):
        increment_rep()
    complete_set()
    assert not is_exercise_complete()
    
    # Complete second set
    for _ in range(10):
        increment_rep()
    assert is_exercise_complete()

def test_parse_reps():
    """Test parsing rep strings."""
    # Single set
    reps, sets = parse_reps("10 reps")
    assert reps == 10
    assert sets == 1
    
    # Multiple sets
    reps, sets = parse_reps("3x10 reps")
    assert reps == 10
    assert sets == 3
    
    # Invalid formats should raise ValueError
    with pytest.raises(ValueError):
        parse_reps("invalid") 