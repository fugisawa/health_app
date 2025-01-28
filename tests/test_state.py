"""Tests for application state management."""
import pytest
from datetime import datetime, timedelta

from app.utils.state import AppState

@pytest.fixture
def state():
    """Create a fresh AppState instance for each test."""
    return AppState()

def test_state_initialization(state):
    """Test that AppState is initialized with correct default values."""
    assert state.completed_count == 0
    assert state.total_count == 9
    assert state.active_exercise is None
    assert state.session_start is None
    assert state.session_end is None
    assert len(state.completed_exercises) == 0

def test_mark_complete(state):
    """Test marking an exercise as complete."""
    state.mark_complete("test_exercise")
    assert "test_exercise" in state.completed_exercises
    assert state.completed_count == 1

def test_start_exercise(state):
    """Test starting an exercise."""
    state.start_exercise("test_exercise")
    assert state.active_exercise == "test_exercise"
    assert state.session_start is not None

def test_complete_session(state):
    """Test completing a session."""
    state.start_exercise("test_exercise")
    state.complete_session()
    assert state.session_end is not None
    assert state.active_exercise is None

def test_reset_session(state):
    """Test resetting a session."""
    state.start_exercise("test_exercise")
    state.mark_complete("test_exercise")
    state.reset_session()
    assert state.completed_count == 0
    assert state.active_exercise is None
    assert len(state.completed_exercises) == 0
    assert state.session_start is None
    assert state.session_end is None

def test_completion_percentage(state):
    """Test completion percentage calculation."""
    assert state.completion_percentage == 0
    state.mark_complete("exercise1")
    assert state.completion_percentage == (1/9) * 100
    state.mark_complete("exercise2")
    assert state.completion_percentage == (2/9) * 100

def test_is_exercise_active(state):
    """Test checking if an exercise is active."""
    exercise = {"name": "test_exercise"}
    assert not state.is_exercise_active(exercise)
    state.start_exercise("test_exercise")
    assert state.is_exercise_active(exercise)

def test_is_exercise_completed(state):
    """Test checking if an exercise is completed."""
    exercise = {"name": "test_exercise"}
    assert not state.is_exercise_completed(exercise)
    state.mark_complete("test_exercise")
    assert state.is_exercise_completed(exercise)

def test_get_session_stats(state):
    """Test getting session statistics."""
    # Start session
    start_time = datetime.now()
    state.start_exercise("test_exercise")
    
    # Get stats immediately
    stats = state.get_session_stats()
    assert stats["completed_count"] == 0
    assert stats["active_exercise"] == "test_exercise"
    assert isinstance(stats["session_duration"], timedelta)
    
    # Complete exercise and check stats
    state.mark_complete("test_exercise")
    state.complete_session()
    stats = state.get_session_stats()
    assert stats["completed_count"] == 1
    assert stats["active_exercise"] is None
    assert isinstance(stats["session_duration"], timedelta) 