#!/usr/bin/env python3
import pandas as pd
from pathlib import Path
import jinja2
from datetime import datetime
import json
import sys
import subprocess
import os

class ProtocolHTMLGenerator:
    def __init__(self, data_dir=None, output_dir=None):
        """Initialize the HTML generator with data and output directories."""
        # Get the absolute path of the script's directory
        script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        
        # Set default paths relative to script location
        self.data_dir = Path(data_dir) if data_dir else script_dir
        self.output_dir = Path(output_dir) if output_dir else script_dir / "protocols"
        
        print(f"Data directory: {self.data_dir}")
        print(f"Output directory: {self.output_dir}")
        
        # Create necessary directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure data files exist
        self._ensure_data_files()
        
        # Load all DataFrames
        try:
            self._load_dataframes()
        except Exception as e:
            print(f"Error loading data files: {e}")
            print("Retrying data file generation...")
            self._ensure_data_files(force_regenerate=True)
            self._load_dataframes()

    def _load_dataframes(self):
        """Load all DataFrames from CSV files."""
        dataframes = {
            'phase1_morning_df': 'phase1_morning_df.csv',
            'phase1_lunch_df': 'phase1_lunch_df.csv',
            'phase1_prebed_df': 'phase1_prebed_df.csv',
            'phase2_morning_df': 'phase2_morning_df.csv',
            'phase2_lunch_df': 'phase2_lunch_df.csv',
            'phase2_prebed_df': 'phase2_prebed_df.csv',
            'phase3_morning_df': 'phase3_morning_df.csv',
            'phase3_lunch_df': 'phase3_lunch_df.csv',
            'phase3_prebed_df': 'phase3_prebed_df.csv',
            'supplements_df': 'supplements_df.csv'
        }
        
        for attr_name, filename in dataframes.items():
            file_path = self.data_dir / filename
            if not file_path.exists():
                raise FileNotFoundError(f"Missing required file: {file_path}")
            setattr(self, attr_name, pd.read_csv(file_path))
            print(f"Loaded {filename}")

    def _ensure_data_files(self, force_regenerate=False):
        """Ensure all required CSV files exist by running health.py if needed."""
        required_files = [
            "phase1_morning_df.csv", "phase1_lunch_df.csv", "phase1_prebed_df.csv",
            "phase2_morning_df.csv", "phase2_lunch_df.csv", "phase2_prebed_df.csv",
            "phase3_morning_df.csv", "phase3_lunch_df.csv", "phase3_prebed_df.csv",
            "supplements_df.csv"
        ]
        
        missing_files = [
            file for file in required_files 
            if not (self.data_dir / file).exists()
        ]
        
        if missing_files or force_regenerate:
            if force_regenerate:
                print("Forcing regeneration of all data files...")
            else:
                print(f"Missing data files: {missing_files}")
            print("Running health.py to generate required files...")
            
            health_script = self.data_dir / "health.py"
            if not health_script.exists():
                raise FileNotFoundError(
                    f"health.py not found in {self.data_dir}. "
                    "Please ensure health.py is in the same directory as html_generator.py"
                )
            
            try:
                # Change to the script directory before running health.py
                original_dir = os.getcwd()
                os.chdir(self.data_dir)
                
                result = subprocess.run(
                    [sys.executable, str(health_script)],
                    capture_output=True,
                    text=True,
                    check=True
                )
                print("Data files generated successfully")
                print("health.py output:")
                print(result.stdout)
                
                # Verify files were created
                still_missing = [
                    file for file in required_files 
                    if not (self.data_dir / file).exists()
                ]
                if still_missing:
                    raise FileNotFoundError(
                        f"Files still missing after running health.py: {still_missing}"
                    )
                
            except subprocess.CalledProcessError as e:
                print(f"Error running health.py: {e}")
                print("Error output:")
                print(e.stderr)
                raise
            finally:
                # Restore original directory
                os.chdir(original_dir)

    def _create_html_template(self):
        """Create the base HTML template with enhanced CSS styling."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>{{ title }}</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                :root {
                    --primary-color: #2c3e50;
                    --secondary-color: #3498db;
                    --background-color: #f5f5f5;
                    --card-background: #ffffff;
                    --text-color: #333333;
                    --border-color: #e0e0e0;
                    --highlight-color: #fff3cd;
                    --success-color: #28a745;
                }

                body {
                    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    background-color: var(--background-color);
                    color: var(--text-color);
                }

                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: var(--card-background);
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }

                h1 {
                    color: var(--primary-color);
                    text-align: center;
                    font-size: 2.5em;
                    margin-bottom: 30px;
                    border-bottom: 3px solid var(--secondary-color);
                    padding-bottom: 15px;
                }

                h2 {
                    color: var(--primary-color);
                    font-size: 1.8em;
                    margin-top: 40px;
                    margin-bottom: 20px;
                }

                h3 {
                    color: var(--secondary-color);
                    font-size: 1.4em;
                    margin-top: 25px;
                }

                .phase-header {
                    background-color: var(--primary-color);
                    color: white;
                    padding: 15px;
                    border-radius: 10px;
                    margin: 30px 0 20px;
                }

                .session-block {
                    background-color: var(--card-background);
                    border: 1px solid var(--border-color);
                    border-radius: 10px;
                    padding: 20px;
                    margin: 20px 0;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                }

                table {
                    width: 100%;
                    border-collapse: separate;
                    border-spacing: 0;
                    margin: 20px 0;
                    background-color: var(--card-background);
                    border-radius: 10px;
                    overflow: hidden;
                }

                th, td {
                    padding: 15px;
                    text-align: left;
                    border-bottom: 1px solid var(--border-color);
                }

                th {
                    background-color: var(--secondary-color);
                    color: white;
                    font-weight: 600;
                }

                tr:last-child td {
                    border-bottom: none;
                }

                tr:nth-child(even) {
                    background-color: rgba(0, 0, 0, 0.02);
                }

                .exercise-card {
                    background-color: var(--card-background);
                    border: 1px solid var(--border-color);
                    border-radius: 10px;
                    padding: 20px;
                    margin: 15px 0;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                }

                .exercise-card h4 {
                    color: var(--secondary-color);
                    margin: 0 0 15px 0;
                    font-size: 1.2em;
                }

                .key-notes {
                    background-color: var(--highlight-color);
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 0 5px 5px 0;
                }

                .equipment-list {
                    background-color: #e8f4f8;
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                }

                .equipment-list ul {
                    list-style-type: none;
                    padding: 0;
                    margin: 0;
                }

                .equipment-list li {
                    padding: 8px 0;
                    border-bottom: 1px solid var(--border-color);
                }

                .equipment-list li:last-child {
                    border-bottom: none;
                }

                .timestamp {
                    text-align: right;
                    color: #666;
                    font-size: 0.9em;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid var(--border-color);
                }

                .nav-links {
                    display: flex;
                    justify-content: center;
                    gap: 20px;
                    margin: 30px 0;
                }

                .nav-links a {
                    color: var(--secondary-color);
                    text-decoration: none;
                    padding: 10px 20px;
                    border: 2px solid var(--secondary-color);
                    border-radius: 5px;
                    transition: all 0.3s ease;
                }

                .nav-links a:hover {
                    background-color: var(--secondary-color);
                    color: white;
                }

                @media (max-width: 768px) {
                    .container {
                        padding: 15px;
                    }

                    table {
                        display: block;
                        overflow-x: auto;
                    }

                    .nav-links {
                        flex-direction: column;
                        align-items: center;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                {{ content }}
                <div class="timestamp">
                    Generated on: {{ timestamp }}
                </div>
            </div>
        </body>
        </html>
        """

    def generate_phase_protocol(self, phase_number, phase_name):
        """Generate HTML for a specific phase's mobility protocol."""
        morning_df = getattr(self, f"phase{phase_number}_morning_df")
        lunch_df = getattr(self, f"phase{phase_number}_lunch_df")
        prebed_df = getattr(self, f"phase{phase_number}_prebed_df")
        
        content = f"""
        <h1>Phase {phase_number} - {phase_name} Protocol</h1>
        <div class="phase-header">
            <h2>Months {(phase_number-1)*6 + 1}-{phase_number*6}</h2>
        </div>
        """
        
        for session_name, df in [
            ("Morning", morning_df),
            ("Lunch", lunch_df),
            ("Pre-Bed", prebed_df)
        ]:
            equipment_needed = sorted(list(set(
                equipment for equipment in df["Equipment"].unique()
                if equipment != "None"
            )))
            
            content += f"""
            <div class="session-block">
                <h3>{session_name} Session</h3>
                
                <div class="equipment-list">
                    <h4>Required Equipment</h4>
                    <ul>
                        {chr(10).join(f'<li>{item}</li>' for item in equipment_needed)}
                    </ul>
                </div>
                
                <h4>Exercise Sequence</h4>
            """
            
            for idx, exercise in df.iterrows():
                content += f"""
                <div class="exercise-card">
                    <h4>{idx + 1}. {exercise['Exercise']}</h4>
                    <table>
                        <tr>
                            <th>Parameter</th>
                            <th>Details</th>
                        </tr>
                        <tr>
                            <td>Sets/Reps/Duration</td>
                            <td>{exercise['Sets/Reps/Duration']}</td>
                        </tr>
                        <tr>
                            <td>Equipment</td>
                            <td>{exercise['Equipment']}</td>
                        </tr>
                    </table>
                    <div class="key-notes">
                        <strong>Key Notes:</strong> {exercise['Key Notes']}
                    </div>
                </div>
                """
            
            content += "</div>"
        
        template = jinja2.Template(self._create_html_template())
        html = template.render(
            title=f"Phase {phase_number} - {phase_name} Protocol",
            content=content,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        output_file = self.output_dir / f"phase{phase_number}_protocol.html"
        with open(output_file, 'w') as f:
            f.write(html)
        
        return output_file

    def generate_supplements_protocol(self):
        """Generate HTML for supplements protocol."""
        content = """
        <h1>Supplements Protocol</h1>
        
        <div class="session-block">
            <table>
                <tr>
                    <th>Time</th>
                    <th>Supplement</th>
                    <th>Dosage</th>
                    <th>Purpose</th>
                    <th>Notes</th>
                </tr>
        """
        
        for _, supplement in self.supplements_df.iterrows():
            content += f"""
                <tr>
                    <td>{supplement['Time']}</td>
                    <td>{supplement['Supplement']}</td>
                    <td>{supplement['Dosage']}</td>
                    <td>{supplement['Purpose']}</td>
                    <td>{supplement['Notes']}</td>
                </tr>
            """
        
        content += """
            </table>
        </div>
        """
        
        template = jinja2.Template(self._create_html_template())
        html = template.render(
            title="Supplements Protocol",
            content=content,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        output_file = self.output_dir / "supplements_protocol.html"
        with open(output_file, 'w') as f:
            f.write(html)
        
        return output_file

    def generate_all_protocols(self):
        """Generate all protocol HTML files."""
        generated_files = []
        
        # Generate phase protocols
        phases = [
            (1, "Foundation"),
            (2, "Intermediate"),
            (3, "Advanced")
        ]
        
        for phase_number, phase_name in phases:
            file = self.generate_phase_protocol(phase_number, phase_name)
            generated_files.append(str(file))
        
        # Generate supplements protocol
        file = self.generate_supplements_protocol()
        generated_files.append(str(file))
        
        # Create index page
        index_content = """
        <h1>Health Protocols Index</h1>
        
        <div class="nav-links">
        """
        
        for phase_number, phase_name in phases:
            filename = f"phase{phase_number}_protocol.html"
            index_content += f'<a href="{filename}">Phase {phase_number} - {phase_name}</a>'
        
        index_content += '<a href="supplements_protocol.html">Supplements Protocol</a>'
        index_content += "</div>"
        
        template = jinja2.Template(self._create_html_template())
        index_html = template.render(
            title="Health Protocols Index",
            content=index_content,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        index_file = self.output_dir / "index.html"
        with open(index_file, 'w') as f:
            f.write(index_html)
        
        generated_files.append(str(index_file))
        
        return generated_files

def main():
    """Generate all protocol HTML files."""
    try:
        print("Initializing Protocol HTML Generator...")
        generator = ProtocolHTMLGenerator()
        
        print("Generating protocol files...")
        files = generator.generate_all_protocols()
        
        print("\nSuccessfully generated protocol files:")
        for file in files:
            print(f"- {file}")
        
        print("\nYou can now open index.html in your browser to view all protocols.")
        
    except Exception as e:
        print(f"Error generating protocols: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 