from flask import Flask
import threading

app = Flask(__name__)

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/')
def home():
    return 'PDF Telegram Bot is running', 200

def run_healthcheck():
    app.run(host='0.0.0.0', port=8000, threaded=True)

def start_healthcheck_server():
    thread = threading.Thread(target=run_healthcheck, daemon=True)
    thread.start()
