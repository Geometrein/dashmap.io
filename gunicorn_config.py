"""
Gunicorn configuration.
"""
import multiprocessing

# Server socket
BIND = "0.0.0.0:8080"

# The number of pending connections.
BACKLOG = 1024

# Running the server with N workers:
# Docs: https://docs.gunicorn.org/en/stable/configure.html
WORKERS = multiprocessing.cpu_count() * 2 + 1
