"""Zbieracz - serwer napastnika w laboratorium 6. Zapisuje w logu wiersz kazdego zadania.

Dziala pod inna nazwa hosta niz aplikacja (localhost zamiast 127.0.0.1),
wiec przegladarka nie wysyla mu ciasteczek aplikacji. Widzi tylko to, co wysle skrypt.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote


class Zbieracz(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"ZEBRANO: {unquote(self.path)}", flush=True)
        self.send_response(204)
        self.end_headers()

    def log_message(self, *args):
        pass


HTTPServer(("0.0.0.0", 8081), Zbieracz).serve_forever()
