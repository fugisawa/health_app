"""Data validation utilities."""
from typing import Dict, Any, List, Set, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ValidationError:
    """Validation error details."""
    field: str
    message: str
    value: Any = None

class DataValidator:
    """Data structure validator."""
    
    @staticmethod
    def validate_exercise(exercise: Dict[str, Any]) -> List[ValidationError]:
        """Validate exercise data structure.
        
        Required fields:
        - name: Exercise name
        - sets_reps: Sets and reps information
        - equipment: Required equipment
        - notes: Exercise notes/instructions
        - duration: Time duration
        """
        errors = []
        required_fields = {
            'name': str,
            'sets_reps': str,
            'equipment': str,
            'notes': str,
            'duration': str
        }
        
        for field, expected_type in required_fields.items():
            if field not in exercise:
                errors.append(ValidationError(field, f"Missing required field: {field}"))
                continue
            
            value = exercise[field]
            if not isinstance(value, expected_type):
                errors.append(ValidationError(
                    field,
                    f"Invalid type for {field}: expected {expected_type.__name__}, got {type(value).__name__}",
                    value
                ))
        
        return errors
    
    @staticmethod
    def validate_treatment(treatment: Dict[str, Any]) -> List[ValidationError]:
        """Validate LLLT treatment data structure.
        
        Required fields:
        - name: Treatment name
        - intensity: Treatment intensity
        - duration: Time duration
        - equipment: Required equipment
        - notes: Treatment notes/instructions
        """
        errors = []
        required_fields = {
            'name': str,
            'intensity': str,
            'duration': str,
            'equipment': str,
            'notes': str
        }
        
        for field, expected_type in required_fields.items():
            if field not in treatment:
                errors.append(ValidationError(field, f"Missing required field: {field}"))
                continue
            
            value = treatment[field]
            if not isinstance(value, expected_type):
                errors.append(ValidationError(
                    field,
                    f"Invalid type for {field}: expected {expected_type.__name__}, got {type(value).__name__}",
                    value
                ))
        
        return errors
    
    @staticmethod
    def validate_protocol_version(version: str) -> bool:
        """Validate protocol version format (major.minor.patch)."""
        try:
            major, minor, patch = map(int, version.split('.'))
            return all(x >= 0 for x in (major, minor, patch))
        except (ValueError, AttributeError):
            return False
    
    @staticmethod
    def check_protocol_compatibility(
        lllt_version: str,
        mobility_version: str,
        min_version: str = "1.0.0"
    ) -> List[ValidationError]:
        """Check protocol version compatibility."""
        errors = []
        
        if not DataValidator.validate_protocol_version(lllt_version):
            errors.append(ValidationError("lllt_version", "Invalid version format", lllt_version))
        
        if not DataValidator.validate_protocol_version(mobility_version):
            errors.append(ValidationError("mobility_version", "Invalid version format", mobility_version))
        
        if not DataValidator.validate_protocol_version(min_version):
            errors.append(ValidationError("min_version", "Invalid version format", min_version))
        
        if not errors:
            lllt_parts = tuple(map(int, lllt_version.split('.')))
            mobility_parts = tuple(map(int, mobility_version.split('.')))
            min_parts = tuple(map(int, min_version.split('.')))
            
            if lllt_parts < min_parts:
                errors.append(ValidationError(
                    "lllt_version",
                    f"LLLT protocol version {lllt_version} is below minimum {min_version}",
                    lllt_version
                ))
            
            if mobility_parts < min_parts:
                errors.append(ValidationError(
                    "mobility_version",
                    f"Mobility protocol version {mobility_version} is below minimum {min_version}",
                    mobility_version
                ))
            
            if lllt_parts != mobility_parts:
                errors.append(ValidationError(
                    "version_mismatch",
                    f"Protocol version mismatch: LLLT {lllt_version} vs Mobility {mobility_version}"
                ))
        
        return errors 