"""
Mobility Protocol view module.
"""
import streamlit as st
from datetime import datetime

from app.data.health import (
    get_current_phase,
    get_current_session,
    get_current_exercises
)
from app.utils.storage import (
    load_session_progress,
    save_session_progress
)

def render():
    """Render the Mobility Protocol view."""
    st.title("Mobility Protocol")
    
    # Get current phase and session
    current_phase = get_current_phase()
    current_session = get_current_session()
    exercises = get_current_exercises()
    
    # Display phase information
    st.header(f"Current: {current_phase} - {current_session.title()} Session")
    
    # Initialize completed exercises in session state if not exists
    if 'completed_exercises' not in st.session_state:
        st.session_state.completed_exercises = load_session_progress(current_session)
    
    # Session Overview Table
    st.subheader("📋 Session Overview")
    
    # Create the table header
    header_cols = st.columns([0.5, 2, 1, 1, 2.5])
    header_cols[0].markdown("**✓**")
    header_cols[1].markdown("**Exercise**")
    header_cols[2].markdown("**Sets/Reps**")
    header_cols[3].markdown("**Equipment**")
    header_cols[4].markdown("**Notes**")
    
    # Create table rows
    for idx, exercise in enumerate(exercises):
        cols = st.columns([0.5, 2, 1, 1, 2.5])
        
        # Checkbox column
        is_completed = idx in st.session_state.completed_exercises
        if cols[0].checkbox("Complete", key=f"check_{idx}", value=is_completed, label_visibility="collapsed"):
            st.session_state.completed_exercises.add(idx)
            save_session_progress(st.session_state.completed_exercises, current_session)
        else:
            if idx in st.session_state.completed_exercises:
                st.session_state.completed_exercises.discard(idx)
                save_session_progress(st.session_state.completed_exercises, current_session)
        
        # Exercise details columns
        cols[1].markdown(exercise['name'])
        cols[2].markdown(exercise['sets_reps'])
        cols[3].markdown(exercise['equipment'])
        cols[4].markdown(exercise['notes'])
    
    # Progress bar
    progress = len(st.session_state.completed_exercises) / len(exercises)
    st.progress(progress)
    st.caption(f"Completed: {len(st.session_state.completed_exercises)}/{len(exercises)} exercises")
    
    # Current Exercise Section
    if len(exercises) > 0:
        st.markdown("### 🎯 Current Exercise")
        selected_exercise = st.selectbox(
            "Select exercise to perform:",
            options=range(len(exercises)),
            format_func=lambda x: f"{'✅' if x in st.session_state.completed_exercises else '⏳'} {exercises[x]['name']}",
            key="exercise_selector"
        )
        
        exercise = exercises[selected_exercise]
        
        with st.expander("📋 Exercise Details", expanded=True):
            st.markdown(f"""
            ### {exercise['name']}
            
            **Sets/Reps:** {exercise['sets_reps']}  
            **Equipment:** {exercise['equipment']}  
            **Notes:** _{exercise['notes']}_
            """)
            
            # Auto-complete checkbox
            if st.checkbox("Mark as complete when timer finishes", key=f"auto_{selected_exercise}"):
                st.session_state[f"auto_complete_{selected_exercise}"] = True
        
        # Timer for current exercise
        st.subheader("⏱️ Exercise Timer")
        
        # Parse duration from sets/reps if it contains time
        duration_str = exercise['sets_reps'].lower()
        if "seconds" in duration_str:
            duration = int(duration_str.split()[0])
        elif "mins" in duration_str or "minutes" in duration_str:
            duration = int(duration_str.split()[0]) * 60
        else:
            duration = 60  # default for rep-based exercises
        
        col1, col2 = st.columns(2)
        with col1:
            if 'timer_running' not in st.session_state:
                st.session_state.timer_running = False
                st.session_state.time_remaining = duration
            
            if st.button('Start/Pause Timer'):
                st.session_state.timer_running = not st.session_state.timer_running
            
            st.write(f"Time Remaining: {st.session_state.time_remaining} seconds")
        
        with col2:
            if st.button('Reset Timer'):
                st.session_state.time_remaining = duration
                st.session_state.timer_running = False
    
    # Reset button
    if st.button("🔄 Reset Session"):
        st.session_state.completed_exercises = set()
        st.rerun()
    
    # Session Guidelines
    with st.sidebar:
        st.markdown("### 📝 Session Guidelines")
        st.info("""
        **Before Starting:**
        - Ensure proper warm-up
        - Have water nearby
        - Clear adequate space
        
        **During Exercise:**
        - Focus on form over speed
        - Breathe steadily
        - Stay within pain-free range
        
        **After Completion:**
        - Note any limitations
        - Cool down properly
        - Stay hydrated
        """) 