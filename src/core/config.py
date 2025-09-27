"""
Simple configuration management for PCTracker.
"""


class Config:
    """Simple configuration class with default values only."""
    
    def __init__(self):
        self.config = self._get_default_config()
    
    def _get_default_config(self):
        """Get default configuration."""
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
                "enabled": False,
                "start_minimized": False
            }
        }
    
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


# Global config instance
config = Config()