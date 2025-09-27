"""
Main entry point for PCTracker application.
"""
import sys
import os
import argparse
from pathlib import Path

# Import simplified modules
from gui import PCTrackerGUI
from config import config


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="PCTracker - Computer Usage Monitor")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    print("Starting PCTracker...")
    
    try:
        # Run with GUI (default)
        print("Running with GUI")
        app = PCTrackerGUI()
        app.run()
            
    except KeyboardInterrupt:
        print("Application interrupted by user")
    except Exception as e:
        print(f"Application error: {e}")
        sys.exit(1)
    finally:
        print("Application shutting down")


if __name__ == "__main__":
    main()