"""Theme and styling utilities for the application."""
import streamlit as st

def setup_theme() -> None:
    """Configure the application theme settings."""
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
        /* Base Font Settings */
        .stApp, .css-1d391kg, body {
            font-family: 'Inter', sans-serif;
        }
        
        /* Typography Scale */
        h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            letter-spacing: -0.02em;
            color: var(--text-primary);
        }
        
        h1, .stMarkdown h1 { font-size: 2rem; line-height: 1.2; }
        h2, .stMarkdown h2 { font-size: 1.5rem; line-height: 1.3; }
        h3, .stMarkdown h3 { font-size: 1.25rem; line-height: 1.4; }
        
        p, .stMarkdown p {
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            line-height: 1.6;
            color: var(--text-secondary);
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--border-color);
            padding: 2rem 1rem;
        }
        
        section[data-testid="stSidebar"] .stRadio {
            margin: 1rem 0;
        }
        
        section[data-testid="stSidebar"] .stRadio > label {
            font-size: 1.125rem;
            font-weight: 500;
            color: var(--text-primary);
            margin-bottom: 1rem;
        }
        
        section[data-testid="stSidebar"] .stRadio [role="radiogroup"] {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        
        section[data-testid="stSidebar"] .stRadio [role="radio"] {
            background-color: var(--surface-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1rem;
            transition: all 0.2s ease;
            cursor: pointer;
        }
        
        section[data-testid="stSidebar"] .stRadio [role="radio"]:hover {
            background-color: var(--surface-hover);
            transform: translateY(-2px);
        }
        
        section[data-testid="stSidebar"] .stRadio [aria-checked="true"] {
            background-color: var(--primary-button-bg);
            color: var(--primary-button-text);
            border-color: var(--primary-button-bg);
        }
        
        /* Success Message Styling */
        .element-container .stAlert {
            border-radius: 12px;
            border: none;
            padding: 1rem;
            margin: 1rem 0;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .element-container .stAlert [data-testid="stMarkdownContainer"] {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        /* Tooltip Styling */
        [data-tooltip]:before {
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            padding: 0.5rem 1rem;
            background-color: var(--surface-secondary);
            color: var(--text-primary);
            border-radius: 6px;
            font-size: 0.875rem;
            white-space: nowrap;
            opacity: 0;
            visibility: hidden;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            z-index: 1000;
        }
        
        [data-tooltip]:hover:before {
            opacity: 1;
            visibility: visible;
        }
        </style>
    """, unsafe_allow_html=True)

def apply_custom_css() -> None:
    """Apply custom CSS styling."""
    st.markdown("""
        <style>
        /* Custom CSS Variables */
        :root {
            /* Primary Colors */
            --primary-button-bg: #5A70DD;
            --primary-button-hover: #4F63BF;
            --primary-button-text: #FFFFFF;
            
            /* Success Colors */
            --success-button-bg: #4AD295;
            --success-button-hover: #36B581;
            --success-button-text: #FFFFFF;
            
            /* Disabled Colors */
            --disabled-button-bg: #E0E0E0;
            --disabled-button-text: #9E9E9E;
            
            /* Surface Colors */
            --surface-primary: #F8F9FD;
            --surface-secondary: #FFFFFF;
            --surface-hover: #F1F5FF;
            --sidebar-bg: #1C233A;
            
            /* Text Colors */
            --text-primary: #1A1F36;
            --text-secondary: #4A5568;
            
            /* Border Colors */
            --border-color: #E2E8F0;
            
            /* Focus Colors */
            --focus-ring-color: rgba(90, 112, 221, 0.4);
            
            /* Tab Colors */
            --tab-bg: #2F365F;
            --tab-active: #5A70DD;
        }
        
        /* Tab Styles */
        .stTabs {
            margin-top: 1rem;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background-color: var(--surface-primary);
            padding: 0.5rem;
            border-radius: 12px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: var(--tab-bg);
            border-radius: 8px;
            color: var(--primary-button-text);
            padding: 0.5rem 1rem;
            font-weight: 500;
            border: none;
            transition: all 0.2s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: var(--primary-button-hover);
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--tab-active) !important;
            color: var(--primary-button-text) !important;
        }
        
        /* Button Colors */
        .stButton > button {
            background-color: var(--primary-button-bg);
            color: var(--primary-button-text);
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            font-family: 'Inter', sans-serif;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            font-size: 0.875rem;
            letter-spacing: 0.01em;
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button:hover {
            background-color: var(--primary-button-hover);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(90, 112, 221, 0.2);
        }
        
        .stButton > button:active {
            transform: translateY(0);
        }
        
        /* Success Button */
        .stButton > button[data-testid*="complete"] {
            background-color: var(--success-button-bg);
            min-width: 120px;
        }
        
        .stButton > button[data-testid*="complete"]:hover {
            background-color: var(--success-button-hover);
        }
        
        /* Start Button */
        .stButton > button[data-testid*="start"] {
            min-width: 120px;
        }
        
        /* Disabled Button */
        .stButton > button:disabled {
            background-color: var(--disabled-button-bg);
            color: var(--disabled-button-text);
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        
        /* Button Focus State */
        .stButton > button:focus {
            box-shadow: 0 0 0 2px var(--focus-ring-color);
            outline: none;
        }
        
        /* Button Loading State */
        .stButton > button.running {
            background-color: var(--primary-button-hover);
            cursor: wait;
        }
        
        .stButton > button.running:after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.2),
                transparent
            );
            animation: loading 1.5s infinite;
        }
        
        @keyframes loading {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        /* Additional Styles */
        .stProgress > div > div {
            background-color: var(--primary-button-bg);
            height: 6px;
            border-radius: 3px;
        }
        
        .stMetric {
            background-color: var(--surface-primary);
            padding: 1.25rem;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            transition: transform 0.2s ease;
        }
        
        .stMetric:hover {
            transform: translateY(-2px);
        }
        
        .stMetric label {
            color: var(--text-secondary);
            font-size: 0.875rem;
            font-weight: 500;
            letter-spacing: 0.01em;
        }
        
        .stMetric [data-testid="stMetricValue"] {
            color: var(--text-primary);
            font-size: 1.5rem;
            font-weight: 600;
            letter-spacing: -0.01em;
            margin-top: 0.25rem;
        }
        
        .stMetric [data-testid="stMetricDelta"] {
            color: var(--success-button-bg);
            font-size: 0.875rem;
            font-weight: 500;
            margin-top: 0.25rem;
        }
        
        /* Container Styles */
        div[data-testid="stVerticalBlock"] > div {
            background-color: var(--surface-secondary);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            margin-bottom: 1rem;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        div[data-testid="stVerticalBlock"] > div:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        
        /* Text Selection */
        ::selection {
            background-color: var(--primary-button-bg);
            color: var(--primary-button-text);
        }
        </style>
    """, unsafe_allow_html=True) 