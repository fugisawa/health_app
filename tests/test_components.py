import pytest
import time
from app.components.timer import TimerComponent

def test_timer_initialization():
    timer = TimerComponent()
    assert not timer.state.timer_active
    assert timer.state.timer_start is None
    assert timer.state.timer_duration == 0
    assert not timer.state.timer_paused

def test_timer_start():
    timer = TimerComponent()
    duration = 60
    
    timer.start_timer(duration)
    assert timer.state.timer_active
    assert timer.state.timer_start is not None
    assert timer.state.timer_duration == duration
    assert not timer.state.timer_paused

def test_timer_pause_resume():
    timer = TimerComponent()
    duration = 60
    
    # Start timer
    timer.start_timer(duration)
    start_time = timer.state.timer_start
    
    # Wait briefly
    time.sleep(0.1)
    
    # Pause timer
    timer.pause_timer()
    assert timer.state.timer_paused
    assert timer.state.pause_time is not None
    
    # Wait while paused
    time.sleep(0.1)
    
    # Resume timer
    timer.resume_timer()
    assert not timer.state.timer_paused
    assert timer.state.timer_start > start_time  # Timer start should be adjusted

def test_timer_restart():
    timer = TimerComponent()
    duration = 60
    
    # Start and wait
    timer.start_timer(duration)
    original_start = timer.state.timer_start
    time.sleep(0.1)
    
    # Restart
    timer.restart_timer()
    assert timer.state.timer_start > original_start
    assert not timer.state.timer_paused
    assert timer.state.timer_duration == duration

def test_timer_stop():
    timer = TimerComponent()
    
    # Start and stop
    timer.start_timer(60)
    timer.stop_timer()
    
    assert not timer.state.timer_active
    assert timer.state.timer_start is None
    assert not timer.state.timer_paused

def test_circular_progress():
    timer = TimerComponent()
    
    # Test progress calculation
    progress = 0.5
    time_display = "00:30"
    svg = timer.circular_progress(progress, time_display)
    
    assert "stroke-dashoffset" in svg
    assert time_display in svg
    assert "transform: rotate(-90deg)" in svg 