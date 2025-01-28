import streamlit as st
from datetime import datetime
from app.components.timer import TimerComponent
from data.lllt_data import (
    get_lllt_daily_data,
    get_weekly_schedule,
    get_supplement_data
)

def get_todays_protocol():
    """Get today's LLLT protocol based on the weekly schedule."""
    weekday = datetime.now().strftime("%A")
    schedule = get_weekly_schedule()
    daily_data = get_lllt_daily_data()
    
    for day in schedule:
        if day["name"] == weekday:
            if day["frequency"] == "Rest Day":
                return None, day
            
            # Parse focus areas from the schedule
            focus = day["focus"]
            areas = []
            if "Head" in focus:
                areas.extend(daily_data["Head"])
            if "Neck" in focus:
                areas.extend(daily_data["Neck"])
            if "Back" in focus:
                areas.extend(daily_data["Back"])
            
            return areas, day
    
    return None, None

def render():
    """Render the LLLT protocol view."""
    st.title("LLLT Protocol")
    
    # Get today's protocol
    treatments, schedule = get_todays_protocol()
    
    if not schedule:
        st.error("Could not determine today's protocol. Please check the data.")
        return
    
    # Display today's schedule
    st.header(f"Today's Protocol - {schedule['name']}")
    
    if schedule["frequency"] == "Rest Day":
        st.info(f"""
        ### Rest Day
        Today is a scheduled rest day for tissue recovery and adaptation.
        
        **Key Principle:** {schedule['key_principle']}
        """)
        return
    
    st.markdown(f"""
    **Session Type:** {schedule['frequency']}  
    **Focus Areas:** {schedule['focus']}  
    **Key Principle:** {schedule['key_principle']}
    """)
    
    # Treatment section
    if treatments:
        # Initialize completed treatments in session state if not exists
        if 'completed_treatments' not in st.session_state:
            st.session_state.completed_treatments = set()
        
        # Session Overview Table
        st.subheader("📋 Session Overview")
        treatment_rows = []
        for idx, treatment in enumerate(treatments):
            is_completed = idx in st.session_state.completed_treatments
            status = "✅" if is_completed else "⏳"
            
            treatment_rows.append({
                "Status": status,
                "Treatment": treatment['name'],
                "Duration": treatment['duration'],
                "Intensity": treatment['intensity'],
                "Equipment": treatment['equipment']
            })
        
        # Display table with treatment selection
        col1, col2 = st.columns([3, 1])
        with col1:
            selected_treatment = st.selectbox(
                "Select treatment to perform:",
                options=range(len(treatments)),
                format_func=lambda x: f"{treatment_rows[x]['Status']} {treatment_rows[x]['Treatment']}",
                key="treatment_selector"
            )
        
        with col2:
            if st.button("Mark as Complete", key="complete_button"):
                st.session_state.completed_treatments.add(selected_treatment)
                st.rerun()
        
        # Display treatment table
        st.markdown("### Treatment List")
        st.table(treatment_rows)
        
        # Current Treatment Section
        if selected_treatment is not None:
            treatment = treatments[selected_treatment]
            
            with st.expander("📋 Current Treatment", expanded=True):
                st.markdown(f"""
                ### {treatment['name']}
                
                **Equipment:** {treatment['equipment']}  
                **Intensity:** {treatment['intensity']}  
                **Duration:** {treatment['duration']}
                
                **Steps:**
                """)
                
                for step in treatment['steps']:
                    st.markdown(f"- {step}")
                
                st.markdown(f"**Notes:** _{treatment['notes']}_")
            
            # Timer for current treatment
            st.subheader("⏱️ Treatment Timer")
            timer = TimerComponent()
            duration_seconds = int(treatment['duration'].split()[0])  # Extract seconds from "120 seconds"
            timer.render(duration_seconds=duration_seconds)
        
        # Reset button
        if st.button("🔄 Reset Session"):
            st.session_state.completed_treatments = set()
            st.rerun()
    
    # Supplement recommendations
    with st.sidebar:
        st.markdown("### 💊 Supplement Schedule")
        supplements = get_supplement_data()
        
        for supp in supplements:
            with st.expander(f"🕒 {supp['Time']}"):
                st.markdown(f"""
                **Take:** {supp['Supplements']}  
                **Purpose:** {supp['Purpose']}
                """)
        
        st.divider()
        
        st.markdown("### 📝 Session Guidelines")
        st.info("""
        **Before Starting:**
        - Ensure device is fully charged
        - Clean treatment areas
        - Have timer ready
        
        **During Treatment:**
        - Maintain steady contact
        - Follow prescribed intensity
        - Complete full duration
        
        **After Completion:**
        - Note any sensations
        - Take prescribed supplements
        - Allow recovery time
        """) 