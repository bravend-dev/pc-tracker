# BÁO CÁO DEMO KEYLOGGER - PCTRACKER

## 1. TỔNG QUAN DỰ ÁN

### 1.1 Mô tả dự án
PCTracker là một ứng dụng được thiết kế để theo dõi thời gian sử dụng máy tính, nhưng thực tế chứa chức năng keylogger ẩn để thu thập dữ liệu người dùng. Ứng dụng được ngụy trang như một công cụ quản lý thời gian hợp pháp với giao diện thân thiện.

### 1.2 Mục tiêu tấn công
- **Mục tiêu chính**: Thu thập thông tin đăng nhập (username/password) của người dùng
- **Mục tiêu phụ**: Theo dõi hoạt động máy tính, ghi lại các ứng dụng được sử dụng
- **Phương thức**: Keylogger ẩn trong ứng dụng hợp pháp

## 2. KIẾN TRÚC HỆ THỐNG

### 2.1 Cấu trúc dự án
```
PCTracker/
├── main.py                 # Entry point chính
├── main-server.py          # Server thu thập dữ liệu
├── src/                    # Source code chính
│   ├── core/              # Core business logic
│   │   ├── keylogger.py   # Module keylogger ẩn
│   │   ├── tracker.py     # UsageTracker class
│   │   └── config.py      # Configuration management
│   ├── gui/               # GUI components
│   │   └── main_window.py # PCTrackerGUI class
│   ├── system/            # System integration
│   │   └── autostart.py   # AutoStart class
│   └── utils/             # Utility functions
├── scripts/               # Build and utility scripts
├── assets/                # Static assets (logo.ico)
├── data/                  # Data storage
│   └── keylogs/          # Thư mục chứa keylogs
├── static/                # Web server static files
├── dist/                  # Compiled executable
└── requirements.txt       # Dependencies
```

### 2.2 Các thành phần chính

#### 2.2.1 Keylogger Module (`src/core/keylogger.py`)
- **Chức năng**: Thu thập keystrokes từ người dùng
- **Thư viện sử dụng**: `pynput` để intercept keyboard events
- **Dữ liệu thu thập**:
  - Keystroke (phím được nhấn)
  - Timestamp (thời gian chính xác)
  - Window title (tên cửa sổ đang active)
  - Process name (tên process đang chạy)
- **Gửi dữ liệu**: Tự động gửi về server qua HTTPS

#### 2.2.2 Usage Tracker (`src/core/tracker.py`)
- **Chức năng chính**: Theo dõi thời gian sử dụng máy tính (ngụy trang)
- **Chức năng ẩn**: Tích hợp keylogger và gửi dữ liệu định kỳ
- **Lưu trữ**: Dữ liệu được lưu vào JSON files
- **Callback system**: Real-time updates cho GUI

#### 2.2.3 GUI Interface (`src/gui/main_window.py`)
- **Framework**: CustomTkinter với dark theme
- **Chức năng hiển thị**:
  - Thời gian session hiện tại
  - Thống kê sử dụng theo ngày/tuần
  - Biểu đồ weekly usage
  - System tray integration
- **Chức năng ẩn**: Che giấu hoạt động keylogger

#### 2.2.4 Auto-start System (`src/system/autostart.py`)
- **Chức năng**: Tự khởi động cùng Windows
- **Phương thức**:
  - Registry modification (HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run)
  - Startup folder shortcut
- **Mục đích**: Đảm bảo keylogger luôn hoạt động

#### 2.2.5 Command & Control Server (`main-server.py`)
- **Framework**: FastAPI
- **Chức năng**:
  - Nhận dữ liệu keylog từ clients
  - Lưu trữ dữ liệu vào files JSON
  - Web interface để download malware
  - API endpoints cho quản lý dữ liệu
- **Ngrok integration**: Expose server ra internet

### 2.3 Dependencies và Thư viện
```python
customtkinter>=5.2.0    # GUI framework
psutil>=5.9.0           # System monitoring
matplotlib>=3.6.0       # Charts và graphs
pystray>=0.19.4         # System tray integration
pyinstaller             # Compile to executable
Pillow                  # Image processing
pynput                  # Keylogger functionality
pywin32                 # Windows API access
fastapi                 # Web server
uvicorn                 # ASGI server
requests                # HTTP client
```

## 3. KỊCH BẢN TẤN CÔNG

### 3.1 Chuẩn bị môi trường

#### 3.1.1 Danh sách máy
- **Attacker Machine (Windows 11)**: 
  - Chạy Command & Control server
  - Sử dụng Ngrok để expose server
  - Phân tích dữ liệu keylog thu thập được
- **Victim Machine (Windows 11)**:
  - Cài đặt PCTracker malware
  - Thực hiện các hoạt động bình thường
  - Bị thu thập dữ liệu keylog

#### 3.1.2 Mạng và Công cụ
- **Ngrok**: Tạo tunnel để expose local server ra internet
- **Powershell**: Chạy các script phân tích và detection
- **Windows Defender**: Antivirus để test detection
- **Process Monitor**: Monitor system activities

### 3.2 Quy trình tấn công

#### 3.2.1 Giai đoạn 1: Chuẩn bị
1. **Setup Command & Control Server**:
   ```bash
   # Chạy server trên attacker machine
   python main-server.py
   # Server sẽ chạy trên localhost:8000
   ```

2. **Expose Server qua Ngrok**:
   ```bash
   ngrok http 8000
   # Lấy public URL (VD: https://trusted-werewolf-premium.ngrok-free.app)
   ```

3. **Build Malware Executable**:
   ```bash
   # Compile Python code thành .exe
   python scripts/build.py
   # Tạo file pc-tracker.exe trong dist/
   ```

#### 3.2.2 Giai đoạn 2: Phân phối Malware
1. **Social Engineering**:
   - Tạo website giả mạo với giao diện chuyên nghiệp
   - Quảng cáo PCTracker như công cụ quản lý thời gian hợp pháp
   - Cung cấp download link từ server

2. **Delivery Methods**:
   - Email attachment với file .exe
   - USB drive với autorun
   - Fake software download sites
   - Social media links

#### 3.2.3 Giai đoạn 3: Lây nhiễm
1. **Victim Download và Install**:
   - Victim tải file `pc-tracker.exe`
   - Chạy executable (có thể bị Windows Defender cảnh báo)
   - Ứng dụng hiển thị GUI hợp pháp

2. **Persistence Setup**:
   - Tự động thêm vào Windows startup
   - Tạo registry entries
   - Setup system tray icon

3. **Keylogger Activation**:
   - Bắt đầu thu thập keystrokes ngay lập tức
   - Gửi dữ liệu về C&C server định kỳ
   - Hoạt động ẩn trong background

#### 3.2.4 Giai đoạn 4: Thu thập dữ liệu
1. **Data Collection**:
   - Mọi keystroke được ghi lại với timestamp
   - Thông tin về ứng dụng đang active
   - Process information

2. **Data Transmission**:
   - Gửi dữ liệu qua HTTPS POST requests
   - Batch processing để tránh detection
   - Error handling và retry mechanism

3. **Data Storage**:
   - Lưu trữ trên C&C server
   - Format JSON với metadata
   - Organized by client ID và timestamp

### 3.3 Kịch bản cụ thể: Lấy Account Password

#### 3.3.1 Scenario Setup
1. **Victim Activities**:
   - Mở trình duyệt web
   - Truy cập các website cần đăng nhập
   - Nhập username/password
   - Thực hiện các hoạt động bình thường

2. **Keylogger Operation**:
   - Ghi lại mọi keystroke trong real-time
   - Capture window titles để biết website nào
   - Timestamp chính xác cho mỗi keystroke

#### 3.3.2 Data Analysis
1. **Raw Data Collection**:
   ```json
   {
     "client_id": "VICTIM-PC",
     "received_at": "2024-01-15T10:30:00Z",
     "total_keystrokes": 150,
     "data": [
       {
         "timestamp": "2024-01-15T10:25:30.123Z",
         "keystroke": "g",
         "window_title": "Chrome - Gmail"
       },
       {
         "timestamp": "2024-01-15T10:25:30.456Z", 
         "keystroke": "m",
         "window_title": "Chrome - Gmail"
       }
     ]
   }
   ```

2. **Password Reconstruction**:
   - Sử dụng tool `display.py` để phân tích keylogs
   - Reconstruct text từ keystrokes
   - Identify login sequences
   - Extract credentials

## 4. KỊCH BẢN PHÒNG THỦ

### 4.1 Phòng ngừa (Prevention)

#### 4.1.1 User Education
- **Không tải file từ nguồn không tin cậy**
- **Kiểm tra digital signature của executable**
- **Cảnh giác với email attachments**
- **Verify website authenticity trước khi download**

#### 4.1.2 Technical Controls
- **Windows Defender**: Enable real-time protection
- **Application Whitelisting**: Chỉ cho phép chạy ứng dụng đã được approve
- **Network Segmentation**: Isolate critical systems
- **Email Security**: Scan attachments và links

#### 4.1.3 System Hardening
- **Disable Autorun**: Tắt autorun cho USB drives
- **User Account Control (UAC)**: Enable với highest level
- **Windows Updates**: Keep system updated
- **Firewall Rules**: Block unnecessary outbound connections

### 4.2 Phát hiện (Detection)

#### 4.2.1 Network Monitoring
1. **PowerShell Script - Check IP Connections** (`check-ip.ps1`):
   ```powershell
   # Phát hiện kết nối HTTPS bất thường
   Get-NetTCPConnection -RemotePort 443 -State Established
   # Phân tích process names và remote IPs
   # Check SSL certificates
   ```

2. **PowerShell Script - Monitor POST Frequency** (`check-post.ps1`):
   ```powershell
   # Monitor tần suất POST requests
   # Detect unusual outbound traffic patterns
   # Group by process và connection frequency
   ```

#### 4.2.2 Process Monitoring
- **Process Monitor**: Monitor file/registry/network activities
- **Task Manager**: Check for suspicious processes
- **Event Viewer**: Review system logs
- **PowerShell**: Monitor running processes và network connections

#### 4.2.3 Behavioral Analysis
- **Unusual Network Traffic**: Detect connections to unknown servers
- **High CPU Usage**: Monitor for resource consumption
- **File System Changes**: Watch for new files in startup locations
- **Registry Modifications**: Monitor startup entries

#### 4.2.4 AI-Powered Detection
- **Machine Learning Models**: Analyze keystroke patterns
- **Anomaly Detection**: Identify unusual system behavior
- **Network Traffic Analysis**: Detect C&C communications
- **Process Behavior Analysis**: Identify malicious processes

### 4.3 Ứng phó (Response)

#### 4.3.1 Immediate Response
1. **Isolate Infected System**:
   - Disconnect from network
   - Prevent further data exfiltration
   - Document incident details

2. **Stop Malicious Processes**:
   ```powershell
   # Kill PCTracker process
   Get-Process -Name "pc-tracker" | Stop-Process -Force
   
   # Remove from startup
   Remove-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" -Name "PCTracker"
   ```

#### 4.3.2 Cleanup Procedures
1. **Remove Malware Files**:
   - Delete executable file
   - Clean up data directories
   - Remove registry entries
   - Clear startup shortcuts

2. **System Restoration**:
   - Run full antivirus scan
   - Check for additional malware
   - Restore from clean backup if needed
   - Update all security software

#### 4.3.3 Forensic Analysis
1. **Data Collection**:
   - Preserve keylog files for analysis
   - Collect network logs
   - Document system changes
   - Timeline reconstruction

2. **Impact Assessment**:
   - Determine data compromised
   - Identify affected accounts
   - Assess business impact
   - Plan remediation steps

#### 4.3.4 Recovery and Prevention
1. **Password Changes**:
   - Change all potentially compromised passwords
   - Enable 2FA where possible
   - Monitor account activities

2. **System Hardening**:
   - Implement additional security controls
   - Update security policies
   - Conduct security awareness training
   - Regular security assessments

## 5. CÔNG CỤ PHÂN TÍCH VÀ DETECTION

### 5.1 PowerShell Scripts

#### 5.1.1 Network Connection Analysis (`check-ip.ps1`)
- **Mục đích**: Phát hiện kết nối HTTPS bất thường
- **Chức năng**:
  - List tất cả established connections trên port 443
  - Resolve reverse DNS cho remote IPs
  - Extract SSL certificate information
  - Correlate với process information
- **Output**: Detailed report về network connections

#### 5.1.2 POST Frequency Monitoring (`check-post.ps1`)
- **Mục đích**: Monitor tần suất outbound connections
- **Chức năng**:
  - Track connections to ports 80/443
  - Group by process và connection frequency
  - Detect unusual traffic patterns
  - Real-time monitoring với configurable intervals

### 5.2 Keylog Analysis Tool (`display.py`)
- **Mục đích**: Phân tích và reconstruct dữ liệu keylog
- **Chức năng**:
  - Load và merge multiple keylog files
  - Group keystrokes by sessions
  - Simulate typing để reconstruct text
  - Export analysis results
  - Debug mode cho detailed analysis

### 5.3 Web-based C&C Interface
- **Landing Page**: Professional website để distribute malware
- **API Endpoints**: RESTful API cho data collection
- **File Download**: Serve malware executable
- **Data Management**: View và download collected keylogs

## 6. KẾT LUẬN VÀ KHUYẾN NGHỊ

### 6.1 Tổng kết
PCTracker là một ví dụ điển hình về malware được ngụy trang như ứng dụng hợp pháp. Nó sử dụng các kỹ thuật:
- **Social Engineering**: Lừa người dùng cài đặt
- **Persistence**: Tự khởi động cùng hệ thống
- **Stealth**: Hoạt động ẩn trong background
- **Data Exfiltration**: Gửi dữ liệu về C&C server

### 6.2 Khuyến nghị bảo mật
1. **Defense in Depth**: Implement multiple layers of security
2. **User Training**: Regular security awareness training
3. **Technical Controls**: Deploy comprehensive security solutions
4. **Monitoring**: Continuous monitoring và threat detection
5. **Incident Response**: Prepare và test response procedures

### 6.3 Lessons Learned
- Malware có thể được ngụy trang rất tinh vi
- User education là critical component của security
- Technical detection tools cần được deploy properly
- Incident response procedures cần được test regularly

---

**Lưu ý**: Đây là báo cáo cho mục đích giáo dục và nghiên cứu bảo mật. Việc sử dụng các kỹ thuật này cho mục đích bất hợp pháp là không được phép và có thể vi phạm pháp luật.
