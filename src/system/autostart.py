"""
Simple auto-start functionality for PCTracker.
"""
import os
import sys
import winreg
from pathlib import Path


class AutoStart:
    """Simple auto-start manager for Windows."""
    
    def __init__(self, app_name: str = "PCTracker"):
        self.app_name = app_name
        self.registry_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        self.startup_folder = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    
    def is_enabled(self) -> bool:
        """Check if auto-start is enabled."""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.registry_key) as key:
                try:
                    winreg.QueryValueEx(key, self.app_name)
                    return True
                except FileNotFoundError:
                    return False
        except Exception as e:
            print(f"Error checking auto-start status: {e}")
            return False
    
    def enable(self, exe_path: str) -> bool:
        """Enable auto-start for the application."""
        try:
            # Add to Windows registry
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.registry_key, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, self.app_name, 0, winreg.REG_SZ, exe_path)
            
            # Create startup shortcut as backup
            self._create_startup_shortcut(exe_path)
            
            print(f"Auto-start enabled for {self.app_name}")
            return True
            
        except Exception as e:
            print(f"Error enabling auto-start: {e}")
            return False
    
    def disable(self) -> bool:
        """Disable auto-start for the application."""
        success = True
        try:
            # Remove from Windows registry
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.registry_key, 0, winreg.KEY_SET_VALUE) as key:
                    try:
                        winreg.DeleteValue(key, self.app_name)
                        print(f"Registry entry removed for {self.app_name}")
                    except FileNotFoundError:
                        print(f"Registry entry not found for {self.app_name}")
            except Exception as e:
                print(f"Error accessing registry: {e}")
                success = False
            
            # Remove startup shortcut
            self._remove_startup_shortcut()
            
            if success:
                print(f"Auto-start disabled for {self.app_name}")
            return success
            
        except Exception as e:
            print(f"Error disabling auto-start: {e}")
            return False
    
    def _create_startup_shortcut(self, exe_path: str):
        """Create shortcut in startup folder."""
        try:
            # Create a simple batch file as alternative to shortcut
            batch_path = self.startup_folder / f"{self.app_name}.bat"
            with open(batch_path, 'w') as f:
                f.write(f'@echo off\nstart "" "{exe_path}"\n')
            
            print(f"Startup shortcut created at {batch_path}")
            
        except Exception as e:
            print(f"Error creating startup shortcut: {e}")
    
    def _remove_startup_shortcut(self):
        """Remove shortcut from startup folder."""
        try:
            # Remove batch file
            batch_path = self.startup_folder / f"{self.app_name}.bat"
            if batch_path.exists():
                batch_path.unlink()
                print(f"Startup shortcut removed from {batch_path}")
            
            # Remove .lnk file if exists
            shortcut_path = self.startup_folder / f"{self.app_name}.lnk"
            if shortcut_path.exists():
                shortcut_path.unlink()
                print(f"Startup shortcut removed from {shortcut_path}")
                
        except Exception as e:
            print(f"Error removing startup shortcut: {e}")
    
    def get_current_exe_path(self) -> str:
        """Get the current executable path."""
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            exe_path = sys.executable
        else:
            # Running as script
            exe_path = sys.argv[0]
        
        # Convert to absolute path and normalize
        exe_path = os.path.abspath(exe_path)
        return exe_path
    
    def setup_autostart(self) -> bool:
        """Setup auto-start with current executable path."""
        exe_path = self.get_current_exe_path()
        return self.enable(exe_path)
    
    def remove_autostart(self) -> bool:
        """Remove auto-start configuration."""
        return self.disable()
    
    def cleanup_invalid_entries(self) -> bool:
        """Clean up invalid autostart entries (when exe file doesn't exist)."""
        try:
            # Check registry entry
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.registry_key) as key:
                try:
                    exe_path, _ = winreg.QueryValueEx(key, self.app_name)
                    # Check if the exe file exists
                    if not os.path.exists(exe_path):
                        print(f"Invalid autostart entry found: {exe_path}")
                        print("Cleaning up invalid entry...")
                        return self.disable()
                    else:
                        print(f"Valid autostart entry: {exe_path}")
                        return True
                except FileNotFoundError:
                    print("No autostart entry found in registry")
                    return True
        except Exception as e:
            print(f"Error checking autostart entry: {e}")
            return False
