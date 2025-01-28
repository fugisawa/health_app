#!/usr/bin/env python3
import pandas as pd
import os
from pathlib import Path
import shutil
from datetime import datetime
import json
import hashlib
import sys

class HealthDataProcessor:
    def __init__(self, output_dir=None):
        """Initialize the health data processor with output directory and backup system."""
        # Get the absolute path of the script's directory
        script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        
        # Set default paths relative to script location
        self.output_dir = Path(output_dir) if output_dir else script_dir
        self.backup_dir = self.output_dir / "backups"
        self.archive_dir = self.output_dir / "archive"
        self.metadata_file = self.output_dir / "data_versions.json"
        
        print(f"Output directory: {self.output_dir}")
        print(f"Backup directory: {self.backup_dir}")
        print(f"Archive directory: {self.archive_dir}")
        
        # Create necessary directories
        for directory in [self.output_dir, self.backup_dir, self.archive_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize version tracking
        self.versions = self._load_versions()

    def _load_versions(self):
        """Load version history from metadata file."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_versions(self):
        """Save version history to metadata file."""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.versions, f, indent=2)

    def _create_backup(self, df, name):
        """Create a backup of the DataFrame before saving."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"{name}_{timestamp}.csv"
        df.to_csv(backup_path, index=False)
        return backup_path

    def _calculate_checksum(self, df):
        """Calculate checksum of DataFrame for integrity verification."""
        return hashlib.md5(pd.util.hash_pandas_object(df).values).hexdigest()

    def _archive_old_version(self, file_path):
        """Archive the old version of a file if it exists."""
        if file_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_path = self.archive_dir / f"{file_path.name}_{timestamp}"
            shutil.move(str(file_path), str(archive_path))
            return archive_path
        return None

    def _validate_dataframe(self, df, required_columns, name=""):
        """Enhanced DataFrame validation with type checking and data constraints."""
        # Check required columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns in {name}: {missing_columns}")
        
        # Check for null values
        null_columns = df.columns[df.isnull().any()].tolist()
        if null_columns:
            raise ValueError(f"Null values found in {name} columns: {null_columns}")
        
        # Check for empty strings
        empty_columns = df.columns[(df == "").any()].tolist()
        if empty_columns:
            raise ValueError(f"Empty string values found in {name} columns: {empty_columns}")
        
        # Check for duplicate rows
        if df.duplicated().any():
            raise ValueError(f"Duplicate rows found in {name}")
        
        # Validate specific constraints based on DataFrame type
        if "Time" in df.columns:
            valid_times = {"Post-AM LLLT", "Post-PM LLLT", "Pre-Bed"}
            invalid_times = set(df["Time"]) - valid_times
            if invalid_times:
                raise ValueError(f"Invalid time values in {name}: {invalid_times}")

    def _safe_save_dataframe(self, df, name):
        """Safely save DataFrame with backup and version control."""
        if df.empty:
            print(f"Warning: Skipping {name} as DataFrame is empty")
            return False

        try:
            # Create paths
            file_path = self.output_dir / f"{name}.csv"
            
            # Calculate checksum
            checksum = self._calculate_checksum(df)
            
            # Check if content has changed or file doesn't exist
            should_save = True
            if file_path.exists():
                try:
                    existing_df = pd.read_csv(file_path)
                    existing_checksum = self._calculate_checksum(existing_df)
                    if existing_checksum == checksum:
                        print(f"No changes detected in {name}, skipping save")
                        should_save = False
                except Exception as e:
                    print(f"Error reading existing file {name}.csv: {e}")
                    should_save = True
            else:
                print(f"File {name}.csv doesn't exist, creating it")
                should_save = True
            
            if should_save:
                # Create backup of current version if it exists
                backup_path = self._create_backup(df, name) if file_path.exists() else None
                archive_path = self._archive_old_version(file_path) if file_path.exists() else None
                
                # Save new version
                df.to_csv(file_path, index=False)
                print(f"Saved {name}.csv successfully")
                
                # Update version metadata
                version_info = {
                    "timestamp": datetime.now().isoformat(),
                    "checksum": checksum,
                    "backup_path": str(backup_path) if backup_path else None,
                    "archive_path": str(archive_path) if archive_path else None,
                    "row_count": len(df),
                    "column_count": len(df.columns)
                }
                
                if name not in self.versions:
                    self.versions[name] = []
                self.versions[name].append(version_info)
                self._save_versions()
            
            return True
            
        except Exception as e:
            print(f"Error saving {name}: {e}")
            # If save fails and we have a backup, try to restore from it
            if "backup_path" in locals() and backup_path:
                try:
                    shutil.copy(str(backup_path), str(file_path))
                    print(f"Restored {name} from backup after save failure")
                except Exception as restore_error:
                    print(f"Error restoring from backup: {restore_error}")
            return False

    def create_phase1_morning_df(self):
        """Create Phase 1 (Months 1-6) Morning Mobility DataFrame."""
        try:
            data = [
                {
                    "Exercise": "Dynamic Cat-Cow",
                    "Sets/Reps/Duration": "2 mins",
                    "Equipment": "None",
                    "Key Notes": "Mobilize the entire spine. Inhale to arch, exhale to round.",
                    "Phase": "Foundation",
                    "Session": "Morning"
                },
                {
                    "Exercise": "Dynamic Leg Swings",
                    "Sets/Reps/Duration": "15 reps/side",
                    "Equipment": "None",
                    "Key Notes": "Front/back and lateral swings. Prioritize controlled motion.",
                    "Phase": "Foundation",
                    "Session": "Morning"
                },
                {
                    "Exercise": "90/90 Hip Switch",
                    "Sets/Reps/Duration": "10 reps/side",
                    "Equipment": "None",
                    "Key Notes": "Improve internal/external hip rotation. Keep pelvis neutral.",
                    "Phase": "Foundation",
                    "Session": "Morning"
                },
                {
                    "Exercise": "Baddha Konasana (PNF)",
                    "Sets/Reps/Duration": "3x30s hold",
                    "Equipment": "Yoga blocks",
                    "Key Notes": "Contract hips inward for 5s, relax deeper. Critical for lotus progression.",
                    "Phase": "Foundation",
                    "Session": "Morning"
                }
            ]
            df = pd.DataFrame(data)
            self._validate_dataframe(df, ["Exercise", "Sets/Reps/Duration", "Equipment", "Key Notes", "Phase", "Session"], "phase1_morning")
            return df
        except Exception as e:
            print(f"Error creating Phase 1 Morning DataFrame: {e}")
            return pd.DataFrame()

    def create_phase1_lunch_df(self):
        """Create Phase 1 (Months 1-6) Lunch Mobility DataFrame."""
        try:
            data = [
                {
                    "Exercise": "Wall Angels",
                    "Sets/Reps/Duration": "3x10 reps",
                    "Equipment": "Wall",
                    "Key Notes": "Enhances scapular control and thoracic extension. Keep lower back flat.",
                    "Phase": "Foundation",
                    "Session": "Lunch"
                },
                {
                    "Exercise": "Chair-Assisted Thoracic Extension",
                    "Sets/Reps/Duration": "2x8 reps",
                    "Equipment": "Office chair",
                    "Key Notes": "Arch upper back over chair edge. Prepares for Urdhva Dhanurasana.",
                    "Phase": "Foundation",
                    "Session": "Lunch"
                },
                {
                    "Exercise": "Median Nerve Glides",
                    "Sets/Reps/Duration": "8–10 reps/arm",
                    "Equipment": "None",
                    "Key Notes": "Gentle nerve mobilization for thoracic/shoulder health. No pain.",
                    "Phase": "Foundation",
                    "Session": "Lunch"
                }
            ]
            df = pd.DataFrame(data)
            self._validate_dataframe(df, ["Exercise", "Sets/Reps/Duration", "Equipment", "Key Notes", "Phase", "Session"], "phase1_lunch")
            return df
        except Exception as e:
            print(f"Error creating Phase 1 Lunch DataFrame: {e}")
            return pd.DataFrame()

    def create_phase1_prebed_df(self):
        """Create Phase 1 (Months 1-6) Pre-Bed Mobility DataFrame."""
        try:
            data = [
                {
                    "Exercise": "Nordic Curl Negatives",
                    "Sets/Reps/Duration": "3x5 reps",
                    "Equipment": "Resistance band",
                    "Key Notes": "Eccentric hamstring rehab. Lower slowly (3–5s).",
                    "Phase": "Foundation",
                    "Session": "Pre-Bed"
                },
                {
                    "Exercise": "PNF Pancake Stretch",
                    "Sets/Reps/Duration": "3x30s",
                    "Equipment": "Yoga blocks",
                    "Key Notes": "Contract adductors for 5s, relax deeper. Blocks under knees if needed.",
                    "Phase": "Foundation",
                    "Session": "Pre-Bed"
                }
            ]
            df = pd.DataFrame(data)
            self._validate_dataframe(df, ["Exercise", "Sets/Reps/Duration", "Equipment", "Key Notes", "Phase", "Session"], "phase1_prebed")
            return df
        except Exception as e:
            print(f"Error creating Phase 1 Pre-Bed DataFrame: {e}")
            return pd.DataFrame()

    def create_phase2_morning_df(self):
        """Create Phase 2 (Months 7-12) Morning Mobility DataFrame."""
        try:
            data = [
                {
                    "Exercise": "Advanced Cat-Cow with Thread the Needle",
                    "Sets/Reps/Duration": "3 mins",
                    "Equipment": "None",
                    "Key Notes": "Add thoracic rotation to basic cat-cow. Emphasize control.",
                    "Phase": "Intermediate",
                    "Session": "Morning"
                },
                {
                    "Exercise": "Standing Dynamic Hip CARs",
                    "Sets/Reps/Duration": "10 reps/direction/side",
                    "Equipment": "None",
                    "Key Notes": "Controlled Articular Rotations for hip joint. Full ROM.",
                    "Phase": "Intermediate",
                    "Session": "Morning"
                },
                {
                    "Exercise": "Half-Lotus Prep with Band",
                    "Sets/Reps/Duration": "2x30s/side",
                    "Equipment": "Resistance band",
                    "Key Notes": "External rotation emphasis. Stop if knee pain occurs.",
                    "Phase": "Intermediate",
                    "Session": "Morning"
                }
            ]
            df = pd.DataFrame(data)
            self._validate_dataframe(df, ["Exercise", "Sets/Reps/Duration", "Equipment", "Key Notes", "Phase", "Session"], "phase2_morning")
            return df
        except Exception as e:
            print(f"Error creating Phase 2 Morning DataFrame: {e}")
            return pd.DataFrame()

    def create_phase2_lunch_df(self):
        """Create Phase 2 (Months 7-12) Lunch Mobility DataFrame."""
        try:
            data = [
                {
                    "Exercise": "Bent-Knee Eccentric Sliders",
                    "Sets/Reps/Duration": "3x10 reps/side",
                    "Equipment": "Chair, sliders",
                    "Key Notes": "Hamstring/adductor focus. Control eccentric phase.",
                    "Phase": "Intermediate",
                    "Session": "Lunch"
                },
                {
                    "Exercise": "Side-Lying Thoracic Opener",
                    "Sets/Reps/Duration": "2x45s/side",
                    "Equipment": "Yoga block",
                    "Key Notes": "Progress range as mobility improves. Keep hips stacked.",
                    "Phase": "Intermediate",
                    "Session": "Lunch"
                }
            ]
            df = pd.DataFrame(data)
            self._validate_dataframe(df, ["Exercise", "Sets/Reps/Duration", "Equipment", "Key Notes", "Phase", "Session"], "phase2_lunch")
            return df
        except Exception as e:
            print(f"Error creating Phase 2 Lunch DataFrame: {e}")
            return pd.DataFrame()

    def create_phase2_prebed_df(self):
        """Create Phase 2 (Months 7-12) Pre-Bed Mobility DataFrame."""
        try:
            data = [
                {
                    "Exercise": "IT Band Massage Gun Therapy",
                    "Sets/Reps/Duration": "2 mins/side",
                    "Equipment": "Massage gun",
                    "Key Notes": "Focus on tight spots. Medium intensity setting.",
                    "Phase": "Intermediate",
                    "Session": "Pre-Bed"
                },
                {
                    "Exercise": "Supported Reclined Hero Pose",
                    "Sets/Reps/Duration": "2x60s",
                    "Equipment": "Yoga chair",
                    "Key Notes": "Progress depth gradually. Keep feet pointed straight.",
                    "Phase": "Intermediate",
                    "Session": "Pre-Bed"
                }
            ]
            df = pd.DataFrame(data)
            self._validate_dataframe(df, ["Exercise", "Sets/Reps/Duration", "Equipment", "Key Notes", "Phase", "Session"], "phase2_prebed")
            return df
        except Exception as e:
            print(f"Error creating Phase 2 Pre-Bed DataFrame: {e}")
            return pd.DataFrame()

    def create_phase3_morning_df(self):
        """Create Phase 3 (Months 13-18) Morning Mobility DataFrame."""
        try:
            data = [
                {
                    "Exercise": "Quadruped Thoracic Rotation",
                    "Sets/Reps/Duration": "10 reps/side",
                    "Equipment": "None",
                    "Key Notes": "Full spinal rotation. Keep hips level.",
                    "Phase": "Advanced",
                    "Session": "Morning"
                },
                {
                    "Exercise": "Seated Wide-Legged Forward Fold",
                    "Sets/Reps/Duration": "2x45s",
                    "Equipment": "Yoga strap",
                    "Key Notes": "Focus on adductor length. Keep back straight.",
                    "Phase": "Advanced",
                    "Session": "Morning"
                }
            ]
            df = pd.DataFrame(data)
            self._validate_dataframe(df, ["Exercise", "Sets/Reps/Duration", "Equipment", "Key Notes", "Phase", "Session"], "phase3_morning")
            return df
        except Exception as e:
            print(f"Error creating Phase 3 Morning DataFrame: {e}")
            return pd.DataFrame()

    def create_phase3_lunch_df(self):
        """Create Phase 3 (Months 13-18) Lunch Mobility DataFrame."""
        try:
            data = [
                {
                    "Exercise": "Standing Forward Fold (Bent Knee)",
                    "Sets/Reps/Duration": "2x60s",
                    "Equipment": "Yoga strap",
                    "Key Notes": "Focus on hamstring length. Keep back straight.",
                    "Phase": "Advanced",
                    "Session": "Lunch"
                },
                {
                    "Exercise": "Kettlebell Goblet Cossack Squat",
                    "Sets/Reps/Duration": "2x6 reps/side",
                    "Equipment": "20kg kettlebell",
                    "Key Notes": "Hip mobility under load. Keep chest up.",
                    "Phase": "Advanced",
                    "Session": "Lunch"
                }
            ]
            df = pd.DataFrame(data)
            self._validate_dataframe(df, ["Exercise", "Sets/Reps/Duration", "Equipment", "Key Notes", "Phase", "Session"], "phase3_lunch")
            return df
        except Exception as e:
            print(f"Error creating Phase 3 Lunch DataFrame: {e}")
            return pd.DataFrame()

    def create_phase3_prebed_df(self):
        """Create Phase 3 (Months 13-18) Pre-Bed Mobility DataFrame."""
        try:
            data = [
                {
                    "Exercise": "Legs-Up-The-Wall + Breathing",
                    "Sets/Reps/Duration": "5 mins",
                    "Equipment": "None",
                    "Key Notes": "Focus on diaphragmatic breathing. Relax fully.",
                    "Phase": "Advanced",
                    "Session": "Pre-Bed"
                },
                {
                    "Exercise": "Infrared Mat Therapy",
                    "Sets/Reps/Duration": "10 mins",
                    "Equipment": "Infrared/NIR mat",
                    "Key Notes": "End with relaxation. Use medium intensity setting.",
                    "Phase": "Advanced",
                    "Session": "Pre-Bed"
                }
            ]
            df = pd.DataFrame(data)
            self._validate_dataframe(df, ["Exercise", "Sets/Reps/Duration", "Equipment", "Key Notes", "Phase", "Session"], "phase3_prebed")
            return df
        except Exception as e:
            print(f"Error creating Phase 3 Pre-Bed DataFrame: {e}")
            return pd.DataFrame()

    def create_supplements_df(self):
        """Create Supplements DataFrame."""
        try:
            data = [
                {
                    "Time": "Post-AM LLLT",
                    "Supplement": "Vitamin D3",
                    "Dosage": "5000 IU",
                    "Purpose": "Bone health, immune support",
                    "Notes": "Take with fatty meal"
                },
                {
                    "Time": "Post-PM LLLT",
                    "Supplement": "Magnesium Glycinate",
                    "Dosage": "400mg",
                    "Purpose": "Muscle recovery, sleep support",
                    "Notes": "Take 2-3 hours before bed"
                },
                {
                    "Time": "Pre-Bed",
                    "Supplement": "Zinc Picolinate",
                    "Dosage": "30mg",
                    "Purpose": "Immune support, hormone balance",
                    "Notes": "Take away from other minerals"
                }
            ]
            df = pd.DataFrame(data)
            self._validate_dataframe(df, ["Time", "Supplement", "Dosage", "Purpose", "Notes"], "supplements")
            return df
        except Exception as e:
            print(f"Error creating Supplements DataFrame: {e}")
            return pd.DataFrame()

    def save_dataframes(self):
        """Save all DataFrames to CSV files."""
        results = {}
        
        # Create and save all DataFrames
        dataframes = {
            'phase1_morning_df': self.create_phase1_morning_df(),
            'phase1_lunch_df': self.create_phase1_lunch_df(),
            'phase1_prebed_df': self.create_phase1_prebed_df(),
            'phase2_morning_df': self.create_phase2_morning_df(),
            'phase2_lunch_df': self.create_phase2_lunch_df(),
            'phase2_prebed_df': self.create_phase2_prebed_df(),
            'phase3_morning_df': self.create_phase3_morning_df(),
            'phase3_lunch_df': self.create_phase3_lunch_df(),
            'phase3_prebed_df': self.create_phase3_prebed_df(),
            'supplements_df': self.create_supplements_df()
        }
        
        for name, df in dataframes.items():
            success = self._safe_save_dataframe(df, name)
            results[name] = {
                'success': success,
                'rows': len(df) if not df.empty else 0,
                'columns': len(df.columns) if not df.empty else 0
            }
        
        # Save processing summary
        summary = {
            'timestamp': datetime.now().isoformat(),
            'results': results,
            'total_files': len(results),
            'successful_saves': sum(1 for r in results.values() if r['success'])
        }
        
        with open(self.output_dir / 'processing_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        return results

def main():
    """Process health data and save to CSV files."""
    try:
        processor = HealthDataProcessor()
        results = processor.save_dataframes()
        
        print("\nProcessing Summary:")
        for name, result in results.items():
            status = "✓" if result['success'] else "✗"
            print(f"{status} {name}: {result['rows']} rows, {result['columns']} columns")
        
    except Exception as e:
        print(f"Error processing health data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 