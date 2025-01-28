"""Rep counter utilities for exercise tracking."""
import streamlit as st
from typing import Optional, Tuple

def init_rep_counter() -> None:
    """Initialize rep counter session state variables."""
    if "current_reps" not in st.session_state:
        st.session_state.current_reps = 0
    if "target_reps" not in st.session_state:
        st.session_state.target_reps = 0
    if "current_set" not in st.session_state:
        st.session_state.current_set = 1
    if "target_sets" not in st.session_state:
        st.session_state.target_sets = 1

def start_rep_counter(target_reps: int, target_sets: int = 1) -> None:
    """Start a new rep counter with the specified targets.
    
    Args:
        target_reps: The target number of repetitions.
        target_sets: The target number of sets (default: 1).
    """
    st.session_state.current_reps = 0
    st.session_state.target_reps = target_reps
    st.session_state.current_set = 1
    st.session_state.target_sets = target_sets

def increment_rep() -> None:
    """Increment the rep counter by one."""
    if st.session_state.current_reps < st.session_state.target_reps:
        st.session_state.current_reps += 1

def complete_set() -> None:
    """Complete the current set and move to the next one."""
    if st.session_state.current_set < st.session_state.target_sets:
        st.session_state.current_set += 1
        st.session_state.current_reps = 0

def get_rep_display() -> Tuple[str, float]:
    """Get the current rep counter display information.
    
    Returns:
        Tuple[str, float]: A tuple containing:
            - The formatted rep/set display string
            - The progress percentage (0-100)
    """
    total_reps = st.session_state.target_reps * st.session_state.target_sets
    completed_reps = ((st.session_state.current_set - 1) * st.session_state.target_reps + 
                     st.session_state.current_reps)
    
    progress = (completed_reps / total_reps) * 100 if total_reps > 0 else 0
    
    if st.session_state.target_sets > 1:
        display = (f"Set {st.session_state.current_set}/{st.session_state.target_sets} - "
                  f"Rep {st.session_state.current_reps}/{st.session_state.target_reps}")
    else:
        display = f"Rep {st.session_state.current_reps}/{st.session_state.target_reps}"
    
    return display, progress

def is_set_complete() -> bool:
    """Check if the current set is complete.
    
    Returns:
        bool: True if the current set is complete, False otherwise.
    """
    return st.session_state.current_reps >= st.session_state.target_reps

def is_exercise_complete() -> bool:
    """Check if all sets are complete.
    
    Returns:
        bool: True if all sets are complete, False otherwise.
    """
    return (st.session_state.current_set >= st.session_state.target_sets and 
            st.session_state.current_reps >= st.session_state.target_reps)

def parse_reps(reps_str: str) -> Tuple[int, int]:
    """Parse a reps string into target reps and sets.
    
    Args:
        reps_str: String containing rep/set information (e.g., "10 reps", "3x10 reps").
    
    Returns:
        Tuple[int, int]: A tuple containing (target_reps, target_sets).
    """
    parts = reps_str.lower().split()
    
    # Check for set notation (e.g., "3x10 reps")
    if 'x' in parts[0]:
        sets, reps = parts[0].split('x')
        return int(reps), int(sets)
    
    # Single set notation (e.g., "10 reps")
    return int(parts[0]), 1 