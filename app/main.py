import os
from flask import Flask, jsonify

app = Flask(__name__)

# CONFIGURATION
# We grab these from the Environment. This is a Cloud Native best practice.
# If the variable isn't set, we use a default.
APP_PORT = int(os.environ.get("APP_PORT", 5000))
APP_MESSAGE = os.environ.get("APP_MESSAGE", "Welcome to the Container Basics Course!")
APP_VERSION = "1.0.0"

@app.route("/")
def hello():
    return jsonify({
        "message": APP_MESSAGE,
        "version": APP_VERSION,
        "hostname": os.environ.get("HOSTNAME", "unknown") # In Docker, hostname is the Container ID
    })

@app.route("/health")
def health():
    # This is useful for Kubernetes Liveness/Readiness probes later
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=APP_PORT)