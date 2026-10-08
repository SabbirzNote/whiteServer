import os
import sys
import platform
import socket
import getpass
import shutil
import html
import json

try:
    import psutil
except ImportError:
    psutil = None


def format_bytes(value):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if value < 1024:
            return f"{value:.2f} {unit}"
        value /= 1024

    return f"{value:.2f} PB"


def row(label, value):
    return f"""
        <div class="row">
            <span class="label">{html.escape(str(label))}</span>
            <span class="value">{html.escape(str(value))}</span>
        </div>
    """


def card(title, content):
    return f"""
        <section class="card">
            <h2>{title}</h2>
            {content}
        </section>
    """


def hello_app(environ, start_response):

    # -----------------------------
    # System information
    # -----------------------------

    system = ""

    system += row("Hostname", socket.gethostname())
    system += row("FQDN", socket.getfqdn())
    system += row("Operating System", platform.system())
    system += row("OS Release", platform.release())
    system += row("OS Version", platform.version())
    system += row("Machine", platform.machine())
    system += row("Architecture", platform.architecture()[0])
    system += row("Processor", platform.processor())
    system += row("CPU Count", os.cpu_count())
    system += row("Current User", getpass.getuser())
    system += row("Working Directory", os.getcwd())


    # -----------------------------
    # Python information
    # -----------------------------

    python = ""

    python += row("Python Version", platform.python_version())
    python += row("Implementation", platform.python_implementation())
    python += row("Executable", sys.executable)
    python += row("Python Prefix", sys.prefix)

    python_path = "<br>".join(
        html.escape(path)
        for path in sys.path
    )

    python += row("Python Path", python_path)


    # -----------------------------
    # Memory information
    # -----------------------------

    memory = ""

    if psutil:

        mem = psutil.virtual_memory()

        memory += row("Total", format_bytes(mem.total))
        memory += row("Used", format_bytes(mem.used))
        memory += row("Available", format_bytes(mem.available))
        memory += row("Free", format_bytes(mem.free))
        memory += row("Usage", f"{mem.percent}%")

    else:

        memory += row(
            "Status",
            "Install psutil to get memory information"
        )


    # -----------------------------
    # Disk information
    # -----------------------------

    disk = ""

    try:

        usage = shutil.disk_usage("/")

        percent = round(
            usage.used / usage.total * 100,
            2
        )

        disk += row("Mount", "/")
        disk += row("Total", format_bytes(usage.total))
        disk += row("Used", format_bytes(usage.used))
        disk += row("Free", format_bytes(usage.free))
        disk += row("Usage", f"{percent}%")

    except Exception as e:

        disk += row("Error", e)


    # -----------------------------
    # CPU information
    # -----------------------------

    cpu = ""

    cpu += row("Logical CPUs", os.cpu_count())

    if psutil:

        cpu += row(
            "Physical CPUs",
            psutil.cpu_count(logical=False)
        )

        cpu += row(
            "Current CPU Usage",
            f"{psutil.cpu_percent(interval=0.1)}%"
        )

        frequency = psutil.cpu_freq()

        if frequency:

            cpu += row(
                "CPU Frequency",
                f"{frequency.current:.2f} MHz"
            )


    # -----------------------------
    # Process information
    # -----------------------------

    process = ""

    process += row("PID", os.getpid())
    process += row("Parent PID", os.getppid())

    if psutil:

        current_process = psutil.Process(os.getpid())

        process += row(
            "Process Name",
            current_process.name()
        )

        process += row(
            "Status",
            current_process.status()
        )

        process += row(
            "Process Memory",
            format_bytes(
                current_process.memory_info().rss
            )
        )

        process += row(
            "CPU Usage",
            f"{current_process.cpu_percent()}%"
        )


    # -----------------------------
    # WSGI information
    # -----------------------------

    wsgi = ""

    wsgi_keys = [
        "REQUEST_METHOD",
        "PATH_INFO",
        "QUERY_STRING",
        "SERVER_NAME",
        "SERVER_PORT",
        "SERVER_PROTOCOL",
        "REMOTE_ADDR",
        "REMOTE_PORT",
        "SERVER_SOFTWARE",
        "SCRIPT_NAME",
        "wsgi.version",
        "wsgi.url_scheme",
        "wsgi.multithread",
        "wsgi.multiprocess",
        "wsgi.run_once",
    ]

    for key in wsgi_keys:

        if key in environ:

            wsgi += row(
                key,
                environ[key]
            )


    # -----------------------------
    # Network information
    # -----------------------------

    network = ""

    try:

        hostname = socket.gethostname()

        addresses = socket.gethostbyname_ex(
            hostname
        )[2]

        for address in addresses:

            network += row(
                "IP Address",
                address
            )

    except Exception as e:

        network += row(
            "Error",
            e
        )


    # -----------------------------
    # HTTP Headers
    # -----------------------------

    headers = ""

    for key, value in environ.items():

        if key.startswith("HTTP_"):

            name = key[5:].replace(
                "_",
                "-"
            )

            headers += row(
                name,
                value
            )


    # -----------------------------
    # Build HTML
    # -----------------------------

    body = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Server Diagnostic</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 30px;

    background: #0f172a;

    color: #e2e8f0;

    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Roboto,
        Arial,
        sans-serif;
}}

.container {{
    max-width: 1200px;
    margin: auto;
}}

header {{
    margin-bottom: 30px;
}}

header h1 {{
    margin: 0;

    font-size: 32px;

    color: #f8fafc;
}}

header p {{
    margin-top: 8px;

    color: #94a3b8;
}}

.grid {{
    display: grid;

    grid-template-columns:
        repeat(auto-fit, minmax(350px, 1fr));

    gap: 20px;
}}

.card {{
    background: #1e293b;

    border: 1px solid #334155;

    border-radius: 12px;

    padding: 20px;

    box-shadow:
        0 10px 25px
        rgba(0, 0, 0, 0.15);
}}

.card h2 {{
    margin: 0 0 18px 0;

    font-size: 18px;

    color: #38bdf8;

    border-bottom:
        1px solid #334155;

    padding-bottom: 12px;
}}

.row {{
    display: flex;

    justify-content: space-between;

    gap: 20px;

    padding: 9px 0;

    border-bottom:
        1px solid #273449;

    font-size: 14px;
}}

.row:last-child {{
    border-bottom: none;
}}

.label {{
    color: #94a3b8;

    min-width: 120px;
}}

.value {{
    color: #f1f5f9;

    text-align: right;

    word-break: break-word;
}}

footer {{
    margin-top: 30px;

    text-align: center;

    color: #64748b;

    font-size: 13px;
}}

@media (max-width: 600px) {{

    body {{
        padding: 15px;
    }}

    .grid {{
        grid-template-columns: 1fr;
    }}

    .row {{
        flex-direction: column;

        gap: 5px;
    }}

    .value {{
        text-align: left;
    }}

}}

</style>

</head>


<body>

<div class="container">

<header>

<h1>Server Diagnostic Dashboard</h1>

<p>
Python / WSGI Server Environment Information
</p>

</header>


<div class="grid">

{card("System", system)}

{card("Python", python)}

{card("CPU", cpu)}

{card("Memory", memory)}

{card("Disk", disk)}

{card("Process", process)}

{card("Network", network)}

{card("WSGI Server", wsgi)}

{card("HTTP Headers", headers)}

</div>


<footer>

Python Server Diagnostic Tool

</footer>

</div>

</body>

</html>
"""

    body = body.encode("utf-8")

    response_headers = [
        ("Content-Type", "text/html; charset=utf-8"),
        ("Content-Length", str(len(body))),
    ]

    start_response(
        "200 OK",
        response_headers
    )

    return [body]
