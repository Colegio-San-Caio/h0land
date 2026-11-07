from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class MockDinerNode(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/data':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            # Dynamic high-speed MOSFET pulse simulation metrics
            response_data = {"red": 88000, "ir": 63000, "mosfet_gate": "ACTIVE_DISCHARGE"}
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    # Using 8888 guarantees a fresh network port connection
    server = HTTPServer(('127.0.0.1', 8888), MockDinerNode)
    print("Mock SRT-Diner server running cleanly on port 8888...")
    server.handle_request()

