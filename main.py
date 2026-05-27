import asyncio
import base64
import json
import os
import sys
import threading
import time
import webbrowser
from urllib.parse import urlparse, urlunparse
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from ping3 import ping
import uvicorn

# When running as an .exe with --noconsole, standard output crashes on emojis/special characters.
# This explicitly disables outputting logs to the hidden console to prevent the charmap error.
if getattr(sys, 'frozen', False):
    sys.stdout = open(os.devnull, 'w', encoding='utf-8')
    sys.stderr = open(os.devnull, 'w', encoding='utf-8')

try:
    import webview
    HAS_WEBVIEW = True
except ImportError:
    HAS_WEBVIEW = False

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller .exe """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = FastAPI()

# Input schemas for the API
class PingRequest(BaseModel):
    ips: list[str]

class ConfigUpdateRequest(BaseModel):
    configs: list[str]
    selected_ips: list[str]
    new_port: int | None = None

# Helper to execute system pings asynchronously
async def async_ping(ip: str):
    try:
        loop = asyncio.get_event_loop()
        delay = await loop.run_in_executor(None, ping, ip, 1.5) # 1.5s timeout
        if delay is not None and delay is not False:
            return {"ip": ip, "status": "online", "latency": round(delay * 1000)}
        return {"ip": ip, "status": "offline", "latency": None}
    except Exception:
        return {"ip": ip, "status": "error", "latency": None}

@app.get("/", response_class=HTMLResponse)
async def read_index():
    # Safely load the HTML file whether running as a script or an .exe
    html_path = get_resource_path("index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/ping")
async def bulk_ping(request: PingRequest):
    tasks = [async_ping(ip.strip()) for ip in request.ips if ip.strip()]
    results = await asyncio.gather(*tasks)
    results.sort(key=lambda x: (x['status'] != 'online', x['latency'] or float('inf')))
    return results

@app.post("/api/process-configs")
async def process_configs(request: ConfigUpdateRequest):
    output_configs = []
    
    for config in request.configs:
        config = config.strip()
        if not config:
            continue
            
        for ip in request.selected_ips:
            try:
                # Handle VMESS (Usually base64 encoded JSON)
                if config.startswith("vmess://"):
                    raw_b64 = config[8:]
                    raw_b64 += "=" * ((4 - len(raw_b64) % 4) % 4)
                    decoded = base64.b64decode(raw_b64).decode('utf-8')
                    data = json.loads(decoded)
                    
                    data["add"] = ip
                    if request.new_port:
                        data["port"] = request.new_port
                    
                    encoded = base64.b64encode(json.dumps(data).encode('utf-8')).decode('utf-8')
                    output_configs.append(f"vmess://{encoded}")
                    
                # Handle VLESS / SS / Trojan
                elif config.startswith("vless://") or config.startswith("trojan://") or config.startswith("ss://"):
                    parsed = urlparse(config)
                    user_info = parsed.netloc.split("@")[0] if "@" in parsed.netloc else ""
                    
                    port = request.new_port if request.new_port else (parsed.port if parsed.port else 443)
                    new_netloc = f"{user_info}@{ip}:{port}" if user_info else f"{ip}:{port}"
                    
                    updated_url = urlunparse((
                        parsed.scheme,
                        new_netloc,
                        parsed.path,
                        parsed.params,
                        parsed.query,
                        parsed.fragment
                    ))
                    output_configs.append(updated_url)
                else:
                    continue
            except Exception as e:
                continue
                
    return {"generated_count": len(output_configs), "configs": output_configs}

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="critical")

if __name__ == "__main__":
    print("Starting IPWeaver...")
    
    # 1. Start the FastAPI server in a background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # 2. Give the server a second to start up
    time.sleep(1.5)
    
    # 3. Detect environment and open native UI or Web Browser
    if getattr(sys, 'frozen', False) and HAS_WEBVIEW:
        # Running as compiled PyInstaller .exe
        webview.create_window('IP Weaver for V2Ray', 'http://127.0.0.1:8000', width=1100, height=800)
        webview.start()
    else:
        # Running open-source script locally
        print("Opening interface in your default web browser...")
        webbrowser.open("http://127.0.0.1:8000")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down IPWeaver...")