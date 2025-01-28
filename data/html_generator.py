import pandas as pd
from datetime import datetime
import os

# CSS Styles
CSS_STYLES = """
<style>
    body {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        line-height: 1.6;
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        background-color: #f5f7fa;
        color: #2c3e50;
    }
    
    .header {
        text-align: center;
        margin-bottom: 30px;
        padding: 20px;
        background: linear-gradient(135deg, #2c3e50, #3498db);
        color: white;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .date {
        font-size: 0.9em;
        color: #95a5a6;
        margin-top: 10px;
    }
    
    .section {
        background: white;
        padding: 25px;
        margin-bottom: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .section h2 {
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
        background: white;
    }
    
    th {
        background: #3498db;
        color: white;
        padding: 12px;
        text-align: left;
    }
    
    td {
        padding: 12px;
        border-bottom: 1px solid #ecf0f1;
    }
    
    tr:hover {
        background: #f8f9fa;
    }
    
    .info-box {
        background: #e8f4f8;
        padding: 15px;
        border-left: 4px solid #3498db;
        margin: 15px 0;
    }
    
    .equipment-list {
        list-style: none;
        padding: 0;
    }
    
    .equipment-list li {
        padding: 8px 0;
        border-bottom: 1px dashed #ecf0f1;
    }
    
    .equipment-list li:last-child {
        border-bottom: none;
    }
    
    .supplements {
        background: #f0faf0;
        padding: 15px;
        border-left: 4px solid #27ae60;
    }
</style>
"""

# Load the data
lllt_supplements_df = pd.read_csv('data/lllt_supplements.csv')
lllt_daily_df = pd.read_csv('data/lllt_daily.csv')

# Foundation Phase Mobility Data (from notebook)
foundation_mobility = [
    {
        "Exercise": "Camel Pose (Dynamic Pulses)",
        "Sets/Reps/Duration": "3x8 reps",
        "Equipment": "None",
        "Key Notes": "Pulse into backbend with hands on heels. Focus on thoracic extension."
    },
    {
        "Exercise": "Scapular Push-Ups",
        "Sets/Reps/Duration": "3x10 reps",
        "Equipment": "None",
        "Key Notes": "Strengthen serratus anterior for Bakasana and arm balances."
    }
]

def create_html_content(day_type, phase_name, supplements_data, mobility_data):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Health Protocol - {day_type}</title>
        {CSS_STYLES}
    </head>
    <body>
        <div class="header">
            <h1>Health Protocol - {day_type}</h1>
            <div class="date">Last updated: {datetime.now().strftime('%B %d, %Y')}</div>
        </div>
        
        <div class="section">
            <h2>Daily Overview</h2>
            <div class="info-box">
                <p><strong>Day Type:</strong> {day_type}</p>
                <p><strong>Phase:</strong> {phase_name}</p>
            </div>
        </div>
        
        <div class="section">
            <h2>LLLT Protocol</h2>
            <table>
                <tr>
                    <th>Time</th>
                    <th>Supplements</th>
                    <th>Purpose</th>
                </tr>
    """
    
    for _, row in supplements_data.iterrows():
        html_content += f"""
                <tr>
                    <td>{row['Time']}</td>
                    <td>{row['Supplements']}</td>
                    <td>{row['Purpose']}</td>
                </tr>
        """
    
    html_content += """
            </table>
        </div>
        
        <div class="section">
            <h2>Mobility Exercises</h2>
            <table>
                <tr>
                    <th>Exercise</th>
                    <th>Sets/Reps/Duration</th>
                    <th>Equipment</th>
                    <th>Key Notes</th>
                </tr>
    """
    
    for exercise in mobility_data:
        html_content += f"""
                <tr>
                    <td>{exercise['Exercise']}</td>
                    <td>{exercise['Sets/Reps/Duration']}</td>
                    <td>{exercise['Equipment']}</td>
                    <td>{exercise['Key Notes']}</td>
                </tr>
        """
    
    html_content += """
            </table>
        </div>
        
        <div class="section">
            <h2>Important Notes</h2>
            <div class="supplements">
                <p><strong>Supplement Timing:</strong> Take supplements as indicated in the LLLT Protocol table above.</p>
                <p><strong>Hydration:</strong> Maintain proper hydration throughout the day.</p>
                <p><strong>Rest:</strong> Ensure adequate rest between exercises and follow the prescribed order.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

# Create output directory
output_dir = 'data/protocols'
os.makedirs(output_dir, exist_ok=True)

# Generate HTML files for foundation phase
for _, day in lllt_daily_df.iterrows():
    day_type = day['Day Type']
    
    # Create the HTML content
    html_content = create_html_content(
        day_type,
        "Foundation Phase",
        lllt_supplements_df,
        foundation_mobility
    )
    
    # Save the file
    filename = f"{output_dir}/foundation_{day_type.lower().replace(' ', '_')}.html"
    with open(filename, 'w') as f:
        f.write(html_content)

print("HTML files have been generated for the Foundation Phase in the data/protocols directory.") 