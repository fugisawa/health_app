"""Protocol initialization and management."""
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import pandas as pd
import streamlit as st
from datetime import datetime

from app.data_loader import DataLoader
from app.utils.validation import DataValidator, ValidationError

# Protocol phase names
PHASE_NAMES = {
    "phase1": "foundational_mobility",
    "phase2": "intermediate_strength",
    "phase3": "advanced_mastery"
}

# Current protocol version
CURRENT_VERSION = "1.0.0"

@dataclass
class Protocol:
    """Base protocol class."""
    name: str
    description: str
    progress_metrics: pd.DataFrame
    version: str = CURRENT_VERSION
    last_modified: datetime = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert protocol to dictionary format."""
        return {
            "name": self.name,
            "description": self.description,
            "progress_metrics": self.progress_metrics.to_dict(),
            "version": self.version,
            "last_modified": self.last_modified.isoformat()
        }
    
    def validate(self) -> List[ValidationError]:
        """Validate protocol data."""
        errors = []
        if not DataValidator.validate_protocol_version(self.version):
            errors.append(ValidationError("version", "Invalid version format", self.version))
        return errors

@dataclass
class LLLTProtocol(Protocol):
    """LLLT protocol data structure."""
    daily_schedule: Dict[str, List[Dict[str, Any]]]
    supplement_schedule: List[Dict[str, Any]]
    weekly_schedule: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        """Convert LLLT protocol to dictionary format."""
        base_dict = super().to_dict()
        base_dict.update({
            "daily_schedule": self.daily_schedule,
            "supplement_schedule": self.supplement_schedule,
            "weekly_schedule": self.weekly_schedule
        })
        return base_dict
    
    def validate(self) -> List[ValidationError]:
        """Validate LLLT protocol data."""
        errors = super().validate()
        
        # Validate treatments
        for area, treatments in self.daily_schedule.items():
            for treatment in treatments:
                treatment_errors = DataValidator.validate_treatment(treatment)
                if treatment_errors:
                    errors.extend([
                        ValidationError(
                            f"{area}.{err.field}",
                            f"Treatment '{treatment.get('name', 'Unknown')}': {err.message}",
                            err.value
                        )
                        for err in treatment_errors
                    ])
        
        return errors

@dataclass
class MobilityProtocol(Protocol):
    """Mobility protocol data structure."""
    phases: Dict[str, pd.DataFrame]
    phase_details: Dict[str, Dict[str, str]]

    def to_dict(self) -> Dict[str, Any]:
        """Convert mobility protocol to dictionary format."""
        base_dict = super().to_dict()
        base_dict.update({
            "phases": {PHASE_NAMES[k]: v.to_dict() for k, v in self.phases.items()},
            "phase_details": {PHASE_NAMES[k]: v for k, v in self.phase_details.items()}
        })
        return base_dict
    
    def validate(self) -> List[ValidationError]:
        """Validate mobility protocol data."""
        errors = super().validate()
        
        # Validate phase keys
        for phase_key in self.phases.keys():
            if phase_key not in PHASE_NAMES:
                errors.append(ValidationError(
                    "phases",
                    f"Invalid phase key: {phase_key}",
                    phase_key
                ))
        
        # Validate exercises in each phase
        for phase_key, exercises_df in self.phases.items():
            for _, exercise in exercises_df.iterrows():
                exercise_errors = DataValidator.validate_exercise(exercise.to_dict())
                if exercise_errors:
                    errors.extend([
                        ValidationError(
                            f"{phase_key}.{err.field}",
                            f"Exercise '{exercise.get('name', 'Unknown')}': {err.message}",
                            err.value
                        )
                        for err in exercise_errors
                    ])
        
        return errors

    def get_phase_data(self, phase_key: str) -> Optional[pd.DataFrame]:
        """Get phase data by key with validation."""
        if phase_key not in PHASE_NAMES:
            return None
        return self.phases.get(phase_key)

    def update_phase_data(self, phase_key: str, data: pd.DataFrame) -> bool:
        """Update phase data with validation."""
        if phase_key not in PHASE_NAMES:
            return False
        
        # Validate new data
        for _, exercise in data.iterrows():
            errors = DataValidator.validate_exercise(exercise.to_dict())
            if errors:
                return False
        
        self.phases[phase_key] = data
        self.last_modified = datetime.now()
        return True

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_protocols() -> Dict[str, Protocol]:
    """Load all protocol data.
    
    Returns:
        Dictionary containing initialized protocol objects.
    """
    data_loader = DataLoader()
    
    # Initialize LLLT Protocol
    lllt_data = data_loader.load_lllt_data()
    lllt_protocol = LLLTProtocol(
        name="Light Therapy Protocol",
        description="Low-Level Light Therapy Protocol for Hair and Body Optimization",
        progress_metrics=lllt_data["progress_metrics"],
        daily_schedule=lllt_data["daily_schedule"],
        supplement_schedule=lllt_data["supplement_schedule"],
        weekly_schedule=lllt_data["weekly_schedule"],
        version=CURRENT_VERSION
    )
    
    # Initialize Mobility Protocol
    mobility_data = data_loader.load_mobility_data()
    mobility_protocol = MobilityProtocol(
        name="Movement & Mobility Protocol",
        description="Progressive Mobility Training for Movement Mastery",
        progress_metrics=mobility_data["progress_metrics"],
        phases=mobility_data["phases"],
        phase_details=mobility_data["phase_details"],
        version=CURRENT_VERSION
    )
    
    # Validate protocols
    lllt_errors = lllt_protocol.validate()
    mobility_errors = mobility_protocol.validate()
    
    if lllt_errors or mobility_errors:
        error_msg = "Protocol validation failed:\n"
        if lllt_errors:
            error_msg += "\nLLLT Protocol:\n" + "\n".join(f"- {e.message}" for e in lllt_errors)
        if mobility_errors:
            error_msg += "\nMobility Protocol:\n" + "\n".join(f"- {e.message}" for e in mobility_errors)
        raise ValueError(error_msg)
    
    # Check protocol compatibility
    version_errors = DataValidator.check_protocol_compatibility(
        lllt_protocol.version,
        mobility_protocol.version
    )
    if version_errors:
        error_msg = "Protocol version compatibility check failed:\n" + "\n".join(
            f"- {e.message}" for e in version_errors
        )
        raise ValueError(error_msg)
    
    return {
        "lllt": lllt_protocol,
        "mobility": mobility_protocol
    }

def get_protocol(protocol_key: str) -> Optional[Protocol]:
    """Get protocol by key with cache handling."""
    protocols = load_protocols()
    return protocols.get(protocol_key)

def update_protocol(protocol_key: str, protocol: Protocol) -> bool:
    """Update protocol with cache invalidation."""
    if protocol_key not in ["lllt", "mobility"]:
        return False
    
    # Validate protocol
    errors = protocol.validate()
    if errors:
        error_msg = f"Protocol validation failed:\n" + "\n".join(
            f"- {e.message}" for e in errors
        )
        raise ValueError(error_msg)
    
    # Force cache invalidation
    load_protocols.clear()
    DataLoader().clear_cache()
    return True 