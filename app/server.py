from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from pathlib import Path
import os

class ValorantDataHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super().end_headers()

    def do_GET(self):
        if self.path == '/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Get data from files
            data = self.read_data_files()
            self.wfile.write(json.dumps(data).encode())
            return
        
        # Serve files from overlay directory
        if self.path == '/':
            self.path = '/overlay/index.html'
        
        return super().do_GET()

    def read_data_files(self):
        data = {}
        data_dir = Path("data")
        
        if data_dir.exists():
            for file in data_dir.glob("*.txt"):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        data[file.stem] = f.read().strip()
                except Exception as e:
                    print(f"Error reading {file}: {e}")
        
        return data

def run_server():
    # Change to project root directory
    os.chdir(Path(__file__).parent.parent)
    
    print("Starting server on port 8080...")
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, ValorantDataHandler)
    print("Server is running. Press Ctrl+C to stop.")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
