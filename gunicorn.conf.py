import os
import multiprocessing

# Gunicorn configuration
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"
workers = 2
threads = 2
worker_class = 'sync'
timeout = 30
graceful_timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100

# Logging
loglevel = 'info'
accesslog = '-'
errorlog = '-'
