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
from visualization.html_generator import HTMLGenerator
from data.data_manager import DataManager
import pandas as pd

def main():
    # Initialize LLLT Protocol
    lllt_protocol = LLLTProtocol(
        name="LLLT Protocol",
        description="Low-Level Light Therapy Protocol for Hair and Body Optimization",
        daily_schedule=get_lllt_daily_data(),
        supplement_schedule=get_supplement_data(),
        weekly_schedule=get_weekly_schedule()
    )
    
    # Initialize Mobility Protocol
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
    
    # Convert to DataFrames
    lllt_dfs = lllt_protocol.to_dataframe()
    mobility_dfs = mobility_protocol.to_dataframe()
    
    # Initialize HTML generator
    html_generator = HTMLGenerator()
    
    # Prepare LLLT dashboard data
    lllt_dashboard_data = {
        "Daily Schedule": lllt_dfs["daily"],
        "Supplement Schedule": lllt_dfs["supplements"],
        "Weekly Schedule": lllt_dfs["weekly"],
        "Adjustments": pd.DataFrame(get_adjustments_data())
    }
    
    # Generate LLLT dashboard
    lllt_html = html_generator.generate_dashboard(lllt_dashboard_data)
    with open("data/raw/lllt_dashboard.html", "w") as f:
        f.write(lllt_html)
    
    # Prepare Mobility dashboard data
    mobility_dashboard_data = {
        "Phase 1 Morning": mobility_dfs["phase_phase1"]["morning"],
        "Phase 1 Lunch": mobility_dfs["phase_phase1"]["lunch"],
        "Phase 1 Pre-Bed": mobility_dfs["phase_phase1"]["pre_bed"],
        "Phase 2 Morning": mobility_dfs["phase_phase2"]["morning"],
        "Phase 2 Lunch": mobility_dfs["phase_phase2"]["lunch"],
        "Phase 3 Morning": mobility_dfs["phase_phase3"]["morning"],
        "Phase 3 Lunch": mobility_dfs["phase_phase3"]["lunch"],
        "Phase 3 Pre-Bed": mobility_dfs["phase_phase3"]["pre_bed"],
        "Progress Metrics": pd.DataFrame(get_progress_metrics()),
        "Key Adjustments": pd.DataFrame(get_key_adjustments())
    }
    
    # Generate Mobility dashboard
    mobility_html = html_generator.generate_dashboard(mobility_dashboard_data)
    with open("data/raw/mobility_dashboard.html", "w") as f:
        f.write(mobility_html)
    
    # Generate Weekly Schedule
    weekly_schedule_html = html_generator.generate_weekly_schedule(lllt_dfs, mobility_dfs)
    with open("data/raw/weekly_schedule.html", "w") as f:
        f.write(weekly_schedule_html)
    
    # Save protocol data to CSV
    data_manager = DataManager()
    lllt_protocol.save_to_csv("data/raw")
    mobility_protocol.save_to_csv("data/raw")
    
    print("Protocol data and dashboards generated successfully!")

if __name__ == "__main__":
    main() 