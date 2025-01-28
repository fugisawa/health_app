"""Tests for timer utilities."""
import pytest
from datetime import datetime, timedelta
import streamlit as st
from unittest.mock import patch

from app.utils.timer import (
    init_timer,
    start_timer,
    pause_timer,
    resume_timer,
    update_timer,
    get_timer_display,
    is_timer_active,
    is_timer_paused
)

@pytest.fixture
def mock_session_state():
    """Create a mock session state for testing."""
    with patch.object(st, 'session_state', {}) as mock_state:
        init_timer()
        yield mock_state

def test_init_timer(mock_session_state):
    """Test timer initialization."""
    assert mock_session_state.timer_start is None
    assert mock_session_state.timer_duration == 0
    assert not mock_session_state.timer_paused
    assert mock_session_state.pause_time is None

def test_start_timer(mock_session_state):
    """Test starting a timer."""
    start_timer(60)
    assert mock_session_state.timer_start is not None
    assert mock_session_state.timer_duration == 60
    assert not mock_session_state.timer_paused
    assert mock_session_state.pause_time is None

def test_pause_resume_timer(mock_session_state):
    """Test pausing and resuming a timer."""
    # Start timer
    start_timer(60)
    original_start = mock_session_state.timer_start
    
    # Pause timer
    pause_timer()
    assert mock_session_state.timer_paused
    assert mock_session_state.pause_time is not None
    
    # Resume timer
    resume_timer()
    assert not mock_session_state.timer_paused
    assert mock_session_state.pause_time is None
    assert mock_session_state.timer_start > original_start

def test_update_timer(mock_session_state):
    """Test updating timer progress."""
    # No timer active
    assert update_timer() is None
    
    # Start timer
    start_timer(60)
    progress = update_timer()
    assert 0 <= progress <= 100
    
    # Force complete
    progress = update_timer(force_complete=True)
    assert progress == 100
    assert mock_session_state.timer_start is None
    assert mock_session_state.timer_duration == 0

def test_get_timer_display(mock_session_state):
    """Test timer display formatting."""
    # No timer active
    assert get_timer_display() == "00:00"
    
    # Start timer
    start_timer(65)  # 1:05
    display = get_timer_display()
    assert len(display) == 5  # Format: MM:SS
    assert display.count(":") == 1
    minutes, seconds = display.split(":")
    assert 0 <= int(minutes) <= 99
    assert 0 <= int(seconds) <= 59

def test_is_timer_active(mock_session_state):
    """Test checking if timer is active."""
    assert not is_timer_active()
    start_timer(60)
    assert is_timer_active()
    update_timer(force_complete=True)
    assert not is_timer_active()

def test_is_timer_paused(mock_session_state):
    """Test checking if timer is paused."""
    assert not is_timer_paused()
    start_timer(60)
    assert not is_timer_paused()
    pause_timer()
    assert is_timer_paused()
    resume_timer()
    assert not is_timer_paused() 