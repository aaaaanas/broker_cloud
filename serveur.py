import configparser
import subprocess
import threading
from flask import Flask, request, abort
import logging

BROKER_HOST = "192.168.97.45"
BROKER_PORT = 8000
API_HOST = "192.168.97.45"
API_PORT = 8000
CONFIG_FILE = "C:\\Users\\UF187ATA\\Downloads\\a.conf.txt"

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
    logging.debug("Démarrage du broker Mosquitto")
    try:
        result = subprocess.run(["mosquitto"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.debug(f"Sortie de la commande: {result.stdout.decode('utf-8')}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Erreur lors du démarrage du broker Mosquitto: {e}")
        if e.stderr:
            logging.error(f"Erreur de la commande: {e.stderr.decode('utf-8', 'ignore')}")
        else:
            logging.error("Erreur de la commande: Aucune sortie d'erreur disponible")

@app.route('/update_config', methods=['POST'])
def update_config():
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

