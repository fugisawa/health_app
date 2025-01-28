"""Main entry point for the Health Protocol Dashboard."""
import streamlit as st
from app.utils.state import AppState
from app.views.lllt import LLLTView
from app.views.mobility import MobilityView

def main():
    """Main entry point for the application."""
    # Configure the page
    st.set_page_config(
        page_title="Health Protocol Dashboard",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize application state
    if 'app_state' not in st.session_state:
        st.session_state.app_state = AppState()
    state = st.session_state.app_state
    
    # Render sidebar
    with st.sidebar:
        st.subheader("Protocol Selection")
        protocol = st.radio(
            "Select Protocol",
            ["lllt", "mobility"],
            label_visibility="collapsed",
            key="protocol_selector"
        )
        state.switch_protocol(protocol)
    
    # Render selected protocol view
    if state.selected_protocol == "lllt":
        LLLTView(state).render()
    else:
        MobilityView(state).render()

if __name__ == "__main__":
    main() 