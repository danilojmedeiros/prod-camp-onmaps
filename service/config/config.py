import os

bind = "0.0.0.0:5000"
workers = os.getenv("GUNICORN_WORKERS", 1)
timeout = os.getenv("GUNICORN_TIMEOUT", 300)
keepalive = 24 * 60 * 60  # 1 day
threads = os.getenv("GUNICORN_THREADS", 1)
statsd_host = os.getenv("STATSD_EXPORTER")
statsd_prefix = os.getenv("STATSD_PREFIX")
loglevel = os.environ.get("GUNICORN_LOGLEVEL", 'debug')
