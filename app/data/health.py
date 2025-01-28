#!/usr/bin/env python3
import pandas as pd
import os
from pathlib import Path
import shutil
from datetime import datetime
import json
import hashlib
import sys
from typing import Dict, List, Any

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

def get_current_phase() -> str:
    """Get the current phase based on progress."""
    # TODO: Implement phase progression logic
    return "Phase 1"

def get_current_session() -> str:
    """Get the current session based on time of day."""
    hour = datetime.now().hour
    
    if 5 <= hour < 11:
        return "morning"
    elif 11 <= hour < 16:
        return "lunch"
    else:
        return "pre_bed"

def get_phase1_exercises() -> Dict[str, List[Dict[str, Any]]]:
    """Return Phase 1 (Months 1-6) mobility protocol data."""
    return {
        "morning": [
            {
                "name": "Dynamic Cat-Cow",
                "sets_reps": "2 mins",
                "equipment": "None",
                "notes": "Mobilize the entire spine. Inhale to arch, exhale to round."
            },
            {
                "name": "Dynamic Leg Swings",
                "sets_reps": "15 reps/side",
                "equipment": "None",
                "notes": "Front/back and lateral swings. Prioritize controlled motion."
            },
            {
                "name": "90/90 Hip Switch",
                "sets_reps": "10 reps/side",
                "equipment": "None",
                "notes": "Improve internal/external hip rotation. Keep pelvis neutral."
            },
            {
                "name": "Baddha Konasana (PNF)",
                "sets_reps": "3x30s hold",
                "equipment": "Yoga blocks",
                "notes": "Contract hips inward for 5s, relax deeper. Critical for lotus progression."
            },
            {
                "name": "Half-Lotus Prep with Band",
                "sets_reps": "2x30s/side",
                "equipment": "Resistance band",
                "notes": "Gently traction foot into external rotation. Avoid knee pain."
            },
            {
                "name": "Quadruped Thoracic Rotation",
                "sets_reps": "10 reps/side",
                "equipment": "None",
                "notes": "Enhance spinal rotation for twists like Marichyasana. Exhale into rotation."
            },
            {
                "name": "Seated Wide-Legged Forward Fold",
                "sets_reps": "2x45s",
                "equipment": "Yoga strap",
                "notes": "Targets adductors for Upavistha Konasana. Keep knees bent if tight."
            },
            {
                "name": "Supported Bridge Pose",
                "sets_reps": "2x60s",
                "equipment": "Yoga block",
                "notes": "Passive thoracic extension for backbend prep. Block under sacrum."
            },
            {
                "name": "Foam Roller IT Band Release",
                "sets_reps": "2 mins/side",
                "equipment": "Foam roller",
                "notes": "Slow rolling + pauses. Avoid bony areas."
            },
            {
                "name": "Dynamic Pigeon Pose",
                "sets_reps": "8 reps/side",
                "equipment": "None",
                "notes": "Pulse gently to open hips. Focus on glute/hip flexor mobility."
            },
            {
                "name": "Scapular Wall Slides",
                "sets_reps": "3x10 reps",
                "equipment": "Wall",
                "notes": "Improve shoulder/scapular control for arm balances."
            },
            {
                "name": "Supine Spinal Twist",
                "sets_reps": "1 min/side",
                "equipment": "None",
                "notes": "Release lower back tension. Keep shoulders grounded."
            }
        ],
        "lunch": [
            {
                "name": "Wall Angels",
                "sets_reps": "3x10 reps",
                "equipment": "Wall",
                "notes": "Enhances scapular control and thoracic extension. Keep lower back flat."
            },
            {
                "name": "Chair-Assisted Thoracic Extension",
                "sets_reps": "2x8 reps",
                "equipment": "Office chair",
                "notes": "Arch upper back over chair edge. Prepares for Urdhva Dhanurasana."
            },
            {
                "name": "Median Nerve Glides",
                "sets_reps": "8–10 reps/arm",
                "equipment": "None",
                "notes": "Gentle nerve mobilization for thoracic/shoulder health. No pain."
            },
            {
                "name": "Bent-Knee Eccentric Sliders",
                "sets_reps": "3x10 reps/side",
                "equipment": "Chair/sliders",
                "notes": "Rehab for hamstring tendinopathy. Control eccentric phase."
            },
            {
                "name": "Side-Lying Thoracic Opener",
                "sets_reps": "2x45s/side",
                "equipment": "Yoga block",
                "notes": "Stretch chest/shoulders. Block under ribcage for support."
            },
            {
                "name": "Standing Forward Fold (Bent Knee)",
                "sets_reps": "2x60s",
                "equipment": "Yoga strap",
                "notes": "Safe hamstring stretch. Keep knees bent to protect tendons."
            },
            {
                "name": "Kettlebell Goblet Cossack Squat",
                "sets_reps": "2x6 reps/side",
                "equipment": "20kg kettlebell",
                "notes": "Loaded hip mobility for Utthita Parsvakonasana. Go slow."
            },
            {
                "name": "Diaphragmatic Breathing",
                "sets_reps": "5 mins",
                "equipment": "None",
                "notes": "Activates parasympathetic nervous system. Inhale 4s, exhale 6s."
            },
            {
                "name": "Scapular Push-Ups",
                "sets_reps": "3x10 reps",
                "equipment": "None",
                "notes": "Strengthen serratus anterior for shoulder stability."
            },
            {
                "name": "Prone Cobra",
                "sets_reps": "3x10 reps",
                "equipment": "None",
                "notes": "Strengthen spinal extensors. Lift chest and legs while squeezing glutes."
            },
            {
                "name": "Foam Roll Thoracic Spine",
                "sets_reps": "2 mins",
                "equipment": "Foam roller",
                "notes": "Roll mid-back to improve extension."
            },
            {
                "name": "Child's Pose with Side Reach",
                "sets_reps": "1 min/side",
                "equipment": "None",
                "notes": "Stretch lats and improve thoracic rotation."
            }
        ],
        "pre_bed": [
            {
                "name": "Nordic Curl Negatives",
                "sets_reps": "3x5 reps",
                "equipment": "Resistance band",
                "notes": "Eccentric hamstring rehab. Lower slowly (3–5s)."
            },
            {
                "name": "PNF Pancake Stretch",
                "sets_reps": "3x30s",
                "equipment": "Yoga blocks",
                "notes": "Contract adductors for 5s, relax deeper. Blocks under knees if needed."
            },
            {
                "name": "IT Band Massage Gun Therapy",
                "sets_reps": "2 mins/side",
                "equipment": "Massage gun",
                "notes": "Glide along lateral thigh. Avoid direct pressure on bone."
            },
            {
                "name": "Supported Reclined Hero Pose",
                "sets_reps": "2x60s",
                "equipment": "Yoga chair",
                "notes": "Stretch quads/hip flexors. Use chair for depth control."
            },
            {
                "name": "Legs-Up-The-Wall + Breathing",
                "sets_reps": "5 mins",
                "equipment": "None",
                "notes": "Enhances circulation and parasympathetic tone."
            },
            {
                "name": "Infrared Mat Therapy",
                "sets_reps": "10 mins",
                "equipment": "Infrared/NIR mat",
                "notes": "Boosts tissue healing. Focus on lower back/hips."
            },
            {
                "name": "Yin Yoga Frog Pose",
                "sets_reps": "3x90s",
                "equipment": "Yoga blocks",
                "notes": "Passive adductor stretch. Blocks under knees for support."
            },
            {
                "name": "Supine Bound Angle",
                "sets_reps": "5 mins",
                "equipment": "Strap",
                "notes": "Passive hip/internal rotation stretch. Strap around thighs for support."
            },
            {
                "name": "Lacrosse Ball Glute Release",
                "sets_reps": "2 mins/side",
                "equipment": "Lacrosse ball",
                "notes": "Target gluteus medius/minimus for hip stability."
            },
            {
                "name": "Gentle Neck Release",
                "sets_reps": "1 min/side",
                "equipment": "None",
                "notes": "Tilt head side-to-side to relieve tension."
            },
            {
                "name": "Alternate Nostril Breathing",
                "sets_reps": "5 mins",
                "equipment": "None",
                "notes": "Balance the nervous system and reduce stress."
            },
            {
                "name": "Child's Pose",
                "sets_reps": "2 mins",
                "equipment": "Mat",
                "notes": "Final relaxation. Focus on deep breathing."
            }
        ]
    }

def get_phase2_exercises() -> Dict[str, List[Dict[str, Any]]]:
    """Return Phase 2 (Months 7-12) mobility protocol data."""
    return {
        "morning": [
            {
                "name": "Sun Salutation A (Full Vinyasa)",
                "sets_reps": "5 rounds",
                "equipment": "None",
                "notes": "Link breath to movement. Focus on smooth transitions."
            },
            {
                "name": "Lizard Pose with PNF",
                "sets_reps": "3x30s/side",
                "equipment": "Yoga blocks",
                "notes": "Contract front hip into block for 5s, relax deeper. Targets Hanumanasana prep."
            },
            {
                "name": "Marichyasana C Prep (Strap-Assisted)",
                "sets_reps": "3x30s/side",
                "equipment": "Strap",
                "notes": "Loop strap around foot and opposite hip to simulate bind. Rotate spine actively."
            },
            {
                "name": "Kettlebell Overhead Squat Hold",
                "sets_reps": "3x20s/side",
                "equipment": "20kg kettlebell",
                "notes": "Loaded shoulder/hip mobility for Utkatasana. Keep core braced."
            },
            {
                "name": "Dolphin Push-Ups",
                "sets_reps": "3x8 reps",
                "equipment": "None",
                "notes": "Strengthen shoulders and core for Pincha Mayurasana. Lower chest toward floor."
            },
            {
                "name": "Standing Splits (Active Pulses)",
                "sets_reps": "3x10 pulses/side",
                "equipment": "Wall",
                "notes": "Build hamstring strength in lengthened position. Avoid bouncing."
            },
            {
                "name": "Kapotasana Prep (Wall Walk)",
                "sets_reps": "3x5 reps",
                "equipment": "Wall",
                "notes": "Walk hands down wall into backbend. Tuck ribs to protect lumbar spine."
            },
            {
                "name": "Dynamic Spinal Waves",
                "sets_reps": "2 mins",
                "equipment": "None",
                "notes": "Flow between cat-cow and cobra for segmental spinal control."
            },
            {
                "name": "PNF Pancake Stretch with Kettlebell",
                "sets_reps": "3x30s",
                "equipment": "20kg kettlebell",
                "notes": "Press knees outward gently for adductor flexibility. Avoid strain."
            },
            {
                "name": "Foam Roller IT Band Release",
                "sets_reps": "2 mins/side",
                "equipment": "Foam roller",
                "notes": "Reduce lateral thigh stiffness. Roll slowly with pauses."
            },
            {
                "name": "Scapular Wall Slides",
                "sets_reps": "3x10 reps",
                "equipment": "Wall",
                "notes": "Strengthen serratus anterior for shoulder stability in arm balances."
            },
            {
                "name": "Supine Leg Circles",
                "sets_reps": "10 reps/side",
                "equipment": "None",
                "notes": "Improve hip joint mobility for Supta Kurmasana. Keep pelvis stable."
            }
        ],
        "lunch": [
            {
                "name": "Camel Pose (Dynamic Pulses)",
                "sets_reps": "3x8 reps",
                "equipment": "None",
                "notes": "Pulse into backbend with hands on heels. Focus on thoracic extension."
            },
            {
                "name": "Scapular Push-Ups",
                "sets_reps": "3x10 reps",
                "equipment": "None",
                "notes": "Strengthen serratus anterior for Bakasana and Karandavasana."
            },
            {
                "name": "Bow Pose (Dhanurasana) with PNF",
                "sets_reps": "3x20s hold",
                "equipment": "Strap",
                "notes": "Contract glutes/hamstrings, then deepen backbend. Use strap if needed."
            },
            {
                "name": "Side Crow Prep (Koundinyasana)",
                "sets_reps": "3x5 reps/side",
                "equipment": "Yoga blocks",
                "notes": "Shift weight forward onto hands, knees on blocks. Build lateral core strength."
            },
            {
                "name": "Bridge Pose to Wheel (Progression)",
                "sets_reps": "3x5 reps",
                "equipment": "Yoga block",
                "notes": "Lift from bridge to wheel pose. Use block under sacrum for support."
            },
            {
                "name": "Forearm Stand Drills",
                "sets_reps": "3x30s hold",
                "equipment": "Wall",
                "notes": "Kick up to forearm stand against wall. Engage core and shoulders."
            },
            {
                "name": "Nadi Shodhana Breathwork",
                "sets_reps": "5 mins",
                "equipment": "None",
                "notes": "Alternate nostril breathing to balance energy for intense backbends."
            },
            {
                "name": "Thoracic Release with Lacrosse Ball",
                "sets_reps": "2 mins",
                "equipment": "Lacrosse ball",
                "notes": "Target rhomboids and mid-traps. Roll slowly between shoulder blades."
            },
            {
                "name": "Prone T-Spine Extension",
                "sets_reps": "3x10 reps",
                "equipment": "None",
                "notes": "Lift chest and arms while squeezing scapulae. Strengthen spinal extensors."
            },
            {
                "name": "Standing Quad Stretch with PNF",
                "sets_reps": "2x30s/side",
                "equipment": "Wall",
                "notes": "Contract quads against wall for 5s, then relax deeper."
            },
            {
                "name": "Seated Spinal Twist",
                "sets_reps": "1 min/side",
                "equipment": "None",
                "notes": "Improve rotational mobility for Marichyasana D. Exhale into the twist."
            },
            {
                "name": "Child's Pose with Side Reach",
                "sets_reps": "1 min/side",
                "equipment": "None",
                "notes": "Stretch lats and improve thoracic rotation."
            }
        ],
        "pre_bed": [
            {
                "name": "Yin Yoga Pigeon Pose",
                "sets_reps": "3x90s/side",
                "equipment": "Bolster",
                "notes": "Passive hip opener with forward fold. Bolster under knee if needed."
            },
            {
                "name": "Supported Fish Pose",
                "sets_reps": "3x60s",
                "equipment": "Bolster/blanket",
                "notes": "Stretch anterior thoracic spine. Place bolster vertically under spine."
            },
            {
                "name": "Eccentric Nordic Curls",
                "sets_reps": "3x6 reps",
                "equipment": "Resistance band",
                "notes": "Lower over 6s, assist up. Maintain hamstring tendon resilience."
            },
            {
                "name": "Adductor Ball Release",
                "sets_reps": "2 mins/side",
                "equipment": "Lacrosse ball",
                "notes": "Release inner thighs for splits and leg-behind-head poses."
            },
            {
                "name": "Supine Spinal Twist with Traction",
                "sets_reps": "3x60s/side",
                "equipment": "Strap",
                "notes": "Use strap to gently pull knee toward floor while grounding shoulders."
            },
            {
                "name": "Legs-Up-The-Wall w/ Pelvic Tilts",
                "sets_reps": "5 mins",
                "equipment": "None",
                "notes": "Enhance circulation and decompress lumbar spine."
            },
            {
                "name": "Infrared Mat + Guided Visualization",
                "sets_reps": "10 mins",
                "equipment": "Infrared/NIR mat",
                "notes": "Pair heat therapy with mental rehearsal of complex asanas."
            },
            {
                "name": "Yin Yoga Dragon Pose",
                "sets_reps": "2x90s/side",
                "equipment": "Yoga blocks",
                "notes": "Deep hip flexor stretch. Blocks under hands for support."
            },
            {
                "name": "Gentle Neck Release",
                "sets_reps": "1 min/side",
                "equipment": "None",
                "notes": "Tilt head side-to-side to relieve tension."
            },
            {
                "name": "Alternate Nostril Breathing",
                "sets_reps": "5 mins",
                "equipment": "None",
                "notes": "Balance the nervous system and reduce stress."
            },
            {
                "name": "Foam Roll Glutes/Hamstrings",
                "sets_reps": "2 mins/side",
                "equipment": "Foam roller",
                "notes": "Roll posterior chain to release tension from weightlifting."
            },
            {
                "name": "Supported Shoulderstand",
                "sets_reps": "3x60s",
                "equipment": "Wall",
                "notes": "Use wall for support to decompress spine and improve circulation."
            }
        ]
    }

def get_phase3_exercises() -> Dict[str, List[Dict[str, Any]]]:
    """Return Phase 3 (Advanced) mobility protocol data."""
    return {
        "morning": [
            {
                "name": "Sun Salutation B (Full Vinyasa)",
                "sets_reps": "5 rounds",
                "equipment": "None",
                "notes": "Link breath to movement. Emphasize jump-backs and jump-throughs."
            },
            {
                "name": "Kapotasana Prep (Resistance Bands)",
                "sets_reps": "3x30s hold",
                "equipment": "Resistance bands",
                "notes": "Loop bands around thighs to engage glutes while deepening backbend. Focus on thoracic extension."
            },
            {
                "name": "Dwi Pada Sirsasana Drills",
                "sets_reps": "3x30s/side",
                "equipment": "Yoga blocks",
                "notes": "Elevate hips with blocks to reduce strain. Gradually work toward full pose."
            },
            {
                "name": "Handstand Push-Up Negatives",
                "sets_reps": "3x5 reps",
                "equipment": "Wall",
                "notes": "Lower slowly from handstand to build shoulder stability for Karandavasana."
            },
            {
                "name": "Marichyasana D Strap Simulation",
                "sets_reps": "3x30s/side",
                "equipment": "Strap",
                "notes": "Loop strap around foot and opposite hip to mimic bind mechanics."
            },
            {
                "name": "Dynamic Spinal Waves",
                "sets_reps": "2 mins",
                "equipment": "None",
                "notes": "Flow between cat-cow and cobra to enhance segmental spinal control."
            },
            {
                "name": "PNF Pancake Stretch with Kettlebell",
                "sets_reps": "3x30s",
                "equipment": "20kg kettlebell",
                "notes": "Gently press knees outward for adductor flexibility. Avoid strain."
            },
            {
                "name": "IT Band Release + Glute Activation",
                "sets_reps": "2 mins/side",
                "equipment": "Foam roller/massage gun",
                "notes": "Target TFL and glute medius to support leg-behind-head poses."
            },
            {
                "name": "Scapular Wall Slides",
                "sets_reps": "3x10 reps",
                "equipment": "Wall",
                "notes": "Strengthen serratus anterior for shoulder stability in arm balances."
            },
            {
                "name": "Supine Leg Circles",
                "sets_reps": "10 reps/side",
                "equipment": "None",
                "notes": "Improve hip joint mobility for Supta Kurmasana. Keep pelvis stable."
            },
            {
                "name": "Drop-Backs with Spotter/Strap",
                "sets_reps": "5 reps",
                "equipment": "Strap/Wall",
                "notes": "Transition from standing to Urdhva Dhanurasana with controlled eccentric phase."
            },
            {
                "name": "L-Sit to Compass Pose",
                "sets_reps": "3x8 reps/side",
                "equipment": "None",
                "notes": "Strengthen hip flexors and obliques for Parivrtta Surya Yantrasana."
            }
        ],
        "lunch": [
            {
                "name": "Weighted Back Extensions",
                "sets_reps": "3x10 reps",
                "equipment": "24kg kettlebell",
                "notes": "Hold kettlebell to chest while extending spine. Strengthen erectors for backbends."
            },
            {
                "name": "Advanced Crow to Handstand",
                "sets_reps": "3x5 reps",
                "equipment": "Yoga blocks",
                "notes": "Transition from Bakasana to handstand against wall. Builds explosive power."
            },
            {
                "name": "Bow Pose (Dhanurasana) with PNF",
                "sets_reps": "3x30s hold",
                "equipment": "Strap",
                "notes": "Contract glutes/hamstrings, then deepen backbend. Use strap if unable to reach ankles."
            },
            {
                "name": "Resistance Band Rotator Cuff Drills",
                "sets_reps": "3x15 reps/side",
                "equipment": "Resistance band",
                "notes": "External/internal rotations to protect shoulders in arm balances."
            },
            {
                "name": "Kapalabhati Breathwork",
                "sets_reps": "5 mins",
                "equipment": "None",
                "notes": "'Skull-shining breath' to energize and enhance focus for intense sequences."
            },
            {
                "name": "Thoracic Release with Lacrosse Ball",
                "sets_reps": "2 mins",
                "equipment": "Lacrosse ball",
                "notes": "Target rhomboids and mid-traps to maintain upper back mobility."
            },
            {
                "name": "Prone T-Spine Extension",
                "sets_reps": "3x10 reps",
                "equipment": "None",
                "notes": "Lift chest and arms while squeezing scapulae. Strengthen spinal extensors."
            },
            {
                "name": "Standing Quad Stretch with PNF",
                "sets_reps": "2x30s/side",
                "equipment": "Wall",
                "notes": "Contract quads against wall for 5s, then relax deeper."
            },
            {
                "name": "Seated Spinal Twist",
                "sets_reps": "1 min/side",
                "equipment": "None",
                "notes": "Improve rotational mobility for Marichyasana D. Exhale into the twist."
            },
            {
                "name": "Child's Pose with Side Reach",
                "sets_reps": "1 min/side",
                "equipment": "None",
                "notes": "Stretch lats and improve thoracic rotation."
            },
            {
                "name": "Forearm Stand to Scorpion Prep",
                "sets_reps": "3x30s hold",
                "equipment": "Wall",
                "notes": "Lift one leg toward head while in forearm stand. Engage core and shoulders."
            },
            {
                "name": "Dynamic Dragon Pose",
                "sets_reps": "8 reps/side",
                "equipment": "None",
                "notes": "Pulse in lunge position to open hip flexors and deepen backbend."
            }
        ],
        "pre_bed": [
            {
                "name": "Yin Yoga Dragon Pose",
                "sets_reps": "3x90s/side",
                "equipment": "Bolster",
                "notes": "Deep hip flexor stretch with forward fold. Bolster under knee if needed."
            },
            {
                "name": "Supported Kapotasana",
                "sets_reps": "3x60s",
                "equipment": "Yoga chair",
                "notes": "Rest forearms on chair seat to safely deepen backbend. Focus on breath."
            },
            {
                "name": "Eccentric Nordic Curls",
                "sets_reps": "3x8 reps",
                "equipment": "Resistance band",
                "notes": "Lower over 6s, assist up. Maintain hamstring tendon resilience."
            },
            {
                "name": "Adductor Ball Release",
                "sets_reps": "2 mins/side",
                "equipment": "Lacrosse ball",
                "notes": "Release inner thighs for splits and leg-behind-head poses."
            },
            {
                "name": "Supine Spinal Twist with Traction",
                "sets_reps": "3x60s/side",
                "equipment": "Strap",
                "notes": "Use strap to gently pull knee toward floor while grounding shoulders."
            },
            {
                "name": "Legs-Up-The-Wall w/ Pelvic Tilts",
                "sets_reps": "5 mins",
                "equipment": "None",
                "notes": "Enhance circulation and decompress lumbar spine."
            },
            {
                "name": "Infrared Mat + Guided Visualization",
                "sets_reps": "10 mins",
                "equipment": "Infrared/NIR mat",
                "notes": "Pair heat therapy with mental rehearsal of complex asanas."
            },
            {
                "name": "Yin Yoga Sphinx Pose",
                "sets_reps": "3x90s",
                "equipment": "Bolster",
                "notes": "Passive thoracic extension. Place bolster under forearms for support."
            },
            {
                "name": "Gentle Neck Release",
                "sets_reps": "1 min/side",
                "equipment": "None",
                "notes": "Tilt head side-to-side to relieve tension."
            },
            {
                "name": "Alternate Nostril Breathing",
                "sets_reps": "5 mins",
                "equipment": "None",
                "notes": "Balance the nervous system and reduce stress."
            },
            {
                "name": "Foam Roll Glutes/Hamstrings",
                "sets_reps": "2 mins/side",
                "equipment": "Foam roller",
                "notes": "Roll posterior chain to release tension from weightlifting."
            },
            {
                "name": "Supported Shoulderstand",
                "sets_reps": "3x60s",
                "equipment": "Wall",
                "notes": "Use wall for support to decompress spine and improve circulation."
            }
        ]
    }

def get_current_exercises() -> List[Dict[str, Any]]:
    """Get exercises for current phase and session."""
    phase = get_current_phase()
    session = get_current_session()
    
    # Get exercises based on phase
    if phase == "Phase 1":
        exercises = get_phase1_exercises()
    elif phase == "Phase 2":
        exercises = get_phase2_exercises()
    else:
        exercises = get_phase3_exercises()
    
    return exercises.get(session, [])

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