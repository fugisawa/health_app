import pytest
from datetime import datetime, timedelta
from app.utils.state import AppState

def test_app_state_initialization():
    state = AppState()
    assert state.completed_exercises == set()
    assert state.current_exercise is None
    assert state.session_start is None

def test_exercise_completion():
    state = AppState()
    exercise = {'Exercise': 'Test Exercise'}
    
    # Test starting exercise
    state.start_exercise(exercise)
    assert state.current_exercise == exercise
    assert state.session_start is not None
    
    # Test completing exercise
    state.complete_exercise(exercise)
    assert exercise['Exercise'] in state.completed_exercises
    assert state.current_exercise is None

def test_session_stats():
    state = AppState()
    exercise = {'Exercise': 'Test Exercise'}
    
    # Test initial stats
    stats = state.get_session_stats()
    assert stats['completed_count'] == 0
    assert stats['session_duration'] is None
    assert stats['active_exercise'] is None
    
    # Test stats after starting exercise
    state.start_exercise(exercise)
    stats = state.get_session_stats()
    assert stats['completed_count'] == 0
    assert isinstance(stats['session_duration'], timedelta)
    assert stats['active_exercise'] == 'Test Exercise'
    
    # Test stats after completing exercise
    state.complete_exercise(exercise)
    stats = state.get_session_stats()
    assert stats['completed_count'] == 1
    assert isinstance(stats['session_duration'], timedelta)
    assert stats['active_exercise'] is None

def test_reset_session():
    state = AppState()
    exercise = {'Exercise': 'Test Exercise'}
    
    state.start_exercise(exercise)
    state.complete_exercise(exercise)
    
    state.reset_session()
    assert state.completed_exercises == set()
    assert state.current_exercise is None
    assert state.session_start is None 