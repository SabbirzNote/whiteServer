from wsgiref.simple_server import make_server
import importlib, sys
from multiprocessing import Process


def import_app(target):
    module_name, app_name = target.split(":")
    module = importlib.import_module(module_name)
    return getattr(module, app_name)

def processWorker(app, host, port):
    print(f"Worker PID:{__import__('os').getpid()} listening on {host}:{port}")
    Server = make_server(host, port, app)
    Server.serve_forever()

def main():
    if len(sys.argv) < 2:
        print("Usage: whiteserver <module_name>:<app_name>")
        sys.exit(1)
    target = sys.argv[1]
    app = import_app(target)


    workers = []

    for i in range(3):
            cProcess = Process(target=processWorker, args=(app, "127.0.0.1", 8000))
            cProcess.start()
            workers.append(cProcess)

    for cProcess in workers:
        cProcess.join() 



    
    print(f"Master PID:{__import__('os').getpid()} started worker process.")
    print(f"child process PID:{cProcess.pid} listening on 127.0.0.1:8000")
    print("Press Ctrl+C to stop the server.")
    

if __name__ == "__main__":
    main()