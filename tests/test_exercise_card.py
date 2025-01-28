"""Tests for the exercise card component."""
import pytest
import streamlit as st
from unittest.mock import Mock, patch

from app.components.exercise_card import ExerciseCard

def test_render_basic_exercise(mock_streamlit, sample_exercise):
    """Test rendering a basic exercise card."""
    on_start = Mock()
    on_complete = Mock()
    
    with patch('streamlit.container'), \
         patch('streamlit.columns') as mock_cols, \
         patch('streamlit.markdown') as mock_markdown, \
         patch('streamlit.tabs') as mock_tabs, \
         patch('streamlit.button') as mock_button:
        
        # Mock column objects
        mock_cols.return_value = [Mock(), Mock()]
        
        # Mock tab objects
        mock_tabs.return_value = [Mock(), Mock()]
        
        # Render exercise card
        ExerciseCard.render(
            exercise=sample_exercise,
            on_start=on_start,
            on_complete=on_complete
        )
        
        # Verify title was rendered
        mock_markdown.assert_any_call(
            f"""
                <div class="exercise-title">
                    {sample_exercise['name']}
                </div>
            """,
            unsafe_allow_html=True
        )
        
        # Verify exercise details were rendered
        mock_markdown.assert_any_call(f"⏱️ **Duration:** {sample_exercise['duration']}")
        mock_markdown.assert_any_call(f"💪 **Intensity:** {sample_exercise['intensity']}")
        mock_markdown.assert_any_call(f"🔧 **Equipment:** {sample_exercise['equipment']}")
        
        # Verify steps were rendered
        for step in sample_exercise['steps']:
            mock_markdown.assert_any_call(step)
        
        # Verify demo link was rendered
        mock_markdown.assert_any_call(f"[Watch Demo]({sample_exercise['demo_link']})")
        
        # Verify start button was rendered
        mock_button.assert_any_call("Start", key=f"start_{sample_exercise['name']}")

def test_render_active_exercise(mock_streamlit, sample_exercise):
    """Test rendering an active exercise card."""
    on_start = Mock()
    on_complete = Mock()
    
    with patch('streamlit.container'), \
         patch('streamlit.columns') as mock_cols, \
         patch('streamlit.markdown') as mock_markdown, \
         patch('streamlit.tabs'), \
         patch('streamlit.button') as mock_button, \
         patch('streamlit.progress') as mock_progress:
        
        # Mock column objects
        mock_cols.return_value = [Mock(), Mock(), Mock()]
        
        # Render active exercise card
        ExerciseCard.render(
            exercise=sample_exercise,
            on_start=on_start,
            on_complete=on_complete,
            is_active=True
        )
        
        # Verify in progress status was rendered
        mock_markdown.assert_any_call("🔄 In Progress")
        
        # Verify complete button was rendered
        mock_button.assert_any_call(
            "Complete",
            key=f"complete_{sample_exercise['name']}"
        )
        
        # Verify progress bar was rendered
        mock_progress.assert_called()

def test_render_completed_exercise(mock_streamlit, sample_exercise):
    """Test rendering a completed exercise card."""
    on_start = Mock()
    on_complete = Mock()
    
    with patch('streamlit.container'), \
         patch('streamlit.columns') as mock_cols, \
         patch('streamlit.markdown') as mock_markdown, \
         patch('streamlit.tabs'):
        
        # Mock column objects
        mock_cols.return_value = [Mock(), Mock()]
        
        # Render completed exercise card
        ExerciseCard.render(
            exercise=sample_exercise,
            on_start=on_start,
            on_complete=on_complete,
            is_completed=True
        )
        
        # Verify completed status was rendered
        mock_markdown.assert_any_call("✅ Complete")

def test_render_rep_exercise(mock_streamlit, sample_rep_exercise):
    """Test rendering an exercise card with reps."""
    on_start = Mock()
    on_complete = Mock()
    
    with patch('streamlit.container'), \
         patch('streamlit.columns') as mock_cols, \
         patch('streamlit.markdown') as mock_markdown, \
         patch('streamlit.tabs'), \
         patch('streamlit.button') as mock_button:
        
        # Mock column objects
        mock_cols.return_value = [Mock(), Mock()]
        
        # Render exercise card
        ExerciseCard.render(
            exercise=sample_rep_exercise,
            on_start=on_start,
            on_complete=on_complete
        )
        
        # Verify rep information was rendered
        mock_markdown.assert_any_call(f"🔄 **Reps:** {sample_rep_exercise['reps']}")
        
        # Verify equipment was rendered
        mock_markdown.assert_any_call(f"🔧 **Equipment:** {sample_rep_exercise['equipment']}")
        
        # Verify start button was rendered
        mock_button.assert_any_call("Start", key=f"start_{sample_rep_exercise['name']}")

def test_button_callbacks(mock_streamlit, sample_exercise):
    """Test exercise card button callbacks."""
    on_start = Mock()
    on_complete = Mock()
    
    with patch('streamlit.container'), \
         patch('streamlit.columns') as mock_cols, \
         patch('streamlit.markdown'), \
         patch('streamlit.tabs'), \
         patch('streamlit.button') as mock_button:
        
        # Mock column objects
        mock_cols.return_value = [Mock(), Mock()]
        
        # Mock button clicks
        mock_button.side_effect = [True, False]  # Start button clicked
        
        # Render exercise card
        ExerciseCard.render(
            exercise=sample_exercise,
            on_start=on_start,
            on_complete=on_complete
        )
        
        # Verify callbacks were called
        on_start.assert_called_once()
        on_complete.assert_not_called() 