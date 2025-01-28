"""
LLLT Protocol view module.
"""
import streamlit as st
from datetime import datetime

from app.data import (
    get_lllt_daily_data,
    get_weekly_schedule,
    get_adjustments_data,
    get_progress_metrics,
    get_supplement_data
)
from app.utils.storage import (
    load_session_progress,
    save_session_progress
)

def render():
    """Render the LLLT Protocol view."""
    st.title("LLLT Session")
    
    # Get current protocol data
    daily_data = get_lllt_daily_data()
    weekly_schedule = get_weekly_schedule()
    supplements = get_supplement_data()
    
    # Initialize completed treatments in session state if not exists
    if 'completed_treatments' not in st.session_state:
        st.session_state.completed_treatments = load_session_progress('lllt')
    
    # Display key principle
    st.header("Key Principle: Complete coverage of all treatment areas")
    
    # Treatment List Table
    st.subheader("📋 Treatment List")
    
    # Create the table header
    header_cols = st.columns([0.5, 2, 1, 1, 1.5])
    header_cols[0].markdown("**✓**")
    header_cols[1].markdown("**Treatment**")
    header_cols[2].markdown("**Duration**")
    header_cols[3].markdown("**Intensity**")
    header_cols[4].markdown("**Equipment**")
    
    # Create table rows
    for idx, treatment in enumerate(daily_data):
        cols = st.columns([0.5, 2, 1, 1, 1.5])
        
        # Checkbox column
        is_completed = idx in st.session_state.completed_treatments
        if cols[0].checkbox("Complete", key=f"lllt_check_{idx}", value=is_completed, label_visibility="collapsed"):
            st.session_state.completed_treatments.add(idx)
            save_session_progress(st.session_state.completed_treatments, 'lllt')
        else:
            if idx in st.session_state.completed_treatments:
                st.session_state.completed_treatments.discard(idx)
                save_session_progress(st.session_state.completed_treatments, 'lllt')
        
        # Treatment details columns
        cols[1].markdown(treatment['name'])
        cols[2].markdown(f"{treatment['duration']} seconds")
        cols[3].markdown(treatment['intensity'])
        cols[4].markdown(treatment['equipment'])
    
    # Progress bar
    progress = len(st.session_state.completed_treatments) / len(daily_data)
    st.progress(progress)
    st.caption(f"Completed: {len(st.session_state.completed_treatments)}/{len(daily_data)} treatments")
    
    # Current Treatment Section
    if len(daily_data) > 0:
        st.markdown("### 🎯 Current Treatment")
        selected_treatment = st.selectbox(
            "Select treatment to perform:",
            options=range(len(daily_data)),
            format_func=lambda x: f"{'✅' if x in st.session_state.completed_treatments else '⏳'} {daily_data[x]['name']}",
            key="treatment_selector"
        )
        
        treatment = daily_data[selected_treatment]
        
        with st.expander("📋 Treatment Details", expanded=True):
            st.markdown(f"""
            ### {treatment['name']}
            
            **Duration:** {treatment['duration']} seconds  
            **Intensity:** {treatment['intensity']}  
            **Equipment:** {treatment['equipment']}  
            **Steps:**
            {treatment.get('steps', '- Follow standard protocol')}
            """)
            
            # Auto-complete checkbox
            if st.checkbox("Mark as complete when timer finishes", key=f"auto_lllt_{selected_treatment}"):
                st.session_state[f"auto_complete_lllt_{selected_treatment}"] = True
        
        # Timer for current treatment
        st.subheader("⏱️ Treatment Timer")
        duration = int(treatment['duration'])
        
        col1, col2 = st.columns(2)
        with col1:
            if 'lllt_timer_running' not in st.session_state:
                st.session_state.lllt_timer_running = False
                st.session_state.lllt_time_remaining = duration
            
            if st.button('Start/Pause Timer'):
                st.session_state.lllt_timer_running = not st.session_state.lllt_timer_running
            
            st.write(f"Time Remaining: {st.session_state.lllt_time_remaining} seconds")
        
        with col2:
            if st.button('Reset Timer'):
                st.session_state.lllt_time_remaining = duration
                st.session_state.lllt_timer_running = False
    
    # Reset button
    if st.button("🔄 Reset Session"):
        st.session_state.completed_treatments = set()
        st.rerun()
    
    # Supplement Schedule
    with st.sidebar:
        st.markdown("### 💊 Supplement Schedule")
        for timing, supps in supplements.items():
            with st.expander(timing):
                for supp in supps:
                    st.markdown(f"- **{supp['name']}**: {supp['dosage']}")
                    if 'notes' in supp:
                        st.caption(supp['notes'])
        
        # Session Guidelines
        st.markdown("### 📝 Session Guidelines")
        st.info("""
        **Before Starting:**
        - Ensure device is fully charged
        - Clean treatment areas
        - Remove any products from skin
        
        **During Treatment:**
        - Maintain steady contact
        - Move device slowly
        - Follow recommended duration
        
        **After Completion:**
        - Clean device
        - Apply recommended products
        - Take scheduled supplements
        """) 