import multiprocessing

# Server socket
bind = "0.0.0.0:8080"

# The number of pending connections.
backlog = 1024

# Running the server with N workers:
# Docs: https://docs.gunicorn.org/en/stable/configure.html
workers = multiprocessing.cpu_count() * 2 + 1
