"""Tests for the main application."""
import pytest
import streamlit as st
from unittest.mock import Mock, patch

from app.main import init_session_state, setup_page, render_header, render_sidebar, render_protocol_view, main

def test_init_session_state(mock_streamlit):
    """Test session state initialization."""
    init_session_state()
    
    # Verify session state variables were initialized
    assert 'active_protocol' in st.session_state
    assert 'active_treatment' in st.session_state
    assert 'completed_exercises' in st.session_state
    assert isinstance(st.session_state.completed_exercises, set)

def test_setup_page(mock_streamlit):
    """Test page setup."""
    with patch('streamlit.set_page_config') as mock_config:
        setup_page()
        
        mock_config.assert_called_with(
            page_title="Health Protocol Dashboard",
            page_icon="🧘‍♂️",
            layout="wide",
            initial_sidebar_state="expanded"
        )

def test_render_header(mock_streamlit):
    """Test header rendering."""
    with patch('streamlit.title') as mock_title:
        render_header()
        
        mock_title.assert_called_with("🧘‍♂️ Health Protocol Dashboard")

def test_render_sidebar(mock_streamlit):
    """Test sidebar rendering."""
    with patch('streamlit.sidebar.title') as mock_title, \
         patch('streamlit.sidebar.radio') as mock_radio:
        
        mock_radio.return_value = "🔴 Light Therapy (LLLT)"
        
        render_sidebar()
        
        # Verify sidebar title
        mock_title.assert_called_with("Today's Focus")
        
        # Verify protocol selection
        mock_radio.assert_called_with(
            "Choose your wellness activity for this session",
            ["🔴 Light Therapy (LLLT)", "🧘‍♂️ Movement & Mobility"],
            label_visibility="hidden"
        )

def test_render_protocol_view_lllt(mock_streamlit):
    """Test rendering LLLT protocol view."""
    with patch('app.views.lllt.LLLTView') as mock_lllt_view:
        mock_view = Mock()
        mock_lllt_view.return_value = mock_view
        
        st.session_state.active_protocol = "🔴 Light Therapy (LLLT)"
        render_protocol_view()
        
        # Verify LLLT view was rendered
        mock_view.render.assert_called_once()

def test_render_protocol_view_mobility(mock_streamlit):
    """Test rendering Mobility protocol view."""
    with patch('app.views.mobility.MobilityView') as mock_mobility_view:
        mock_view = Mock()
        mock_mobility_view.return_value = mock_view
        
        st.session_state.active_protocol = "🧘‍♂️ Movement & Mobility"
        render_protocol_view()
        
        # Verify Mobility view was rendered
        mock_view.render.assert_called_once()

def test_main(mock_streamlit):
    """Test main application flow."""
    with patch('app.main.setup_page') as mock_setup, \
         patch('app.main.init_session_state') as mock_init, \
         patch('app.main.render_header') as mock_header, \
         patch('app.main.render_sidebar') as mock_sidebar, \
         patch('app.main.render_protocol_view') as mock_view:
        
        main()
        
        # Verify all components were called
        mock_setup.assert_called_once()
        mock_init.assert_called_once()
        mock_header.assert_called_once()
        mock_sidebar.assert_called_once()
        mock_view.assert_called_once()

def test_protocol_change_rerun(mock_streamlit):
    """Test rerun on protocol change."""
    with patch('streamlit.sidebar.radio') as mock_radio, \
         patch('streamlit.rerun') as mock_rerun:
        
        # Simulate protocol change
        st.session_state.active_protocol = "🔴 Light Therapy (LLLT)"
        mock_radio.return_value = "🧘‍♂️ Movement & Mobility"
        
        render_sidebar()
        
        # Verify rerun was triggered
        mock_rerun.assert_called_once() 