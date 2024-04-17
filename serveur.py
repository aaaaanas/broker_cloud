from cmath import e
import configparser
import subprocess
import threading
from flask import Flask, request, abort
import logging
import psutil
import os
import os.path
from flask import request
from flask import jsonify

import traceback

BROKER_HOST = "192.168.97.45"
BROKER_PORT = 8000
API_HOST = "192.168.97.45"
API_PORT = 8000


CONFIG_FILE = "C:\\\\Users\\\\UF187ATA\\\\conf\\\\anas.conf.txt"

try:
    with open(CONFIG_FILE, 'r') as f:
        pass
except FileNotFoundError:
    logging.error(f"Le fichier de configuration {CONFIG_FILE} n'existe pas.")
    abort(500)


print(f"Configuration file path: {CONFIG_FILE}")


def is_mosquitto_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'mosquitto.exe':
            return True
    return False

app = Flask(__name__)



 
def load_config():
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        return config
    except FileNotFoundError:
        logging.error(f"Fichier de configuration {CONFIG_FILE} introuvable")
        raise
 
def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as configfile:
            config.write(configfile)
    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde du fichier de configuration : {e}")
        raise

def write_to_config_file(new_config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            f.write(new_config)
        logging.info(f"Nouvelle configuration écrite dans {CONFIG_FILE}")
    except Exception as e:
        logging.error(f"Erreur lors de l'écriture dans le fichier de configuration : {e}")



   



from flask import jsonify

import json
from flask import jsonify

@app.route('/update_config', methods=['POST'])
def update_config():
    try:
        new_config = request.get_json()
        print(new_config)  

        with open(CONFIG_FILE, 'w') as f:
            json.dump(new_config, f)

        logging.info(f"Nouvelle configuration écrite dans {CONFIG_FILE}")
        return jsonify({'message': 'Configuration mise à jour avec succès'}), 200

    except Exception as e:
        logging.error(f"Erreur lors de l'écriture dans le fichier de configuration : {e}")
        return jsonify({'error': 'Erreur lors de la mise à jour de la configuration'}), 500



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    broker_thread = threading.Thread()
    broker_thread.start()
    app.run(host=API_HOST, port=API_PORT, debug=True)

@app.errorhandler(500)
def internal_server_error(e):
    logging.error(f"Erreur 500: {e}")
    return "Une erreur interne est survenue", 500

@app.errorhandler(500)
def internal_server_error(e):
    logging.error(f"Erreur 500: {e}")
    logging.error(traceback.format_exc())
    return "Une erreur interne est survenue", 500




