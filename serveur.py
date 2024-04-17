import configparser
import subprocess
import threading
from flask import Flask, request, abort
import logging
import os
import uuid

BROKER_HOST = "192.168.97.45"
BROKER_PORT = 8000
API_HOST = "192.168.97.45"
API_PORT = 8000
CONFIG_FILE = "C:\\Users\\UF187ATA\\Downloads\\a.conf.txt"  # Corrected path

app = Flask(__name__)

def load_config():
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        return config
    except FileNotFoundError:
        logging.error(f"Configuration file {CONFIG_FILE} not found")
        raise

def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as configfile:
            config.write(configfile)
    except Exception as e:
        logging.error(f"Error saving configuration file: {e}")
        raise

def start_broker():
    logging.debug("Starting Mosquitto broker")
    try:
        subprocess.run(["mosquitto"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.debug("Mosquitto broker started successfully")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error starting Mosquitto broker: {e}")

@app.route('/update_config', methods=['POST'])
def update_config():
    if 'Authorization' not in request.headers or request.headers['Authorization'] != f'Bearer {my_secret_token}':
        abort(401)

    new_config = request.data.decode('utf-8')
    try:
        with open(CONFIG_FILE, 'w') as f:
            f.write(new_config)
        subprocess.run(['systemctl', 'restart', 'mosquitto'], check=True)
        return 'Configuration updated successfully', 200
    except Exception as e:
        logging.error(f"Error updating configuration: {e}")
        abort(500)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Start the Mosquitto broker in a separate thread
    broker_thread = threading.Thread(target=start_broker)
    broker_thread.start()
    
    # Generate a random UUID as the secret token
    my_secret_token = str(uuid.uuid4())
    print("Your secret token:", my_secret_token)
    
    # Run the Flask app
    app.run(host=API_HOST, port=API_PORT, debug=True)
