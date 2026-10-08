# whiteServer

A lightweight, beginner-friendly Python WSGI application server built on top of Python's built-in `wsgiref` library and `multiprocessing`. **whiteServer** lets you serve any WSGI-compatible web application with a single command — no complex configuration required.

> [!NOTE]
> This project is actively being developed. Check back regularly for new features and improvements!

---

## Features

- **Zero dependencies** — built entirely on Python's standard library
- **WSGI-compatible** — works with any WSGI app (Flask, Django, custom, etc.)
- **Multi-process worker model** — handles requests concurrently out of the box
- **Simple CLI** — start a server anywhere using a simple command

---

## Installation

Install directly from PyPI (once published), or locally via pip:

```bash
pip install whiteserver
```

Alternatively, to install directly from the source code during development:

```bash
git clone https://github.com/your-username/whiteServer.git
cd whiteServer
pip install .
```

---

## Quick Start

### 1. Create your WSGI App
Create a file named `myapp.py`:
```python
def application(environ, start_response):
    body = b"Hello from whiteServer!"
    headers = [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(body))),
    ]
    start_response("200 OK", headers)
    return [body]
```

### 2. Run the Server
Use the new CLI tool to run your application:

```bash
whiteserver myapp:application
```

Then open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000) and you'll see your app running!

---

## Usage

```bash
whiteserver <module_name>:<app_name>
```

| Argument | Description |
|---|---|
| `module_name` | Python module (file) that contains your WSGI app |
| `app_name` | The callable inside that module that is your WSGI app |

---

## Roadmap

- [ ] Custom host/port via CLI flags
- [ ] Multi-threaded/Multi-process request handling improvements
- [ ] Request logging middleware
- [ ] HTTPS / TLS support
- [ ] Hot-reload on file changes

---

## License

This project is licensed under the [MIT License](LICENSE).
