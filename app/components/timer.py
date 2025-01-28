"""Timer component for Streamlit."""
import streamlit as st
import time
from datetime import datetime, timedelta

class TimerComponent:
    """Enhanced timer component with pause/resume and sound notification."""
    
    def __init__(self):
        """Initialize timer state."""
        if 'start_time' not in st.session_state:
            st.session_state.start_time = None
        if 'paused_time' not in st.session_state:
            st.session_state.paused_time = None
        if 'is_paused' not in st.session_state:
            st.session_state.is_paused = False
    
    def render(self, duration_seconds=300):
        """Render the timer component.
        
        Args:
            duration_seconds: Timer duration in seconds (default: 5 minutes)
        """
        if st.session_state.start_time is None:
            st.session_state.start_time = datetime.now()
            st.session_state.paused_time = None
            st.session_state.is_paused = False
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Calculate elapsed time
            if st.session_state.is_paused:
                elapsed = st.session_state.paused_time - st.session_state.start_time
            else:
                elapsed = datetime.now() - st.session_state.start_time
            
            remaining = timedelta(seconds=duration_seconds) - elapsed
            remaining_seconds = max(0, int(remaining.total_seconds()))
            
            # Display progress bar
            progress = 1 - (remaining_seconds / duration_seconds)
            st.progress(min(1.0, progress))
            
            # Display time remaining
            mins, secs = divmod(remaining_seconds, 60)
            st.markdown(f"**Time Remaining:** {mins:02d}:{secs:02d}")
        
        with col2:
            # Pause/Resume button
            if st.button("⏯️ Pause/Resume"):
                if st.session_state.is_paused:
                    # Resume - adjust start time to account for pause duration
                    pause_duration = datetime.now() - st.session_state.paused_time
                    st.session_state.start_time += pause_duration
                    st.session_state.is_paused = False
                else:
                    # Pause
                    st.session_state.paused_time = datetime.now()
                    st.session_state.is_paused = True
            
            # Reset button
            if st.button("🔄 Reset"):
                st.session_state.start_time = datetime.now()
                st.session_state.paused_time = None
                st.session_state.is_paused = False
        
        # Play sound when timer completes
        if remaining_seconds <= 0 and not st.session_state.is_paused:
            st.balloons()
            st.audio("data:audio/wav;base64,UklGRjIAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAAABmYWN0BAAAAAAAAABkYXRhAAAAAA==", format='audio/wav')
            st.session_state.start_time = None 