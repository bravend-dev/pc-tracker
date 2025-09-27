#!/usr/bin/env python3
"""
Build script for PCTracker installer.
This script automates the process of building the executable using PyInstaller.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed."""
    required_packages = [
        ('customtkinter', 'customtkinter'),
        ('psutil', 'psutil'),
        ('matplotlib', 'matplotlib'),
        ('pystray', 'pystray'),
        ('Pillow', 'PIL'),
        ('pyinstaller', 'PyInstaller')
    ]
    
    missing_packages = []
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install " + " ".join(missing_packages))
        return False
    
    return True

def clean_build():
    """Clean previous build artifacts."""
    print("Cleaning previous build artifacts...")
    
    # Remove build directories
    dirs_to_remove = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Removed {dir_name}/")
    
    # Remove .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))

def build_executable():
    """Build the executable using PyInstaller."""
    print("Building executable with PyInstaller...")
    
    try:
        # Run PyInstaller with the spec file
        cmd = [sys.executable, '-m', 'PyInstaller', '../pc-tracker.spec']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Build completed successfully!")
            return True
        else:
            print("Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"Error during build: {e}")
        return False

def create_installer_package():
    """Create a complete installer package."""
    print("Creating installer package...")
    
    dist_dir = Path('../dist')
    if not dist_dir.exists():
        print("Dist directory not found. Build may have failed.")
        return False
    
    # Find the executable
    exe_files = list(dist_dir.glob('pc-tracker.exe'))
    if not exe_files:
        print("Executable not found in dist directory.")
        return False
    
    exe_file = exe_files[0]
    
    # Create installer directory
    installer_dir = Path('../installer')
    installer_dir.mkdir(exist_ok=True)
    
    # Copy executable
    installer_exe = installer_dir / 'pc-tracker.exe'
    shutil.copy2(exe_file, installer_exe)
    print(f"Copied executable to {installer_exe}")
    
    # Create README for installer
    readme_content = """# PCTracker Installer

## Installation Instructions

1. Run `pc-tracker.exe` to start the application
2. The application will automatically:
   - Start tracking your computer usage
   - Add itself to Windows startup (auto-start)
   - Create a system tray icon for easy access

## Features

- Real-time computer usage tracking
- Daily and weekly usage statistics
- Modern dark theme interface
- System tray integration
- Auto-start with Windows
- Data persistence across sessions

## Usage

- The application will start automatically when you run the installer
- Click the system tray icon to show/hide the main window
- View your usage statistics in real-time
- Data is automatically saved to the application directory

## Uninstallation

To remove PCTracker:
1. Close the application (right-click tray icon → Exit)
2. Delete the application folder
3. The auto-start entry will be automatically removed

## Support

For issues or questions, please check the application logs in the data directory.
"""
    
    readme_file = installer_dir / 'README.txt'
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"Created README at {readme_file}")
    print(f"Installer package created in {installer_dir}/")
    
    return True

def main():
    """Main build process."""
    print("=== PCTracker Build Script ===")
    print()
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Clean previous builds
    clean_build()
    
    # Build executable
    if not build_executable():
        sys.exit(1)
    
    # Create installer package
    if not create_installer_package():
        sys.exit(1)
    
    print()
    print("=== Build Complete ===")
    print("The installer package is ready in the 'installer/' directory")
    print("You can now distribute the pc-tracker.exe file")

if __name__ == "__main__":
    main()
