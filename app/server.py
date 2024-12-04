from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import mimetypes
from pathlib import Path
import os

class ValorantDataHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_GET(self):
        print(f"Request path: {self.path}")
        if self.path == '/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = self.read_data_files()
            print(f"Sending data: {data}")
            self.wfile.write(json.dumps(data).encode())
            return
        elif self.path.startswith('/assets/'):
            # Remove '/assets/' from path and get full path
            file_path = self.path[1:]  # Remove leading slash
            print(f"Looking for asset at: {file_path}")
            if Path(file_path).exists():
                self.send_response(200)
                content_type = mimetypes.guess_type(str(file_path))[0]
                self.send_header('Content-type', content_type)
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
            else:
                print(f"File not found: {file_path}")
                self.send_error(404, "File not found")
                return

        return super().do_GET()

    def read_data_files(self):
        data = {}
        data_dir = Path("data")
        
        if data_dir.exists():
            # Read all text files
            for file in data_dir.glob("*.txt"):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        data[file.stem] = f.read().strip()
                except Exception as e:
                    print(f"Error reading {file}: {e}")

            # Handle logo paths
            logo_dir = Path("assets/logos")
            if logo_dir.exists():
                for team in ['team1', 'team2']:
                    logo_files = list(logo_dir.glob(f"{team}.*"))
                    if logo_files:
                        # Use absolute path for logos
                        logo_path = f'/assets/logos/{logo_files[0].name}'
                        data[f"{team}_logo"] = logo_path
                        print(f"Found {team} logo: {logo_path}")

        return data

def run_server():
    base_dir = Path(__file__).parent.parent
    print(f"Changing to base directory: {base_dir}")
    os.chdir(base_dir)
    
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, ValorantDataHandler)
    print(f"Server running at http://localhost:8080")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
