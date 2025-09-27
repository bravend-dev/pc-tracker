@echo off
echo Cleaning previous build artifacts...

REM Remove build directories
if exist "build" (
    echo Removing build/ directory...
    rmdir /s /q "build"
)

if exist "dist" (
    echo Removing dist/ directory...
    rmdir /s /q "dist"
)

if exist "__pycache__" (
    echo Removing __pycache__/ directory...
    rmdir /s /q "__pycache__"
)

REM Remove .pyc files
echo Removing .pyc files...
for /r . %%i in (*.pyc) do del "%%i" /q

echo Clean completed!
pause
