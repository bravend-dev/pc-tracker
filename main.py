"""
Main entry point for PCTracker application.
"""
import sys
from src.gui import PCTrackerGUI

def main():
    """Main function."""

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