# whiteServer

A lightweight, beginner-friendly Python WSGI application server built on top of Python's built-in `wsgiref` library. **whiteServer** lets you serve any WSGI-compatible web application with a single command — no complex configuration required.

> [!NOTE]
> This project is actively being developed. Check back regularly for new features and improvements!

---

## Features

- **Zero dependencies** — built entirely on Python's standard library
- **WSGI-compatible** — works with any WSGI app (Flask, Django, custom, etc.)
- **Simple CLI** — start a server with a single command
- **Configurable host & port** — defaults to `127.0.0.1:8000`, easily overridden

---

## Project Structure

```
whiteServer/
├── server.py      # Core server logic and CLI entry point
├── app.py         # Example WSGI application
├── LICENSE        # MIT License
└── README.md
```

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/whiteServer.git
cd whiteServer
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv env
# Windows
env\Scripts\activate
# macOS / Linux
source env/bin/activate
```

### 3. Run the example app

```bash
python server.py app:hello_app
```

Then open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000) and you'll see:

```
Hello from http server version 0.1
```

---

## Usage

```bash
python server.py <module_name>:<app_name>
```

| Argument | Description |
|---|---|
| `module_name` | Python module (file) that contains your WSGI app |
| `app_name` | The callable inside that module that is your WSGI app |

### Example

If your project has a file `myapp.py` with a WSGI callable named `application`:

```bash
python server.py myapp:application
```

---

## Writing a WSGI App

A WSGI application is just a Python callable that accepts `environ` and `start_response`. Here's the minimal example included in [`app.py`](app.py):

```python
def hello_app(environ, start_response):
    body = b"Hello from http server version 0.1"
    headers = [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(body))),
    ]
    start_response("200 OK", headers)
    return [body]
```

---

## API Reference

### `WhiteServer(app, host="127.0.0.1", port=8000)`

The core server class defined in [`server.py`](server.py).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `app` | callable | — | A WSGI-compatible application callable |
| `host` | `str` | `"127.0.0.1"` | Host address to bind to |
| `port` | `int` | `8000` | Port number to listen on |

#### `WhiteServer.runServer()`

Starts the server and blocks until interrupted (Ctrl+C).

---

### `import_app(target)`

Dynamically imports a WSGI app from a `"module:callable"` string.

```python
from server import import_app

app = import_app("myapp:application")
```

---

## Roadmap

- [ ] Custom host/port via CLI flags
- [ ] Multi-threaded request handling
- [ ] Request logging middleware
- [ ] HTTPS / TLS support
- [ ] Hot-reload on file changes

---

## License

This project is licensed under the [MIT License](LICENSE).

