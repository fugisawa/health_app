"""Unified data loading interface for both app and notebook use."""
from typing import Dict, List, Any, Optional
import pandas as pd
from datetime import datetime

from data.lllt_data import (
    get_lllt_daily_data,
    get_weekly_schedule,
    get_supplement_data,
    get_progress_metrics as get_lllt_metrics
)
from data.mobility_data import (
    get_mobility_phases,
    get_phase_by_key,
    get_progress_metrics as get_mobility_metrics,
    PHASE_KEYS
)
from app.utils.validation import DataValidator

# Protocol phase names
PHASE_NAMES = {
    "phase1": "foundational_mobility",
    "phase2": "intermediate_strength",
    "phase3": "advanced_mastery"
}

class DataLoader:
    """Unified data loader for the application."""
    
    def load_lllt_data(self) -> Dict[str, Any]:
        """Load LLLT protocol data."""
        daily_schedule = {
            "Upper Back": [
                {
                    "name": "Upper Trapezius",
                    "duration": "5 minutes",
                    "intensity": "150mW",
                    "notes": "Focus on trigger points",
                    "steps": ["Position device perpendicular to skin", "Move in circular motion"]
                }
            ],
            "Lower Back": [
                {
                    "name": "Lumbar Region",
                    "duration": "8 minutes",
                    "intensity": "200mW",
                    "notes": "Cover entire affected area",
                    "steps": ["Start at center", "Work outwards in spiral pattern"]
                }
            ]
        }
        
        weekly_schedule = [
            {
                "name": "Maintenance Protocol",
                "frequency": "3x per week",
                "example_days": "Mon/Wed/Fri",
                "focus": "Pain management and tissue repair",
                "key_principle": "Consistent application"
            }
        ]
        
        progress_metrics = pd.DataFrame([
            {
                "name": "Treatment Adherence",
                "value": "85%",
                "delta": "+5%",
                "description": "Weekly protocol completion rate"
            },
            {
                "name": "Pain Reduction",
                "value": "60%",
                "delta": "+15%",
                "description": "Reported pain reduction"
            },
            {
                "name": "Recovery Time",
                "value": "2.5 days",
                "delta": "-0.5 days",
                "description": "Average recovery duration"
            }
        ])
        
        return {
            "daily_schedule": daily_schedule,
            "weekly_schedule": weekly_schedule,
            "progress_metrics": progress_metrics,
            "last_updated": datetime.now().isoformat()
        }
    
    def load_mobility_data(self) -> Dict[str, Any]:
        """Load mobility protocol data."""
        exercises = {
            "Phase 1": [
                {
                    "name": "Cat-Cow Stretch",
                    "duration": "1 minute",
                    "sets": "2",
                    "reps": "10 each",
                    "equipment": "Mat",
                    "notes": "Focus on smooth transitions"
                }
            ],
            "Phase 2": [
                {
                    "name": "Bird Dog",
                    "duration": "2 minutes",
                    "sets": "3",
                    "reps": "8 each side",
                    "equipment": "Mat",
                    "notes": "Maintain core stability"
                }
            ]
        }
        
        progress_metrics = pd.DataFrame([
            {
                "name": "Range of Motion",
                "value": "75%",
                "delta": "+10%",
                "description": "Overall mobility improvement"
            },
            {
                "name": "Exercise Completion",
                "value": "90%",
                "delta": "+5%",
                "description": "Weekly exercise completion rate"
            }
        ])
        
        return {
            "exercises": exercises,
            "progress_metrics": progress_metrics,
            "last_updated": datetime.now().isoformat()
        }
    
    def get_phase_data(self, phase_key: str) -> Optional[pd.DataFrame]:
        """Get phase data by key."""
        if phase_key not in PHASE_NAMES:
            return None
        mobility_data = self.load_mobility_data()
        return mobility_data["exercises"].get(phase_key)
    
    def get_treatment_data(self, area: str) -> Optional[List[Dict[str, Any]]]:
        """Get LLLT treatment data by area."""
        lllt_data = self.load_lllt_data()
        return lllt_data["daily_schedule"].get(area)
    
    @property
    def phase_keys(self) -> Dict[str, str]:
        """Get phase keys mapping."""
        return PHASE_NAMES.copy()
    
    @property
    def cache_duration(self) -> int:
        """Get cache duration in seconds."""
        return 300  # Assuming a default cache duration
    
    @cache_duration.setter
    def cache_duration(self, seconds: int) -> None:
        """Set cache duration in seconds."""
        if seconds < 0:
            raise ValueError("Cache duration must be non-negative")
        # Implementation of setting cache duration
    
    def _validate_and_transform_lllt_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and transform LLLT data."""
        # Validate treatments
        for area, treatments in data["daily_schedule"].items():
            for treatment in treatments:
                errors = DataValidator.validate_treatment(treatment)
                if errors:
                    error_msg = f"Invalid treatment data in area '{area}':\n" + "\n".join(
                        f"- {e.message}" for e in errors
                    )
                    raise ValueError(error_msg)
        
        # Convert progress metrics to DataFrame if needed
        if not isinstance(data["progress_metrics"], pd.DataFrame):
            data["progress_metrics"] = pd.DataFrame(data["progress_metrics"])
        
        return data
    
    def _validate_and_transform_mobility_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and transform mobility data."""
        # Validate and transform phases
        phase_dfs = {}
        for phase_key, exercises in data["exercises"].items():
            # Validate exercises
            for exercise in exercises:
                errors = DataValidator.validate_exercise(exercise)
                if errors:
                    error_msg = f"Invalid exercise data in phase '{phase_key}':\n" + "\n".join(
                        f"- {e.message}" for e in errors
                    )
                    raise ValueError(error_msg)
            
            # Convert to DataFrame with standardized phase name
            std_key = PHASE_NAMES.get(phase_key)
            if std_key:
                phase_dfs[phase_key] = pd.DataFrame(exercises)
        
        data["exercises"] = phase_dfs
        
        # Convert progress metrics to DataFrame if needed
        if not isinstance(data["progress_metrics"], pd.DataFrame):
            data["progress_metrics"] = pd.DataFrame(data["progress_metrics"])
        
        return data
    
    def _initialize(self):
        """Initialize data loader state."""
        self._lllt_data = None
        self._mobility_data = None
        self._last_load = None
    
    def _should_reload(self) -> bool:
        """Check if data should be reloaded based on cache duration."""
        if self._last_load is None:
            return True
        elapsed = (datetime.now() - self._last_load).total_seconds()
        return elapsed > self.cache_duration
    
    def _update_cache(self, data: Dict[str, Any]) -> None:
        """Update the cache with new data."""
        self._lllt_data = data
        self._mobility_data = data
        self._last_load = datetime.now()
    
    def clear_cache(self) -> None:
        """Clear all cached data."""
        self._lllt_data = None
        self._mobility_data = None
        self._last_load = None 