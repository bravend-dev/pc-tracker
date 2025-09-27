# PCTracker - Thiết kế App Đơn giản hóa

## Tổng quan
PCTracker là ứng dụng theo dõi thời gian sử dụng máy tính với giao diện đơn giản, chạy nền và tự khởi động. Thiết kế mới tập trung vào việc tinh gọn code và dễ bảo trì.

## Kiến trúc App

### 1. Cấu trúc thư mục mới
```
PCTracker/
├── main.py                 # Entry point chính
├── src/                    # Source code chính
│   ├── core/              # Core business logic
│   │   ├── tracker.py     # UsageTracker class
│   │   └── config.py      # Configuration management
│   ├── gui/               # GUI components
│   │   └── main_window.py # PCTrackerGUI class
│   ├── system/            # System integration
│   │   └── autostart.py   # AutoStart class
│   └── utils/             # Utility functions
├── scripts/               # Build and utility scripts
│   ├── build.py
│   ├── build.bat
│   ├── run.bat
│   └── clean.bat
├── assets/                # Static assets
│   └── logo.ico
├── data/                  # Data storage
│   └── usage_data.json
├── requirements.txt       # Dependencies
└── pc-tracker.spec       # PyInstaller spec
```

### 2. Các module chính

#### 2.1 main.py - Entry Point
```python
# Chức năng:
- Khởi tạo app
- Chọn chế độ chạy (GUI/Background)
- Xử lý command line arguments
- Quản lý lifecycle của app
```

#### 2.2 src/core/config.py - Cấu hình
```python
# Chức năng:
- Load/save cấu hình từ file JSON
- Các setting cơ bản: theme, window size, tracking interval
- Default values
- Validation cấu hình
```

#### 2.3 src/core/tracker.py - Core Logic
```python
# Chức năng:
- Theo dõi hoạt động máy tính
- Lưu trữ dữ liệu session
- Tính toán thống kê (ngày/tuần/tháng)
- Callback system cho real-time updates
```

#### 2.4 src/gui/main_window.py - Giao diện
```python
# Chức năng:
- Main window với CustomTkinter
- Hiển thị thống kê real-time
- Biểu đồ đơn giản (matplotlib)
- Menu cơ bản (Start/Stop, Settings, Exit)
- Minimize to tray
```

#### 2.5 src/system/autostart.py - Tự khởi động
```python
# Chức năng:
- Tự khởi động cùng Windows
- Registry management
- Startup folder management
- Enable/disable autostart
- Cross-platform support (Windows focus)
```

#### 2.6 scripts/ - Build Scripts
```python
# Chức năng:
- build.py: Automated build process
- build.bat: Windows build script
- run.bat: Quick run script
- clean.bat: Clean build artifacts
```

## Thiết kế UI đơn giản

### 1. Main Window Layout
```
┌─────────────────────────────────────┐
│ PCTracker - Computer Usage Monitor  │
├─────────────────────────────────────┤
│ [Start/Stop] [Status: Running]      │
├─────────────────────────────────────┤
│ Current Session: 02:15:30           │
│ Today's Usage:   04:22:15           │
├─────────────────────────────────────┤
│ Weekly Chart (Simple Bar Chart)     │
│ ████████████████████████████████    │
│ Mon Tue Wed Thu Fri Sat Sun         │
├─────────────────────────────────────┤
│ [Settings] [Export] [Minimize]      │
└─────────────────────────────────────┘
```

### 2. Tray Icon Menu
```
┌─────────────────┐
│ Show Window     │
│ Start/Stop      │
│ ─────────────── │
│ Settings        │
│ Export Data     │
│ ─────────────── │
│ Exit            │
└─────────────────┘
```

## Chức năng chính

### 1. Tracking
- **Auto-start tracking**: Tự động bắt đầu khi khởi động app
- **Background monitoring**: Chạy nền không ảnh hưởng hiệu suất
- **Activity detection**: Phát hiện hoạt động người dùng
- **Session management**: Quản lý các phiên làm việc

### 2. Data Management
- **Real-time updates**: Cập nhật dữ liệu theo thời gian thực
- **Persistent storage**: Lưu trữ dữ liệu vào JSON file
- **Statistics calculation**: Tính toán thống kê ngày/tuần/tháng
- **Data export**: Xuất dữ liệu ra CSV

### 3. UI Features
- **Modern dark theme**: Giao diện tối hiện đại
- **Minimize to tray**: Thu nhỏ vào system tray
- **Real-time display**: Hiển thị thời gian real-time
- **Simple charts**: Biểu đồ đơn giản, dễ hiểu

### 4. System Integration
- **Auto-start**: Tự khởi động cùng Windows
- **System tray**: Tích hợp với system tray
- **Graceful shutdown**: Tắt app an toàn

## Cấu hình đơn giản

### config.json
```json
{
  "app": {
    "name": "PCTracker",
    "version": "2.0.0",
    "theme": "dark"
  },
  "tracking": {
    "enabled": true,
    "interval": 1,
    "data_file": "data/usage_data.json"
  },
  "gui": {
    "width": 800,
    "height": 600,
    "minimize_to_tray": true,
    "show_notifications": true
  },
  "autostart": {
    "enabled": false,
    "start_minimized": true
  }
}
```