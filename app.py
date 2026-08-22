import os
import time
import socket
from datetime import datetime
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
START_TIME = datetime.utcnow()
COUNTER_STATE = {"count": 0}

@app.route("/")
def index():
    uptime_seconds = int((datetime.utcnow() - START_TIME).total_seconds())
    hostname = socket.gethostname()
    return render_template(
        "index.html",
        version=APP_VERSION,
        hostname=hostname,
        uptime=uptime_seconds,
        start_time=START_TIME.strftime("%Y-%m-%d %H:%M:%S UTC")
    )

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": APP_VERSION,
        "service": "python-ec2-demo-app"
    }), 200

@app.route("/api/info")
def api_info():
    uptime_seconds = int((datetime.utcnow() - START_TIME).total_seconds())
    return jsonify({
        "app_name": "EC2 Deployment Verification App",
        "version": APP_VERSION,
        "environment": os.getenv("FLASK_ENV", "production"),
        "hostname": socket.gethostname(),
        "uptime_seconds": uptime_seconds,
        "python_version": os.sys.version,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }), 200

@app.route("/api/counter", methods=["GET", "POST"])
def api_counter():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        action = data.get("action", "increment")
        if action == "increment":
            COUNTER_STATE["count"] += 1
        elif action == "decrement":
            COUNTER_STATE["count"] -= 1
        elif action == "reset":
            COUNTER_STATE["count"] = 0
            
    return jsonify({
        "count": COUNTER_STATE["count"],
        "last_updated": datetime.utcnow().strftime("%H:%M:%S UTC")
    }), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
