# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

# Get the current directory
current_dir = Path.cwd()

# Define data files to include
datas = []

# Add assets directory if it exists (optional - now using embedded icons)
# if os.path.exists('assets'):
#     datas.append(('assets', 'assets'))

# Add data directory if it exists
if os.path.exists('data'):
    datas.append(('data', 'data'))

# Define hidden imports
hiddenimports = [
    'customtkinter',
    'psutil',
    'matplotlib',
    'matplotlib.backends.backend_tkagg',
    'pystray',
    'PIL',
    'PIL.Image',
    'winreg',
    'tkinter',
    'tkinter.messagebox',
    'threading',
    'json',
    'datetime',
    'pathlib',
]

# Define the main analysis
a = Analysis(
    ['main.py'],
    pathex=[str(current_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Remove duplicate files
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Create the executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='pc-tracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/logo.ico' if os.path.exists('assets/logo.ico') else None,
    version_file=None,
)

