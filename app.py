import socket 
 
import uvicorn 
from fastapi import FastAPI 
 
 
app = FastAPI() 
 
 
@app.get("/") 
def hello(): 
    return {"message": "Userbot API running"} 
 
 
def find_available_port(start_port=7860, max_port=7960): 
    """Cari port yang tersedia""" 
    for port in range(start_port, max_port): 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
            if s.connect_ex(("localhost", port)) != 0: 
                return port 
    return None  # Jika tidak ada port yang tersedia 
 
 
if __name__ == "__main__": 
    port = find_available_port() 
    if port: 
        print(f"Port {port} is available. Starting server...") 
        uvicorn.run(app, host="0.0.0.0", port=port) 
    else: 
        print("No available ports found in the range.")
