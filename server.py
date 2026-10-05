from wsgiref.simple_server import make_server
import importlib, sys


def import_app(target):
    module_name, app_name = target.split(":")
    module = importlib.import_module(module_name)
    return getattr(module, app_name)

class WhiteServer:
    def __init__(self, app, host="127.0.0.1", port=8000):
        self.host = host
        self.port = port
        self.app = app


    def runServer(self):
        Server = make_server(self.host, self.port, self.app)
        print(f"Serving on http://{self.host}:{self.port}")
        Server.serve_forever()


def startServer():
    if len(sys.argv) < 2:
        print("Usage: python server.py <module_name>:<app_name>")
        sys.exit(1)
    target = sys.argv[1]
    app = import_app(target)
    server = WhiteServer(app=app)
    server.runServer()

if __name__ == "__main__":
    startServer()