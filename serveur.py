from cmath import e
import configparser
import subprocess
import threading
from flask import Flask, request, abort
import logging
import psutil
import os

BROKER_HOST = "192.168.97.45"
BROKER_PORT = 8000
API_HOST = "192.168.97.45"
API_PORT = 8000


CONFIG_FILE = os.path.join(os.path.expanduser("~"), "Downloads", "a.conf")
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

def start_broker():
    if not is_mosquitto_running():
        logging.debug("Démarrage du broker Mosquitto")
        try:
            result = subprocess.run(["mosquitto", "-c", CONFIG_FILE], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logging.debug(f"Sortie de la commande: {result.stdout.decode('utf-8')}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Erreur lors du démarrage du broker Mosquitto: {e}")
            if e.stderr:
                logging.error(f"Erreur de la commande: {e.stderr.decode('utf-8', 'ignore')}")
            else:
                logging.error("Erreur de la commande: Aucune sortie d'erreur disponible")
    else:
        logging.debug("Le broker Mosquitto est déjà en cours d'exécution")



@app.route('/update_config', methods=['POST'])
def update_config():
    if 'Authorization' not in request.headers or request.headers['Authorization'] != 'Bearer my_secret_token':
        abort(401)

    new_config = request.data.decode('utf-8')
    try:
        with open(CONFIG_FILE, 'w') as f:
            f.write(new_config)
        subprocess.run(['systemctl', 'restart', 'mosquitto'], check=True)
        return 'Configuration mise à jour avec succès', 200
    except Exception as e:
        logging.error(f"Erreur lors de la mise à jour de la configuration : {e}")
        abort(500)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    broker_thread = threading.Thread(target=start_broker)
    broker_thread.start()
    app.run(host=API_HOST, port=API_PORT, debug=True)



@app.errorhandler(500)
def internal_server_error(e):
    logging.error(f"Erreur 500: {e}")
    return "Une erreur interne est survenue", 500






