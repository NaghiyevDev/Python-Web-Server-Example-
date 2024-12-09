# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from jinja2 import Environment, FileSystemLoader

import time
import os
import json

from users import get_users, get_user

hostName = "localhost"
serverPort = 8080

templates_directory = os.path.abspath("templates")

static_directory = os.path.abspath('static')


# Configure Jinja2 environment
env = Environment(loader=FileSystemLoader(templates_directory))

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.get_admin_data()
        if self.path.startswith('/static/'):
            self.serve_static_file(self.path[len('/static/'):])
        if self.path == "/":  # Handle the root path
            self.render_template('index.html', {'title': 'Home Page'})
        elif self.path == "/about":  # Handle the '/about' path
            self.render_template('about.html', {'title': 'About Page'})
        elif self.path == "/contact":
            self.render_template("contact.html", {'title': 'Contact Page'})
        elif self.path.startswith('/profile/'):
            username = self.path[len('/profile/'):]
            print('username: ', username)
            user = get_user(username)
            print('User: ', user)
        
        else:  # Handle unknown paths
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>404 Not Found</title></head>", "utf-8"))
            self.wfile.write(bytes("<body><h1>404 - Page Not Found</h1></body></html>", "utf-8"))

    def render_template(self, template_name, context):
        try:
            template = env.get_template(template_name)
            html_content = template.render(context)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(html_content, "utf-8"))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(bytes(f"<h1>500 - Internal Server Error</h1><p>{e}</p>", "utf-8"))
    
    def serve_static_file(self, relative_path):
        safe_path = os.path.normpath(os.path.join(static_directory, relative_path))
        if not safe_path.startswith(static_directory):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(bytes("<h1>403 - Forbidden</h1>", "utf-8"))
            return

        if os.path.exists(safe_path):
            content_type = "text/css" if safe_path.endswith(".css") else "application/octet-stream"
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()
            with open(safe_path, "rb") as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(f"<h1>File {relative_path} Not Found</h1>", "utf-8"))


    def get_admin_data(self, **args):
        users = get_users()
        for user in users:
            if user['role'] == 'Admin':
               # print('Admin user:', user['username'])
                return user


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")