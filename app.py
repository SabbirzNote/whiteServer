
def hello_app(environ, start_response):
    body = b"Hello from http server version 0.1"
    headers = [("Content-Type", "text/plain"),("Content-Length", str(len(body))),]

    start_response(
        "200 OK", headers
    )

    return [body]

