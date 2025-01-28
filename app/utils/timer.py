"""Timer utilities for exercise tracking."""
from datetime import datetime, timedelta
import streamlit as st
from typing import Optional, Callable
import re

def init_timer_state():
    """Initialize all timer-related session state variables."""
    if "timer_active" not in st.session_state:
        st.session_state.timer_active = False
    if "timer_start" not in st.session_state:
        st.session_state.timer_start = None
    if "timer_duration" not in st.session_state:
        st.session_state.timer_duration = 0
    if "timer_paused" not in st.session_state:
        st.session_state.timer_paused = False
    if "pause_time" not in st.session_state:
        st.session_state.pause_time = None
    if "should_play_sound" not in st.session_state:
        st.session_state.should_play_sound = False
    if "last_update" not in st.session_state:
        st.session_state.last_update = None

# Initialize state when module is imported
init_timer_state()

def parse_duration(duration_str: str, default_seconds: int = 60) -> int:
    """Convert duration string to seconds with unified parsing logic.
    
    Handles formats like:
    - "60 seconds"
    - "5 minutes"
    - "3 mins/side"
    - "10 reps"
    - "2 sets x 30 seconds"
    
    Args:
        duration_str: String containing duration information
        default_seconds: Default duration in seconds if parsing fails
    
    Returns:
        Duration in seconds
    """
    duration = 0
    duration_str = duration_str.lower()
    
    # Handle "X mins/side" format
    if '/side' in duration_str:
        duration_str = duration_str.replace('/side', '')
        multiplier = 2
    else:
        multiplier = 1
    
    # Handle "X sets x Y" format
    if 'sets' in duration_str or 'set' in duration_str:
        parts = re.split(r'sets?(?:\s+x\s+|\s+)', duration_str)
        if len(parts) >= 2:
            try:
                sets = int(parts[0].strip())
                duration_str = parts[1].strip()
                multiplier *= sets
            except (ValueError, IndexError):
                pass
    
    # Extract numbers and units
    parts = re.findall(r'(\d+)\s*(\w+)', duration_str)
    for value, unit in parts:
        try:
            value = int(value)
            if any(u in unit for u in ['min', 'minute']):
                duration += value * 60
            elif any(u in unit for u in ['sec', 'second']):
                duration += value
            elif any(u in unit for u in ['rep', 'reps']):
                duration += value * 5  # Assume 5 seconds per rep
        except (ValueError, IndexError):
            continue
    
    final_duration = duration * multiplier
    return final_duration if final_duration > 0 else default_seconds

def start_timer(duration_seconds: int) -> None:
    """Start a new timer with the specified duration."""
    st.session_state.timer_active = True
    st.session_state.timer_start = datetime.now()
    st.session_state.timer_duration = duration_seconds
    st.session_state.timer_paused = False
    st.session_state.pause_time = None
    st.session_state.last_update = datetime.now()
    st.session_state.should_play_sound = False

def update_timer(force_complete: bool = False) -> None:
    """Update the timer state."""
    if not st.session_state.timer_active:
        return
    
    if st.session_state.timer_paused:
        return
    
    current_time = datetime.now()
    elapsed = current_time - st.session_state.timer_start
    remaining = st.session_state.timer_duration - elapsed.total_seconds()
    
    if remaining <= 0 or force_complete:
        st.session_state.timer_active = False
        st.session_state.should_play_sound = True
        return
    
    st.session_state.last_update = current_time

def pause_timer() -> None:
    """Pause the current timer."""
    if st.session_state.timer_active and not st.session_state.timer_paused:
        st.session_state.timer_paused = True
        st.session_state.pause_time = datetime.now()

def resume_timer() -> None:
    """Resume a paused timer."""
    if st.session_state.timer_active and st.session_state.timer_paused:
        pause_duration = datetime.now() - st.session_state.pause_time
        st.session_state.timer_start += pause_duration
        st.session_state.timer_paused = False
        st.session_state.pause_time = None

def get_timer_display() -> str:
    """Get the current timer display string."""
    if not st.session_state.timer_active:
        return "00:00"
    
    current_time = datetime.now()
    if st.session_state.timer_paused:
        elapsed = st.session_state.pause_time - st.session_state.timer_start
    else:
        elapsed = current_time - st.session_state.timer_start
    
    remaining = max(0, st.session_state.timer_duration - elapsed.total_seconds())
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    
    return f"{minutes:02d}:{seconds:02d}"

def should_play_sound() -> bool:
    """Check if sound should be played."""
    return st.session_state.should_play_sound

def reset_sound_flag() -> None:
    """Reset the sound flag after playing."""
    st.session_state.should_play_sound = False

def is_timer_active() -> bool:
    """Check if a timer is currently active.
    
    Returns:
        bool: True if a timer is active, False otherwise.
    """
    return st.session_state.timer_active

def is_timer_paused() -> bool:
    """Check if the timer is currently paused.
    
    Returns:
        bool: True if the timer is paused, False otherwise.
    """
    return st.session_state.timer_paused

def init_rep_counter():
    """Initialize rep counter session state variables."""
    if 'rep_count' not in st.session_state:
        st.session_state.rep_count = 0
    if 'total_reps' not in st.session_state:
        st.session_state.total_reps = 0

def update_rep_counter():
    """Update and display rep counter progress."""
    init_rep_counter()
    
    progress = st.session_state.rep_count / st.session_state.total_reps
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(progress)
    with col2:
        st.markdown(f'<div class="rep-display">{st.session_state.rep_count}/{st.session_state.total_reps}</div>', 
                   unsafe_allow_html=True)
    
    return st.session_state.rep_count >= st.session_state.total_reps 