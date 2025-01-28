import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
from data.lllt_data import (
    get_lllt_daily_data,
    get_supplement_data,
    get_weekly_schedule,
    get_adjustments_data
)
from data.mobility_data import (
    get_phase1_data,
    get_phase2_data,
    get_phase3_data,
    get_progress_metrics,
    get_key_adjustments
)
from models.lllt import LLLTProtocol
from models.mobility import MobilityProtocol
from playsound import playsound
import os
import plotly.express as px
import math

# Page config with custom theme and responsive layout
st.set_page_config(
    page_title="Health Protocol Dashboard",
    page_icon="🧘‍♂️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/health-protocol',
        'Report a bug': "https://github.com/yourusername/health-protocol/issues",
        'About': "# Health Protocol Dashboard\nTrack and manage your health protocols efficiently."
    }
)

# Update the CSS with refined color scheme
st.markdown("""
<style>
    /* Modern color scheme - Inspired by 2024 design trends */
    :root {
        /* Primary Background Colors */
        --bg-gradient-1: #1e1b4b;  /* Deep Navy */
        --bg-gradient-2: #312e81;  /* Rich Indigo */
        
        /* Surface Colors */
        --surface-primary: rgba(255, 255, 255, 0.08);
        --surface-secondary: rgba(255, 255, 255, 0.04);
        
        /* Accent Colors */
        --accent-primary: #818cf8;    /* Soft Indigo */
        --accent-secondary: #4f46e5;  /* Electric Indigo */
        --accent-success: #34d399;    /* Emerald */
        --accent-warning: #fbbf24;    /* Amber */
        
        /* Text Colors */
        --text-primary: #ffffff;
        --text-secondary: rgba(255, 255, 255, 0.7);
        --text-tertiary: rgba(255, 255, 255, 0.5);
    }

    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, var(--bg-gradient-1) 0%, var(--bg-gradient-2) 100%);
        color: var(--text-primary);
    }

    /* Card styling */
    .exercise-card {
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .exercise-card.active {
        border: 2px solid #5BC0BE;
        box-shadow: 0 4px 12px rgba(91, 192, 190, 0.3);
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .duration-badge {
        background: rgba(91, 192, 190, 0.3);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
    }

    /* Timer container */
    .timer-container {
        background: var(--surface-primary);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    /* Timer display */
    .timer-display {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        transform: none !important;
    }

    /* Progress ring */
    .progress-ring circle.background {
        stroke: var(--surface-secondary);
    }
    .progress-ring circle.progress {
        stroke: var(--accent-primary);
        filter: drop-shadow(0 0 4px var(--accent-primary));
    }

    /* Button styles */
    .stButton>button {
        background: var(--accent-secondary);
        color: var(--text-primary);
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
        background: var(--accent-primary);
    }

    /* Specific button styles */
    .start-button button {
        background: linear-gradient(135deg, var(--accent-secondary) 0%, var(--accent-primary) 100%);
    }
    .pause-button button {
        background: var(--accent-warning);
    }
    .complete-button button {
        background: var(--accent-success);
    }

    /* Text styles */
    h1, h2, h3 {
        color: var(--text-primary);
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    p {
        color: var(--text-secondary);
        line-height: 1.6;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: var(--surface-primary);
        border-radius: 12px;
        padding: 0.75rem 1.25rem;
        color: var(--text-primary);
    }
    .stTabs [aria-selected="true"] {
        background: var(--accent-secondary);
    }

    /* Metrics and progress */
    .metric-container {
        background: var(--surface-primary);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .metric-value {
        color: var(--accent-primary);
        font-size: 2rem;
        font-weight: 700;
    }
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.875rem;
    }

    /* Sidebar */
    .css-1d391kg {
        background: var(--surface-primary);
    }

    /* Sidebar text colors */
    .css-1d391kg, .css-1d391kg p {
        color: var(--text-primary) !important;
    }
    
    /* Sidebar text */
    [data-testid="stSidebarNav"] {
        background-color: var(--surface-primary);
    }
    .sidebar .sidebar-content {
        background-color: var(--surface-primary);
    }
    
    /* Radio buttons in sidebar */
    .stRadio > label {
        color: var(--text-primary) !important;
    }
    
    /* Button text alignment */
    .stButton>button {
        white-space: nowrap;
        min-width: 120px;
        padding: 0.75rem 1.25rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        font-size: 0.875rem;
    }
    
    /* Sidebar background */
    section[data-testid="stSidebar"] > div {
        background: var(--bg-gradient-1);
    }
    
    /* Sidebar text */
    .sidebar-content {
        color: var(--text-primary) !important;
    }
    
    /* Radio button text */
    .stRadio label {
        color: var(--text-primary) !important;
    }
    
    /* Help text */
    .stRadio div[data-testid="stMarkdownContainer"] {
        color: var(--text-secondary) !important;
    }

    /* Metrics styling */
    .metric-value, .metric-delta {
        color: var(--text-primary) !important;
    }
    [data-testid="stMetricValue"] > div {
        color: var(--text-primary) !important;
    }
    [data-testid="stMetricDelta"] > div {
        color: var(--text-secondary) !important;
    }
    
    /* Help icon color */
    .stMarkdown div[data-testid="StyledLinkIconContainer"] {
        color: var(--text-primary) !important;
    }
    
    /* Protocol selector styling */
    .protocol-selector {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        margin: 1rem 0;
    }
    
    .protocol-option {
        background: var(--surface-primary);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .protocol-option:hover {
        background: var(--surface-secondary);
        transform: translateY(-2px);
    }
    
    .protocol-option.selected {
        background: var(--accent-primary);
        border-color: var(--accent-secondary);
    }
    
    .protocol-icon {
        font-size: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
    }
    
    .protocol-info {
        flex: 1;
    }
    
    .protocol-name {
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }
    
    .protocol-desc {
        color: var(--text-secondary);
        font-size: 0.875rem;
        margin: 0;
    }

    /* Timer styling */
    .progress-ring {
        position: relative;
        width: 200px;
        height: 200px;
        margin: 0 auto;
    }
    
    .progress-ring circle {
        fill: none;
        stroke-width: 8;
    }
    
    .progress-ring .background {
        stroke: var(--surface-secondary);
    }
    
    .progress-ring .progress {
        stroke: var(--accent-primary);
        filter: drop-shadow(0 0 4px var(--accent-primary));
        transition: stroke-dashoffset 0.3s ease;
    }
    
    /* Timer display container */
    .timer-display-container {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        display: flex;
        align-items: center;
        justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

# Update the main header style
st.markdown("""
    <div style="text-align: center; padding: clamp(2rem, 4vw, 3rem) 0;">
        <h1 style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: clamp(2rem, 5vw, 3rem); color: var(--primary);">
            🧘‍♂️ Health Protocol Dashboard
        </h1>
    </div>
""", unsafe_allow_html=True)

# Update sidebar header style
with st.sidebar:
    st.markdown("""
        <div style="padding: clamp(0.5rem, 2vw, 1rem);">
            <h3 style="font-size: clamp(1.2rem, 3vw, 1.5rem); color: var(--text-primary);">Today's Focus</h3>
            <p style="color: var(--text-secondary); font-size: clamp(0.9rem, 2vw, 1rem); margin-top: 0.5rem;">
                Choose your wellness activity for this session
            </p>
        </div>
    """, unsafe_allow_html=True)

# Initialize protocols
@st.cache_data
def load_protocols():
    lllt_protocol = LLLTProtocol(
        name="LLLT Protocol",
        description="Low-Level Light Therapy Protocol for Hair and Body Optimization",
        daily_schedule=get_lllt_daily_data(),
        supplement_schedule=get_supplement_data(),
        weekly_schedule=get_weekly_schedule()
    )
    
    mobility_protocol = MobilityProtocol(
        name="Mobility Protocol",
        description="Progressive Mobility Training for Ashtanga Yoga Mastery",
        phases={
            "phase1": get_phase1_data(),
            "phase2": get_phase2_data(),
            "phase3": get_phase3_data()
        },
        phase_details={
            "phase1": {
                "name": "1: Foundational Mobility",
                "duration": "Months 1-6"
            },
            "phase2": {
                "name": "2: Intermediate Strength",
                "duration": "Months 7-12"
            },
            "phase3": {
                "name": "3: Advanced Mastery",
                "duration": "Months 13-18"
            }
        },
        progress_metrics=get_progress_metrics()
    )
    
    return lllt_protocol, mobility_protocol

# Movement demonstrations dictionary
MOVEMENT_DEMOS = {
    "Dynamic Cat-Cow": {
        "youtube": "https://www.youtube.com/watch?v=kqnua4rHVVA",
        "how_to": [
            "Start on hands and knees in tabletop position",
            "Inhale: Drop belly, lift chest and tailbone (Cow)",
            "Exhale: Round spine, tuck chin and tailbone (Cat)",
            "Flow smoothly between positions",
            "Keep movements synchronized with breath"
        ]
    },
    "90/90 Hip Switch": {
        "youtube": "https://www.youtube.com/watch?v=nLuvQCTPrcY",
        "how_to": [
            "Sit with one leg bent 90° in front, other leg 90° to side",
            "Keep back straight and core engaged",
            "Lift hips and switch leg positions smoothly",
            "Control the movement throughout",
            "Keep feet flexed to protect knees"
        ]
    },
    "Sun Salutation A": {
        "youtube": "https://www.youtube.com/watch?v=8AakYeM_iRQ",
        "how_to": [
            "Start in Mountain Pose (Tadasana)",
            "Flow through sequence: Forward Fold → Plank → Chaturanga",
            "Upward Dog → Downward Dog → Forward Fold",
            "Return to Mountain Pose",
            "Coordinate movement with breath"
        ]
    }
    # Add more exercises as needed
}

# Load data
lllt_protocol, mobility_protocol = load_protocols()
lllt_dfs = lllt_protocol.to_dataframe()
mobility_dfs = mobility_protocol.to_dataframe()

# Initialize session state variables at the top level
def init_session_state():
    """Initialize all session state variables in one place"""
    defaults = {
        'completed_exercises': set(),
        'current_exercise': None,
        'session_start': None,
        'timer_active': False,
        'timer_start': None,
        'timer_duration': 0,
        'timer_paused': False,
        'pause_time': None,
        'last_update': None,
        'should_play_sound': False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def parse_duration(duration_str: str, default_seconds: int = 60) -> int:
    """Convert duration string to seconds with unified parsing logic"""
    duration = 0
    parts = duration_str.lower().replace('/', ' ').split()
    
    for i, part in enumerate(parts):
        try:
            if 'min' in part:
                num = int(parts[i-1])
                duration += num * 60
            elif 'sec' in part:
                num = int(parts[i-1])
                duration += num
            elif 'rep' in part:
                num = int(parts[i-1])
                duration += num * 5  # Assume 5 seconds per rep
        except (ValueError, IndexError):
            continue
    
    return duration if duration > 0 else default_seconds

def update_timer_state():
    """Update timer state without blocking"""
    if not st.session_state.timer_active:
        return
        
    if st.session_state.timer_paused:
        return
        
    current_time = time.time()
    if st.session_state.last_update is None:
        st.session_state.last_update = current_time
        
    # Calculate elapsed time
    elapsed = current_time - st.session_state.timer_start
    remaining = st.session_state.timer_duration - elapsed
    
    # Check if timer is complete
    if remaining <= 0:
        st.session_state.timer_active = False
        st.session_state.should_play_sound = True
        if st.session_state.current_exercise:
            st.session_state.completed_exercises.add(st.session_state.current_exercise['Exercise'])
            st.session_state.current_exercise = None
        st.rerun()
    
    # Update every second
    if current_time - st.session_state.last_update >= 1:
        st.session_state.last_update = current_time
        st.rerun()

def start_exercise(exercise: dict):
    """Start an exercise with non-blocking timer"""
    st.session_state.current_exercise = exercise
    if not st.session_state.session_start:
        st.session_state.session_start = datetime.now()
    
    # Parse duration and start timer
    duration_str = exercise.get('Sets/Reps/Duration', '60 seconds')
    st.session_state.timer_duration = parse_duration(duration_str)
    st.session_state.timer_start = time.time()
    st.session_state.timer_active = True
    st.session_state.timer_paused = False
    st.session_state.last_update = None
    st.rerun()

def pause_timer():
    """Pause the current timer"""
    if st.session_state.timer_active:
        st.session_state.timer_paused = True
        st.session_state.pause_time = time.time()
        st.rerun()

def resume_timer():
    """Resume the paused timer"""
    if st.session_state.timer_paused:
        elapsed_pause = time.time() - st.session_state.pause_time
        st.session_state.timer_start += elapsed_pause
        st.session_state.timer_paused = False
        st.session_state.last_update = None
        st.rerun()

def restart_timer():
    """Restart the current timer"""
    if st.session_state.current_exercise:
        st.session_state.timer_start = time.time()
        st.session_state.timer_paused = False
        st.session_state.last_update = None
        st.rerun()

def complete_exercise():
    """Mark current exercise as complete"""
    if st.session_state.current_exercise:
        st.session_state.completed_exercises.add(st.session_state.current_exercise['Exercise'])
        st.session_state.current_exercise = None
        st.session_state.timer_active = False
        st.rerun()

def display_timer():
    """Display timer with improved styling and non-blocking updates"""
    if not st.session_state.current_exercise:
        return
        
    # Update timer state
    update_timer_state()
    
    # Calculate time remaining
    if st.session_state.timer_paused:
        elapsed = st.session_state.pause_time - st.session_state.timer_start
    else:
        elapsed = time.time() - st.session_state.timer_start
    
    remaining = max(0, st.session_state.timer_duration - int(elapsed))
    progress = min(1.0, elapsed / st.session_state.timer_duration)
    mins, secs = divmod(remaining, 60)
    
    # Play sound if needed
    if st.session_state.should_play_sound:
        st.session_state.should_play_sound = False
        st.markdown(
            """
            <audio autoplay>
                <source src="data:audio/wav;base64,..." type="audio/wav">
            </audio>
            """,
            unsafe_allow_html=True
        )
    
    # Timer display
    st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: var(--surface-secondary); border-radius: 12px;'>
            <div style='font-size: 3rem; font-weight: bold; color: var(--text-primary);'>
                {mins:02d}:{secs:02d}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.progress(progress)
    
    # Timer controls
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.session_state.timer_paused:
            if st.button("▶️ Resume", use_container_width=True):
                resume_timer()
        else:
            if st.button("⏸️ Pause", use_container_width=True):
                pause_timer()
    
    with col2:
        if st.button("🔄 Restart", use_container_width=True):
            restart_timer()
    
    with col3:
        if st.button("✅ Complete", use_container_width=True):
            complete_exercise()

def main():
    # Initialize session state
    init_session_state()
    
    # App header
    st.markdown("""
        <h1 style="text-align: center; padding: 1rem 0;">
            🧘‍♂️ Health Protocol Dashboard
        </h1>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
            <h3 style="margin-bottom: 1rem;">Today's Focus</h3>
            <p style="color: var(--text-secondary); margin-bottom: 2rem;">
                Choose your wellness activity for this session
            </p>
        """, unsafe_allow_html=True)
        
        # Protocol selector
        selected = st.radio(
            "",
            ["lllt", "mobility"],
            format_func=lambda x: "🔴 Light Therapy (LLLT)" if x == "lllt" else "🧘‍♂️ Movement & Mobility",
            key="protocol_choice",
            label_visibility="collapsed"
        )

    # Main content
    if selected == "lllt":
        display_lllt_protocol()
    else:
        display_mobility_protocol()

def display_lllt_protocol():
    st.header("🔴 Light Therapy Session")
    
    # Protocol tabs
    tab1, tab2, tab3 = st.tabs(["Daily Protocol", "Weekly Schedule", "Progress"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        with col1:
            display_lllt_daily_protocol()
        with col2:
            display_lllt_metrics()
    
    with tab2:
        display_weekly_schedule()
    
    with tab3:
        display_lllt_progress()

def display_mobility_protocol():
    st.header("🧘‍♂️ Movement & Mobility Session")
    
    # Protocol tabs
    tab1, tab2, tab3 = st.tabs(["Exercises", "Progress", "History"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        with col1:
            display_mobility_exercises()
        with col2:
            display_mobility_timer()
    
    with tab2:
        display_mobility_progress()
    
    with tab3:
        display_session_history()

def display_lllt_daily_protocol():
    with st.container():
        st.subheader("Today's Protocol")
        protocols = get_lllt_daily_data()
        
        for protocol in protocols:
            with st.expander(f"{protocol['area']} - {protocol['duration']} mins", expanded=True):
                cols = st.columns([3, 1, 1])
                with cols[0]:
                    st.markdown(f"**Intensity:** {protocol['intensity']}")
                    st.markdown(f"**Notes:** {protocol['notes']}")
                with cols[1]:
                    if st.button("Start", key=f"start_{protocol['area']}"):
                        start_exercise(protocol)
                with cols[2]:
                    if st.button("Complete", key=f"complete_{protocol['area']}"):
                        mark_complete(protocol['area'])

def display_mobility_exercises():
    """Display mobility exercises with improved organization and clarity"""
    exercises = get_phase1_data()
    
    # Group exercises by time of day
    exercise_groups = {
        "morning": [],
        "lunch": [],
        "pre_bed": []
    }
    
    for exercise in exercises:
        if isinstance(exercise, dict):
            time_of_day = exercise.get('Time', 'morning').lower().replace(' ', '_').replace('-', '_')
            exercise_groups[time_of_day].append(exercise)
    
    # Display each group
    for time_of_day, group_exercises in exercise_groups.items():
        if group_exercises:
            st.header(f"{time_of_day.replace('_', ' ').title()} Routine")
            
            for i, exercise in enumerate(group_exercises):
                with st.expander(f"{exercise['Exercise']}", expanded=True):
                    # Exercise title and duration in large, prominent text
                    st.markdown(f"""
                        <div style='background: var(--surface-primary); padding: 1rem; border-radius: 12px; margin-bottom: 1rem;'>
                            <h2 style='margin: 0; color: var(--text-primary); font-size: 1.8rem;'>{exercise['Exercise']}</h2>
                            <p style='margin: 0.5rem 0 0 0; color: var(--accent-primary); font-size: 1.2rem; font-weight: 600;'>
                                {exercise.get('Sets/Reps/Duration', '')}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Timer and controls first if exercise is active
                    if st.session_state.current_exercise and st.session_state.current_exercise.get('Exercise', '') == exercise.get('Exercise', ''):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            if st.session_state.timer_paused:
                                elapsed = st.session_state.pause_time - st.session_state.timer_start
                            else:
                                elapsed = time.time() - st.session_state.timer_start
                            
                            remaining = max(0, st.session_state.timer_duration - int(elapsed))
                            progress = min(1.0, elapsed / st.session_state.timer_duration)
                            mins, secs = divmod(remaining, 60)
                            
                            # Timer display
                            st.markdown(f"""
                                <div style='text-align: center; padding: 1rem; background: var(--surface-secondary); border-radius: 12px;'>
                                    <div style='font-size: 3rem; font-weight: bold; color: var(--text-primary);'>
                                        {mins:02d}:{secs:02d}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            st.progress(progress)
                            
                            if remaining <= 0 and not st.session_state.timer_paused:
                                st.session_state.completed_exercises.add(exercise['Exercise'])
                                st.session_state.current_exercise = None
                                st.rerun()
                        
                        with col2:
                            if st.session_state.timer_paused:
                                if st.button("▶️ Resume", key=f"resume_{time_of_day}_{i}", use_container_width=True):
                                    st.session_state.timer_paused = False
                                    st.session_state.timer_start = time.time() - (st.session_state.pause_time - st.session_state.timer_start)
                                    st.rerun()
                            else:
                                if st.button("⏸️ Pause", key=f"pause_{time_of_day}_{i}", use_container_width=True):
                                    st.session_state.timer_paused = True
                                    st.session_state.pause_time = time.time()
                                    st.rerun()
                            
                            if st.button("🔄 Restart", key=f"restart_{time_of_day}_{i}", use_container_width=True):
                                st.session_state.timer_start = time.time()
                                st.session_state.timer_paused = False
                                st.rerun()
                            
                            if st.button("✅ Complete", key=f"complete_{time_of_day}_{i}", use_container_width=True):
                                st.session_state.completed_exercises.add(exercise['Exercise'])
                                st.session_state.current_exercise = None
                                st.rerun()
                    else:
                        # Start button if exercise is not active
                        if exercise['Exercise'] not in st.session_state.completed_exercises:
                            if st.button("▶️ Start", key=f"start_{time_of_day}_{i}", use_container_width=True):
                                start_exercise(exercise)
                    
                    # Exercise details in tabs
                    tab1, tab2 = st.tabs(["Equipment & Notes", "How to Perform"])
                    
                    with tab1:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("#### Equipment")
                            st.markdown(exercise.get('Equipment', 'None required'))
                        with col2:
                            st.markdown("#### Key Notes")
                            st.markdown(exercise.get('Key Notes', ''))
                    
                    with tab2:
                        if exercise.get('Steps'):
                            for step in exercise['Steps']:
                                st.markdown(f"- {step}")
                            
                            if exercise.get('Demo'):
                                st.markdown(f"[🎥 Watch Demo]({exercise['Demo']})")

def display_mobility_timer():
    if st.session_state.current_exercise:
        exercise = st.session_state.current_exercise
        
        # Timer card with enhanced styling
        display_timer()
        
        # Progress metrics
        progress = len(st.session_state.completed_exercises)
        total = len(get_phase1_data())
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Completed",
                f"{progress}/{total}",
                delta=f"{(progress/total*100):.0f}%",
                delta_color="normal"
            )
        with col2:
            if st.session_state.session_start:
                elapsed = datetime.now() - st.session_state.session_start
                st.metric(
                    "Time",
                    str(elapsed).split('.')[0],
                    delta="Active",
                    delta_color="normal"
                )

def display_lllt_metrics():
    st.subheader("Today's Progress")
    
    # Get metrics
    total_sessions = len(get_lllt_daily_data())
    completed_sessions = len([x for x in st.session_state.completed_exercises if "LLLT" in x])
    
    # Display metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Sessions Completed",
            f"{completed_sessions}/{total_sessions}",
            delta=completed_sessions
        )
    with col2:
        completion_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
        st.metric(
            "Completion Rate",
            f"{completion_rate:.1f}%",
            delta=f"{completion_rate:.1f}%"
        )

def display_weekly_schedule():
    st.subheader("Weekly Schedule")
    schedule = get_weekly_schedule()
    
    # Create schedule table
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    current_day = datetime.now().strftime("%A")
    
    for day in days:
        is_today = day == current_day
        bg_color = "#e8f5e9" if is_today else "#ffffff"
        
        st.markdown(
            f"""
            <div style="background-color: {bg_color}; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
                <h4 style="margin: 0;">{day}</h4>
                <div style="margin-top: 0.5rem;">
                    {'🟢 LLLT Day' if day in schedule['lllt_days'] else '⚪️ Rest Day'}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

def display_lllt_progress():
    st.subheader("Progress Overview")
    
    # Get progress data
    progress_data = {
        "Week 1": 85,
        "Week 2": 90,
        "Week 3": 95,
        "Week 4": 88,
        "Current Week": 92
    }
    
    # Create progress chart
    fig = px.line(
        x=list(progress_data.keys()),
        y=list(progress_data.values()),
        title="Weekly Completion Rate (%)",
        markers=True
    )
    fig.update_layout(
        xaxis_title="Week",
        yaxis_title="Completion Rate (%)",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Display adjustments
    st.subheader("Recent Adjustments")
    adjustments = get_adjustments_data()
    
    for adjustment in adjustments:
        with st.expander(f"📝 {adjustment['date']} - {adjustment['type']}", expanded=False):
            st.markdown(f"**Details:** {adjustment['details']}")
            st.markdown(f"**Impact:** {adjustment['impact']}")

def display_mobility_progress():
    st.subheader("Mobility Progress")
    
    # Example progress data
    progress_data = {
        "Spine Mobility": 4,
        "Hip Flexibility": 3,
        "Shoulder ROM": 4,
        "Ankle Mobility": 2,
        "Wrist Mobility": 3
    }
    
    # Create radar chart
    categories = list(progress_data.keys())
    values = list(progress_data.values())
    
    fig = px.line_polar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        line_close=True
    )
    fig.update_traces(fill='toself')
    st.plotly_chart(fig, use_container_width=True)
    
    # Display metrics
    st.subheader("Key Metrics")
    metrics = get_progress_metrics()
    
    for metric in metrics:
        with st.expander(f"📊 {metric['metric']}", expanded=False):
            st.markdown(f"**Current:** {metric['current']}")
            st.markdown(f"**Target:** {metric['target']}")
            st.markdown(f"**Progress:** {metric['progress']}%")
            st.progress(float(metric['progress']) / 100)

def display_session_history():
    st.subheader("Session History")
    
    # Example session history
    history = [
        {
            "date": "2024-01-25",
            "duration": "45 mins",
            "exercises": 12,
            "notes": "Improved hip mobility, focused on thoracic extension"
        },
        {
            "date": "2024-01-24",
            "duration": "30 mins",
            "exercises": 8,
            "notes": "Quick morning session, emphasized shoulder mobility"
        }
    ]
    
    for session in history:
        with st.expander(f"📅 {session['date']} - {session['duration']}", expanded=False):
            st.markdown(f"**Exercises Completed:** {session['exercises']}")
            st.markdown(f"**Notes:** {session['notes']}")

def mark_complete(area: str):
    """Mark an LLLT session as complete"""
    if f"LLLT_{area}" not in st.session_state.completed_exercises:
        st.session_state.completed_exercises.append(f"LLLT_{area}")
        st.success(f"{area} session completed!")
        st.rerun()

def get_lllt_daily_data():
    """Get LLLT protocol data for the day"""
    return [
        {
            "area": "Head",
            "duration": 15,
            "intensity": "Medium",
            "notes": "Focus on temporal and frontal regions"
        },
        {
            "area": "Neck",
            "duration": 10,
            "intensity": "Low",
            "notes": "Gentle exposure on cervical area"
        },
        {
            "area": "Back",
            "duration": 20,
            "intensity": "High",
            "notes": "Target lower back region"
        }
    ]

def get_weekly_schedule():
    """Get weekly schedule data"""
    return {
        "lllt_days": ["Monday", "Wednesday", "Friday"],
        "rest_days": ["Tuesday", "Thursday", "Saturday", "Sunday"]
    }

def get_adjustments_data():
    """Get recent protocol adjustments"""
    return [
        {
            "date": "2024-01-25",
            "type": "Intensity Increase",
            "details": "Increased head region intensity to medium",
            "impact": "Better response observed"
        },
        {
            "date": "2024-01-20",
            "type": "Duration Adjustment",
            "details": "Extended back treatment by 5 minutes",
            "impact": "Improved recovery time"
        }
    ]

def get_progress_metrics():
    """Get progress tracking metrics"""
    return [
        {
            "metric": "Treatment Consistency",
            "current": "90%",
            "target": "95%",
            "progress": "85"
        },
        {
            "metric": "Session Completion",
            "current": "18/20",
            "target": "20/20",
            "progress": "90"
        }
    ]

if __name__ == "__main__":
    main() 