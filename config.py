"""
Simple configuration management for PCTracker.
"""
import json
import os
from pathlib import Path


class Config:
    """Simple configuration class."""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_default_config()
    
    def _load_default_config(self):
        """Load default configuration."""
        return {
            "app": {
                "name": "PCTracker",
                "version": "2.0.0",
                "theme": "dark"
            },
            "tracking": {
                "enabled": True,
                "interval": 1,
                "data_file": "data/usage_data.json"
            },
            "gui": {
                "width": 800,
                "height": 600,
                "minimize_to_tray": True,
                "show_notifications": True
            },
            "autostart": {
                "enabled": True,
                "start_minimized": True
            }
        }
    
    def save_config(self):
        """Save configuration to file."""
        try:
            # Ensure data directory exists
            data_dir = Path(self.config["tracking"]["data_file"]).parent
            data_dir.mkdir(exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print(f"Config saved to {self.config_file}")
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def _merge_config(self, default, loaded):
        """Merge loaded config with defaults."""
        for key, value in loaded.items():
            if key in default:
                if isinstance(value, dict) and isinstance(default[key], dict):
                    self._merge_config(default[key], value)
                else:
                    default[key] = value
    
    def get(self, section, key=None):
        """Get configuration value."""
        if key is None:
            return self.config.get(section, {})
        return self.config.get(section, {}).get(key)
    
    def set(self, section, key, value):
        """Set configuration value."""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        self.save_config()


# Global config instance
config = Config()
