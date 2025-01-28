"""
Utility functions for local data persistence and data export.
"""
import json
import os
import csv
from datetime import datetime, timedelta
from typing import Dict, Any, List
from ics import Calendar, Event

def get_data_dir() -> str:
    """Get or create the data directory for storing local files."""
    home = os.path.expanduser("~")
    data_dir = os.path.join(home, ".health_protocol")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def save_session_progress(completed_exercises: set, session_type: str) -> None:
    """Save completed exercises to a local JSON file."""
    data_dir = get_data_dir()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Load existing data if any
    progress_file = os.path.join(data_dir, "session_progress.json")
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            progress_data = json.load(f)
    else:
        progress_data = {}
    
    # Update with today's progress
    if today not in progress_data:
        progress_data[today] = {}
    progress_data[today][session_type] = list(completed_exercises)
    
    # Save updated data
    with open(progress_file, 'w') as f:
        json.dump(progress_data, f)

def load_session_progress(session_type: str) -> set:
    """Load completed exercises for today's session."""
    data_dir = get_data_dir()
    today = datetime.now().strftime("%Y-%m-%d")
    progress_file = os.path.join(data_dir, "session_progress.json")
    
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            progress_data = json.load(f)
            if today in progress_data and session_type in progress_data[today]:
                return set(progress_data[today][session_type])
    
    return set()

def get_session_history(days: int = 7) -> Dict[str, Any]:
    """Get session completion history for the last N days."""
    data_dir = get_data_dir()
    progress_file = os.path.join(data_dir, "session_progress.json")
    
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            progress_data = json.load(f)
            # Sort and limit to last N days
            dates = sorted(progress_data.keys(), reverse=True)[:days]
            return {date: progress_data[date] for date in dates}
    
    return {}

def export_history_to_csv(days: int = 30) -> str:
    """Export session history to CSV file."""
    history = get_session_history(days)
    data_dir = get_data_dir()
    export_file = os.path.join(data_dir, f"health_protocol_history_{datetime.now().strftime('%Y%m%d')}.csv")
    
    # Prepare data for CSV
    rows = []
    for date, sessions in history.items():
        for session_type, completed in sessions.items():
            rows.append({
                'Date': date,
                'Session': session_type,
                'Completed Exercises': len(completed),
                'Exercise IDs': ','.join(map(str, completed))
            })
    
    # Write to CSV
    if rows:
        with open(export_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['Date', 'Session', 'Completed Exercises', 'Exercise IDs'])
            writer.writeheader()
            writer.writerows(rows)
    
    return export_file

def generate_calendar_events(days_ahead: int = 7) -> str:
    """Generate ICS file with scheduled sessions."""
    cal = Calendar()
    
    # Add events for each session type
    session_times = {
        'morning': ('08:00', '09:00'),
        'lunch': ('12:00', '13:00'),
        'pre_bed': ('20:00', '21:00')
    }
    
    for day in range(days_ahead):
        date = datetime.now().date() + timedelta(days=day)
        for session, (start_time, end_time) in session_times.items():
            event = Event()
            event.name = f"Health Protocol - {session.title()} Session"
            event.begin = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
            event.end = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")
            event.description = f"Complete your {session} health protocol exercises"
            cal.events.add(event)
    
    # Save calendar file
    data_dir = get_data_dir()
    calendar_file = os.path.join(data_dir, f"health_protocol_schedule_{datetime.now().strftime('%Y%m%d')}.ics")
    with open(calendar_file, 'w') as f:
        f.write(str(cal))
    
    return calendar_file

def get_completion_stats(days: int = 30) -> Dict[str, Any]:
    """Get completion statistics for visualization."""
    history = get_session_history(days)
    stats = {
        'daily_completion': [],
        'session_types': {},
        'streak': 0
    }
    
    dates = sorted(history.keys())
    current_streak = 0
    
    for date in dates:
        sessions = history[date]
        total_completed = sum(len(completed) for completed in sessions.values())
        stats['daily_completion'].append({
            'date': date,
            'completed': total_completed
        })
        
        # Track completion by session type
        for session_type, completed in sessions.items():
            if session_type not in stats['session_types']:
                stats['session_types'][session_type] = []
            stats['session_types'][session_type].append({
                'date': date,
                'completed': len(completed)
            })
        
        # Calculate streak
        if total_completed > 0:
            current_streak += 1
        else:
            current_streak = 0
        stats['streak'] = max(stats['streak'], current_streak)
    
    return stats 