import streamlit as st
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Set
from dataclasses import dataclass, field
import pandas as pd

from app.data.data_loader import DataLoader

@dataclass
class AppState:
    """Application state management."""
    
    # Protocol selection
    selected_protocol: str = "lllt"
    
    # Session tracking
    session_start: Optional[datetime] = None
    _completed_exercises: Set[str] = field(default_factory=set)
    current_exercise: Optional[Dict[str, Any]] = None
    
    # Timer state
    timer_active: bool = False
    timer_start: Optional[datetime] = None
    timer_duration: int = 0
    timer_paused: bool = False
    pause_time: Optional[datetime] = None
    
    # Data
    data_loader: DataLoader = field(default_factory=lambda: DataLoader())
    mobility_data: Dict[str, Dict[str, pd.DataFrame]] = field(default_factory=dict)
    lllt_data: Dict[str, pd.DataFrame] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize session state and load data."""
        self._init_session_state()
        self.load_data()
    
    def _init_session_state(self):
        """Initialize session state variables."""
        defaults = {
            'completed_exercises': set(),
            'current_exercise': None,
            'session_start': None,
            'timer_active': False,
            'timer_start': None,
            'timer_duration': 0,
            'timer_paused': False,
            'pause_time': None,
            'should_play_sound': False
        }
        
        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    def load_data(self):
        """Load all protocol data."""
        self.mobility_data = self.data_loader.load_all_mobility_data()
        self.lllt_data = self.data_loader.load_lllt_data()
    
    def switch_protocol(self, protocol: str):
        """Switch the active protocol."""
        if protocol != self.selected_protocol:
            self.selected_protocol = protocol
            self.reset_session()
    
    def reset_session(self):
        """Reset session state."""
        self.session_start = None
        self._completed_exercises.clear()
        self.current_exercise = None
        self.timer_active = False
        self.timer_start = None
        self.timer_duration = 0
        self.timer_paused = False
        self.pause_time = None
    
    def start_exercise(self, exercise: Dict[str, Any]):
        """Start a new exercise."""
        if not exercise:
            return
        self.current_exercise = exercise
        if not self.session_start:
            self.session_start = datetime.now()
    
    def complete_exercise(self, exercise_id: str):
        """Mark an exercise as completed."""
        if not exercise_id:
            return
        self._completed_exercises.add(exercise_id)
        self.current_exercise = None
    
    def is_exercise_completed(self, exercise: Dict[str, Any]) -> bool:
        """Check if an exercise is completed."""
        exercise_name = exercise.get('Exercise', exercise.get('name', ''))
        return exercise_name in self._completed_exercises
    
    def is_exercise_active(self, exercise: Dict[str, Any]) -> bool:
        """Check if an exercise is currently active."""
        if not exercise or not self.current_exercise:
            return False
        exercise_name = exercise.get('Exercise', exercise.get('name', ''))
        current_name = self.current_exercise.get('Exercise', self.current_exercise.get('name', ''))
        return exercise_name == current_name
    
    def get_session_progress(self) -> Dict[str, Any]:
        """Get current session progress metrics."""
        if not self.session_start:
            return {"completed": 0, "total": 0, "duration": "00:00:00"}
        
        total = 0
        if self.selected_protocol == "mobility":
            for phase_data in self.mobility_data.values():
                for session_data in phase_data.values():
                    total += len(session_data)
        else:
            total = len(self.lllt_data.get("lllt_days", pd.DataFrame()))
        
        completed = len(self._completed_exercises)
        duration = datetime.now() - self.session_start
        
        return {
            "completed": completed,
            "total": total,
            "duration": str(duration).split('.')[0]
        }
    
    def get_current_phase_data(self, session: str) -> pd.DataFrame:
        """Get data for current phase and session."""
        if self.selected_protocol == "mobility":
            phase = "phase1"  # Default to phase 1 for now
            return self.mobility_data[phase][session]
        return pd.DataFrame()  # Empty DataFrame if not found
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get current session statistics."""
        stats = {
            'completed_count': len(self._completed_exercises),
            'active_exercise': self.active_exercise,
            'session_duration': None
        }
        
        if self.session_start:
            stats['session_duration'] = datetime.now() - self.session_start
        
        return stats
    
    @property
    def session_end(self) -> Optional[datetime]:
        """Get session end time."""
        return datetime.now()
    
    def complete_session(self) -> None:
        """Complete the current session."""
        st.session_state.session_end = datetime.now()
        self.current_exercise = None
    
    def is_timer_active(self) -> bool:
        """Check if the timer is currently active."""
        return st.session_state.timer_active
    
    def is_timer_paused(self) -> bool:
        """Check if the timer is currently paused."""
        return st.session_state.timer_paused
    
    def get_timer_duration(self) -> float:
        """Get the current timer duration in seconds."""
        return st.session_state.timer_duration
    
    def get_timer_start(self) -> Optional[datetime]:
        """Get the timer start timestamp."""
        return st.session_state.timer_start
    
    def get_pause_time(self) -> Optional[datetime]:
        """Get the time when the timer was paused."""
        return st.session_state.pause_time
    
    def get_last_update(self) -> Optional[datetime]:
        """Get the last timer update timestamp."""
        return st.session_state.last_update
    
    def should_play_sound(self) -> bool:
        """Check if sound should be played."""
        return st.session_state.should_play_sound
    
    def set_timer_active(self, active: bool) -> None:
        """Set the timer active state."""
        st.session_state.timer_active = active
    
    def set_timer_paused(self, paused: bool) -> None:
        """Set the timer paused state."""
        st.session_state.timer_paused = paused
    
    def set_timer_duration(self, duration: float) -> None:
        """Set the timer duration in seconds."""
        st.session_state.timer_duration = duration
    
    def set_timer_start(self, start: Optional[datetime]) -> None:
        """Set the timer start timestamp."""
        st.session_state.timer_start = start
    
    def set_pause_time(self, pause_time: Optional[datetime]) -> None:
        """Set the time when the timer was paused."""
        st.session_state.pause_time = pause_time
    
    def set_last_update(self, last_update: Optional[datetime]) -> None:
        """Set the last timer update timestamp."""
        st.session_state.last_update = last_update
    
    def set_should_play_sound(self, should_play: bool) -> None:
        """Set the sound play flag."""
        st.session_state.should_play_sound = should_play
    
    @property
    def active_exercise(self) -> Optional[str]:
        """Get the name of the currently active exercise."""
        if not self.current_exercise:
            return None
        return self.current_exercise.get('Exercise', self.current_exercise.get('name', ''))
    
    @property
    def completion_percentage(self) -> float:
        """Calculate the completion percentage."""
        if self.total_count == 0:
            return 0.0
        return self.completion_percentage
    
    def mark_complete(self, exercise_name: str) -> None:
        """Mark an exercise as completed."""
        if exercise_name == self.current_exercise.get('name', ''):
            self.current_exercise = None
        self._completed_exercises.add(exercise_name)
        if self.session_start:
            self.completion_percentage = (len(self._completed_exercises) / self.total_count) * 100
    
    @property
    def total_count(self) -> int:
        """Get the total count of exercises."""
        if self.selected_protocol == "mobility":
            total = 0
            for phase_data in self.mobility_data.values():
                for session_data in phase_data.values():
                    total += len(session_data)
            return total
        else:
            return len(self.lllt_data.get("lllt_days", pd.DataFrame()))
    
    def add_completed_exercise(self, exercise: str) -> None:
        """Add an exercise to the completed set."""
        self._completed_exercises.add(exercise)
    
    def clear_completed_exercises(self) -> None:
        """Clear all completed exercises."""
        self._completed_exercises.clear() 