import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

# Import views
from app.views import render_mobility, render_lllt

# Import data functions
from app.data import (
    get_current_phase,
    get_current_session,
    get_current_exercises
)

# Import storage utilities
from app.utils.storage import (
    load_session_progress,
    save_session_progress,
    get_session_history,
    export_history_to_csv,
    generate_calendar_events,
    get_completion_stats
)

def render_current_session():
    """Render the current session's exercise table."""
    current_phase = get_current_phase()
    current_session = get_current_session()
    exercises = get_current_exercises()
    
    # Initialize completed exercises from storage
    if 'completed_exercises' not in st.session_state:
        st.session_state.completed_exercises = load_session_progress(current_session)
    
    st.subheader(f"Current Session: {current_phase} - {current_session.title()}")
    
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
        if cols[0].checkbox("Complete", key=f"home_check_{idx}", value=is_completed, label_visibility="collapsed"):
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

def render_progress_history():
    """Render the progress history section."""
    st.subheader("📊 Progress History")
    
    # Get completion statistics
    stats = get_completion_stats(30)  # Last 30 days
    
    if not stats['daily_completion']:
        st.info("No progress history available yet. Complete some exercises to see your progress!")
        return
    
    # Show current streak
    st.metric("🔥 Current Streak", f"{stats['streak']} days")
    
    # Create completion trend chart
    df_daily = pd.DataFrame(stats['daily_completion'])
    fig_daily = px.line(df_daily, x='date', y='completed', 
                       title='Daily Completion Trend',
                       labels={'completed': 'Exercises Completed', 'date': 'Date'})
    st.plotly_chart(fig_daily, use_container_width=True)
    
    # Session type breakdown
    st.subheader("Session Type Breakdown")
    session_data = []
    for session_type, data in stats['session_types'].items():
        df_session = pd.DataFrame(data)
        avg_completion = df_session['completed'].mean()
        session_data.append({
            'Session': session_type.title(),
            'Average Completion': f"{avg_completion:.1f}",
            'Total Sessions': len(data)
        })
    
    st.dataframe(
        pd.DataFrame(session_data),
        column_config={
            'Session': st.column_config.Column('Session Type', width='medium'),
            'Average Completion': st.column_config.NumberColumn('Avg. Exercises/Session', format="%.1f"),
            'Total Sessions': st.column_config.NumberColumn('Total Sessions', width='small'),
        },
        hide_index=True,
    )
    
    # Export options
    st.subheader("📤 Export Options")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export History (CSV)"):
            csv_file = export_history_to_csv()
            with open(csv_file, 'r') as f:
                st.download_button(
                    "Download CSV",
                    f.read(),
                    file_name=f"health_protocol_history_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    
    with col2:
        if st.button("📅 Generate Calendar (ICS)"):
            ics_file = generate_calendar_events()
            with open(ics_file, 'r') as f:
                st.download_button(
                    "Download Calendar",
                    f.read(),
                    file_name=f"health_protocol_schedule_{datetime.now().strftime('%Y%m%d')}.ics",
                    mime="text/calendar"
                )

def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="Health Protocol",
        page_icon="🏥",
        layout="wide"
    )
    
    # Add custom CSS for mobile responsiveness
    st.markdown("""
        <style>
        /* Make the layout more responsive */
        @media (max-width: 768px) {
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            /* Adjust column widths for mobile */
            div[data-testid="column"] {
                width: 100% !important;
                flex: 1 1 auto !important;
                min-width: auto !important;
            }
            /* Make sidebar collapsible on mobile */
            .css-1d391kg {
                width: auto !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("Health Protocol App")
    
    # Show current session at the top of home page
    render_current_session()
    
    st.divider()
    
    # Navigation sidebar
    with st.sidebar:
        st.subheader("Navigation")
        page = st.radio(
            "Go to",
            ["Home", "LLLT Session", "Mobility Training"],
            label_visibility="collapsed"
        )
    
    # Render the selected view
    if page == "LLLT Session":
        render_lllt()
    elif page == "Mobility Training":
        render_mobility()
    else:  # Home
        render_progress_history()
        st.markdown("""
        ### Welcome to your Health Protocol App
        
        Select a session from the navigation menu to begin:
        - **LLLT Session**: Low-Level Light Therapy protocol
        - **Mobility Training**: Daily mobility exercises
        """)

if __name__ == "__main__":
    main() 