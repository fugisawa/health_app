"""Tests for data management."""
import pytest
from datetime import datetime

from app.data.lllt_data import (
    get_lllt_daily_data,
    get_weekly_schedule,
    get_adjustments_data,
    get_progress_metrics
)
from app.data.mobility_data import (
    get_mobility_phases,
    get_phase_details,
    get_phase1_data,
    get_phase2_data,
    get_phase3_data
)

def test_lllt_daily_data():
    """Test LLLT daily data structure."""
    data = get_lllt_daily_data()
    
    # Verify data structure
    assert isinstance(data, dict)
    assert all(area in data for area in ['Head', 'Neck', 'Back'])
    
    # Verify treatment details
    for area, details in data.items():
        assert 'duration' in details
        assert 'intensity' in details
        assert 'equipment' in details
        assert 'notes' in details
        assert 'steps' in details
        assert isinstance(details['steps'], list)

def test_lllt_weekly_schedule():
    """Test LLLT weekly schedule structure."""
    schedule = get_weekly_schedule()
    
    # Verify schedule structure
    assert isinstance(schedule, list)
    assert len(schedule) > 0
    
    # Verify schedule details
    for day in schedule:
        assert 'name' in day
        assert 'frequency' in day
        assert 'example_days' in day
        assert 'focus' in day
        assert 'key_principle' in day

def test_lllt_adjustments():
    """Test LLLT adjustments data structure."""
    adjustments = get_adjustments_data()
    
    # Verify adjustments structure
    assert isinstance(adjustments, list)
    assert len(adjustments) > 0
    
    # Verify adjustment details
    for adjustment in adjustments:
        assert 'date' in adjustment
        assert 'type' in adjustment
        assert 'details' in adjustment
        assert 'impact' in adjustment

def test_lllt_progress_metrics():
    """Test LLLT progress metrics structure."""
    metrics = get_progress_metrics()
    
    # Verify metrics structure
    assert isinstance(metrics, dict)
    assert 'treatment_consistency' in metrics
    assert 'protocol_adherence' in metrics
    assert 'recovery_improvement' in metrics
    
    # Verify metric values
    for metric, value in metrics.items():
        assert isinstance(value, (int, float))
        assert 0 <= value <= 100

def test_mobility_phases():
    """Test mobility phases structure."""
    phases = get_mobility_phases()
    
    # Verify phases structure
    assert isinstance(phases, dict)
    assert all(phase in phases for phase in ['phase1', 'phase2', 'phase3'])
    
    # Verify phase details
    for phase, exercises in phases.items():
        assert isinstance(exercises, list)
        for exercise in exercises:
            assert 'name' in exercise
            assert any(key in exercise for key in ['duration', 'reps'])
            assert 'equipment' in exercise
            assert 'key_notes' in exercise

def test_phase_details():
    """Test phase details structure."""
    details = get_phase_details()
    
    # Verify details structure
    assert isinstance(details, dict)
    assert all(phase in details for phase in ['phase1', 'phase2', 'phase3'])
    
    # Verify detail fields
    for phase, info in details.items():
        assert 'name' in info
        assert 'duration' in info

def test_phase1_data():
    """Test phase 1 exercise data."""
    exercises = get_phase1_data()
    
    # Verify exercises structure
    assert isinstance(exercises, list)
    assert len(exercises) > 0
    
    # Verify exercise details
    for exercise in exercises:
        assert 'name' in exercise
        assert any(key in exercise for key in ['duration', 'reps'])
        assert 'equipment' in exercise
        assert 'key_notes' in exercise
        assert 'steps' in exercise
        assert isinstance(exercise['steps'], list)

def test_phase2_data():
    """Test phase 2 exercise data."""
    exercises = get_phase2_data()
    
    # Verify exercises structure
    assert isinstance(exercises, list)
    assert len(exercises) > 0
    
    # Verify exercise details
    for exercise in exercises:
        assert 'name' in exercise
        assert any(key in exercise for key in ['duration', 'reps'])
        assert 'equipment' in exercise
        assert 'key_notes' in exercise
        assert 'steps' in exercise
        assert isinstance(exercise['steps'], list)

def test_phase3_data():
    """Test phase 3 exercise data."""
    exercises = get_phase3_data()
    
    # Verify exercises structure
    assert isinstance(exercises, list)
    assert len(exercises) > 0
    
    # Verify exercise details
    for exercise in exercises:
        assert 'name' in exercise
        assert any(key in exercise for key in ['duration', 'reps'])
        assert 'equipment' in exercise
        assert 'key_notes' in exercise
        assert 'steps' in exercise
        assert isinstance(exercise['steps'], list) 