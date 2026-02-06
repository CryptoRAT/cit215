import logging
import os
import uuid
from datetime import datetime
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template, request, jsonify

APP_NAME = "log-lab-buttons"
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

os.makedirs(LOG_DIR, exist_ok=True)

app = Flask(__name__)

def build_logger() -> logging.Logger:
    logger = logging.getLogger(APP_NAME)
    logger.setLevel(logging.DEBUG)  # app captures everything; handlers can filter later

    # Avoid duplicate handlers if reloaded
    if logger.handlers:
        return logger

    fmt = logging.Formatter(
        fmt="%(asctime)s level=%(levelname)s app=%(name)s request_id=%(request_id)s ip=%(ip)s path=%(path)s msg=%(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    # File handler
    fh = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    # Console handler (useful if running in a terminal)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

logger = build_logger()

def log_event(level: str, message: str):
    # Minimal "structured context" without extra libs
    extra = {
        "request_id": request.headers.get("X-Request-ID", str(uuid.uuid4())),
        "ip": request.headers.get("X-Forwarded-For", request.remote_addr or "-"),
        "path": request.path,
    }

    level = level.lower().strip()
    if level == "debug":
        logger.debug(message, extra=extra)
    elif level == "info":
        logger.info(message, extra=extra)
    elif level == "warning":
        logger.warning(message, extra=extra)
    elif level == "error":
        logger.error(message, extra=extra)
    elif level == "critical":
        logger.critical(message, extra=extra)
    else:
        logger.info(f"unknown_level={level} {message}", extra=extra)

@app.route("/")
def home():
    # A baseline log line to show "normal behavior logs"
    log_event("info", "page_view")
    return render_template("index.html")

@app.route("/api/log/<level>", methods=["POST"])
def api_log(level: str):
    payload = request.get_json(silent=True) or {}
    note = payload.get("note", "").strip()
    msg = f"button_click level={level} note={note if note else '-'}"
    log_event(level, msg)
    return jsonify({"ok": True, "level": level, "ts": datetime.utcnow().isoformat() + "Z"})

@app.route("/api/error-demo", methods=["GET"])
def api_error_demo():
    # Intentional error to create app error log + nginx upstream behavior
    log_event("warning", "about_to_raise_demo_error")
    raise RuntimeError("Intentional demo error for log lab")

if __name__ == "__main__":
    # Dev server (good enough for a lab)
    # Listen on all interfaces so nginx on same VM can proxy to it.
    app.run(host="0.0.0.0", port=5000, debug=False)
