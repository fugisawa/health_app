import streamlit as st
import time
from typing import Dict, Optional, Callable

class ExerciseCard:
    @staticmethod
    def render(
        exercise: Dict,
        on_start: Optional[Callable] = None,
        on_complete: Optional[Callable] = None,
        is_active: bool = False,
        is_completed: bool = False
    ):
        with st.container():
            # Exercise header with title and duration/reps
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f'<h3 class="exercise-title">{exercise["name"]}</h3>', unsafe_allow_html=True)
            with col2:
                duration = exercise.get("duration", "")
                reps = exercise.get("reps", "")
                if duration:
                    st.markdown(f'<div class="duration-badge">{duration}</div>', unsafe_allow_html=True)
                elif reps:
                    st.markdown(f'<div class="duration-badge">{reps} reps</div>', unsafe_allow_html=True)
            
            # Exercise details in tabs
            tab1, tab2 = st.tabs(["📝 Details", "🎯 How to Perform"])
            
            with tab1:
                # Equipment section
                st.markdown("**EQUIPMENT**")
                st.markdown(exercise.get("equipment", "None required"))
                
                # Key notes section
                st.markdown("**KEY NOTES**")
                st.markdown(exercise.get("key_notes", "No specific notes"))
            
            with tab2:
                if "steps" in exercise:
                    for i, step in enumerate(exercise["steps"], 1):
                        st.markdown(f"{i}. {step}")
                if exercise.get("demo_link"):
                    st.markdown(f"[Watch Demo]({exercise['demo_link']})")
            
            # Control buttons
            if not is_completed:
                cols = st.columns([1, 1, 1])
                
                # Start/Pause button
                with cols[0]:
                    if not is_active:
                        if st.button("Start", key=f"start_{exercise['name']}", use_container_width=True):
                            if duration:
                                # Parse duration string to seconds
                                seconds = ExerciseCard._parse_duration(duration)
                                st.session_state.timer_duration = seconds
                            elif reps:
                                st.session_state.rep_count = 0
                                st.session_state.total_reps = int(reps.split()[0])
                            on_start()
                    else:
                        if st.button("Pause", key=f"pause_{exercise['name']}", use_container_width=True):
                            st.session_state.timer_paused = True
                            st.rerun()
                
                # Restart button
                with cols[1]:
                    if is_active:
                        if st.button("Restart", key=f"restart_{exercise['name']}", use_container_width=True):
                            if duration:
                                seconds = ExerciseCard._parse_duration(duration)
                                st.session_state.timer_duration = seconds
                                st.session_state.timer_start = time.time()
                            else:
                                st.session_state.rep_count = 0
                            st.session_state.timer_paused = False
                            st.rerun()
                
                # Complete button
                with cols[2]:
                    if is_active:
                        if st.button("Complete", key=f"complete_{exercise['name']}", use_container_width=True):
                            on_complete()
            else:
                st.success("✅ Completed")

    @staticmethod
    def _parse_duration(duration: str) -> int:
        """Convert duration string to seconds."""
        if "seconds" in duration:
            return int(duration.split()[0])
        elif "minutes" in duration:
            return int(duration.split()[0]) * 60
        return 0 