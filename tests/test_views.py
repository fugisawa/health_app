"""Tests for the application views."""
import pytest
import streamlit as st
from unittest.mock import Mock, patch

from app.views.lllt import LLLTView
from app.views.mobility import MobilityView

def test_lllt_view_initialization(mock_streamlit, sample_lllt_data):
    """Test LLLT view initialization."""
    with patch('app.data.lllt_data.get_lllt_daily_data') as mock_get_data:
        mock_get_data.return_value = sample_lllt_data
        
        view = LLLTView()
        assert view.daily_data == sample_lllt_data

def test_lllt_view_render(mock_streamlit, sample_lllt_data):
    """Test LLLT view rendering."""
    with patch('app.data.lllt_data.get_lllt_daily_data') as mock_get_data, \
         patch('streamlit.tabs') as mock_tabs:
        
        mock_get_data.return_value = sample_lllt_data
        mock_tabs.return_value = [Mock(), Mock(), Mock()]
        
        view = LLLTView()
        view.render()
        
        # Verify tabs were created
        mock_tabs.assert_called_with(['Daily Protocol', 'Weekly Schedule', 'Progress'])

def test_lllt_view_start_treatment(mock_streamlit, sample_lllt_data):
    """Test starting LLLT treatment."""
    with patch('app.data.lllt_data.get_lllt_daily_data') as mock_get_data, \
         patch('app.utils.timer.start_timer') as mock_start_timer:
        
        mock_get_data.return_value = sample_lllt_data
        
        view = LLLTView()
        view._start_treatment('Head')
        
        # Verify timer was started
        mock_start_timer.assert_called_once()
        
        # Verify session state was updated
        assert st.session_state.active_treatment == 'Head'

def test_mobility_view_initialization(mock_streamlit, sample_mobility_data):
    """Test Mobility view initialization."""
    with patch('app.data.mobility_data.get_mobility_phases') as mock_get_data:
        mock_get_data.return_value = sample_mobility_data
        
        view = MobilityView()
        assert view.exercises == sample_mobility_data

def test_mobility_view_render(mock_streamlit, sample_mobility_data):
    """Test Mobility view rendering."""
    with patch('app.data.mobility_data.get_mobility_phases') as mock_get_data, \
         patch('streamlit.tabs') as mock_tabs:
        
        mock_get_data.return_value = sample_mobility_data
        mock_tabs.return_value = [Mock(), Mock(), Mock()]
        
        view = MobilityView()
        view.render()
        
        # Verify tabs were created
        mock_tabs.assert_called_with(['Exercises', 'Progress', 'History'])

def test_mobility_view_start_exercise(mock_streamlit, sample_mobility_data):
    """Test starting mobility exercise."""
    with patch('app.data.mobility_data.get_mobility_phases') as mock_get_data, \
         patch('app.utils.timer.start_timer') as mock_start_timer, \
         patch('app.utils.rep_counter.start_rep_counter') as mock_start_rep_counter:
        
        mock_get_data.return_value = sample_mobility_data
        
        view = MobilityView()
        
        # Test starting timed exercise
        exercise = {'name': 'Test Exercise', 'duration': '60 seconds'}
        view._start_exercise(exercise)
        mock_start_timer.assert_called_once()
        
        # Test starting rep exercise
        exercise = {'name': 'Test Exercise', 'reps': '10 reps x 3 sets'}
        view._start_exercise(exercise)
        mock_start_rep_counter.assert_called_once()

def test_mobility_view_complete_exercise(mock_streamlit, sample_mobility_data):
    """Test completing mobility exercise."""
    with patch('app.data.mobility_data.get_mobility_phases') as mock_get_data:
        mock_get_data.return_value = sample_mobility_data
        
        view = MobilityView()
        exercise = {'name': 'Test Exercise'}
        
        view._complete_exercise(exercise)
        
        # Verify exercise was marked as complete
        assert exercise['name'] in st.session_state.completed_exercises

def test_mobility_view_session_progress(mock_streamlit, sample_mobility_data):
    """Test mobility session progress calculation."""
    with patch('app.data.mobility_data.get_mobility_phases') as mock_get_data:
        mock_get_data.return_value = sample_mobility_data
        
        view = MobilityView()
        
        # Complete some exercises
        st.session_state.completed_exercises = set(['Exercise 1', 'Exercise 2'])
        
        progress = view._get_session_progress()
        assert isinstance(progress, float)
        assert 0 <= progress <= 100 