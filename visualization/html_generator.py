import pandas as pd
from typing import Dict, List
import json

class HTMLGenerator:
    """Generate HTML visualizations for health protocols"""
    
    @staticmethod
    def generate_protocol_html(df: pd.DataFrame, title: str) -> str:
        """Generate HTML table with custom styling"""
        html_template = f"""
        <div class="protocol-container">
            <h2>{title}</h2>
            {{table}}
        </div>
        """
        
        styled_df = (df.style
            .set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#f4f4f4')]},
                {'selector': 'td', 'props': [('padding', '8px')]}
            ])
            .hide()
        )
        
        return html_template.format(table=styled_df.to_html())
    
    @staticmethod
    def generate_dashboard(protocols: Dict[str, pd.DataFrame]) -> str:
        """Generate complete HTML dashboard"""
        html_parts = []
        for protocol_name, df in protocols.items():
            html_parts.append(HTMLGenerator.generate_protocol_html(df, protocol_name))
        
        return "\n".join(html_parts)
    
    @staticmethod
    def generate_weekly_schedule(lllt_data: Dict[str, pd.DataFrame], mobility_data: Dict[str, pd.DataFrame]) -> str:
        """Generate a weekly schedule view combining LLLT and mobility protocols"""
        # CSS styles for the weekly schedule
        css = """
        <style>
            .schedule-container {
                font-family: Arial, sans-serif;
                margin: 20px;
            }
            .day-container {
                margin-bottom: 30px;
                border: 1px solid #ddd;
                padding: 15px;
                border-radius: 5px;
            }
            .day-header {
                background-color: #f4f4f4;
                padding: 10px;
                margin: -15px -15px 15px -15px;
                border-radius: 5px 5px 0 0;
                border-bottom: 1px solid #ddd;
            }
            .period {
                margin-bottom: 15px;
            }
            .period h4 {
                color: #444;
                margin-bottom: 8px;
            }
            .protocol {
                background-color: #fff;
                padding: 10px;
                margin-bottom: 5px;
                border-left: 4px solid;
            }
            .lllt {
                border-left-color: #4CAF50;
            }
            .mobility {
                border-left-color: #2196F3;
            }
            .legend {
                margin-bottom: 20px;
                padding: 10px;
                background-color: #f9f9f9;
                border-radius: 5px;
            }
            .legend-item {
                display: inline-block;
                margin-right: 20px;
            }
            .legend-color {
                display: inline-block;
                width: 20px;
                height: 20px;
                margin-right: 5px;
                vertical-align: middle;
            }
        </style>
        """
        
        # Create legend
        legend = """
        <div class="legend">
            <div class="legend-item">
                <span class="legend-color" style="background-color: #4CAF50;"></span>
                LLLT Protocol
            </div>
            <div class="legend-item">
                <span class="legend-color" style="background-color: #2196F3;"></span>
                Mobility Protocol
            </div>
        </div>
        """
        
        # Process LLLT data
        lllt_weekly = lllt_data["weekly"]
        lllt_daily = lllt_data["daily"]
        
        # Get LLLT days from weekly schedule
        lllt_days = []
        for _, row in lllt_weekly.iterrows():
            if "Example Days" in row and isinstance(row["Example Days"], str):
                days = row["Example Days"].replace("/", ",").split(",")
                if row["Day Type"] == "LLLT Days":
                    lllt_days.extend([d.strip()[:3] for d in days])  # Get first 3 letters
        
        # Create schedule structure
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        periods = ["Morning", "Lunch", "Evening", "Pre-Bed"]
        
        html_parts = [css, '<div class="schedule-container">', legend]
        
        for day in days:
            day_short = day[:3]  # First 3 letters
            html_parts.append(f'<div class="day-container">')
            html_parts.append(f'<div class="day-header"><h3>{day}</h3></div>')
            
            for period in periods:
                html_parts.append(f'<div class="period">')
                html_parts.append(f'<h4>{period}</h4>')
                
                # Add LLLT activities
                if day_short in lllt_days:
                    lllt_activities = lllt_daily[lllt_daily["Session"].str.contains(period, case=False, na=False)]
                    if not lllt_activities.empty:
                        for _, activity in lllt_activities.iterrows():
                            html_parts.append(
                                f'<div class="protocol lllt">'
                                f'LLLT: {activity["Target"]} - {activity["Device Mode"]}'
                                f'</div>'
                            )
                
                # Add Mobility activities
                mobility_key = period.lower().replace("-", "_")
                phase_keys = ["phase_phase1", "phase_phase2", "phase_phase3"]
                
                for phase_key in phase_keys:
                    if phase_key in mobility_data and mobility_key in mobility_data[phase_key]:
                        mobility_df = mobility_data[phase_key][mobility_key]
                        if not mobility_df.empty:
                            exercises = mobility_df["Exercise"].tolist()
                            html_parts.append(
                                f'<div class="protocol mobility">'
                                f'Mobility ({phase_key.replace("phase_", "Phase ")}): '
                                f'{", ".join(exercises)}'
                                f'</div>'
                            )
                
                html_parts.append('</div>')
            
            html_parts.append('</div>')
        
        html_parts.append('</div>')
        return "\n".join(html_parts) 