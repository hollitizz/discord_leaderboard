from time import sleep
from datetime import datetime
from logging import getLogger
import os
import subprocess

_logger = getLogger(__name__)

def cleanSaveFolder():
    while len(os.listdir(os.getenv("DB_SAVE_PATH"))) > 7:
        oldest_file = min([datetime.strptime(f[:-4], "%d-%m-%Y") for f in os.listdir(os.getenv("DB_SAVE_PATH"))])
        subprocess.Popen(
            f"rm -rf {os.getenv('DB_SAVE_PATH')}/{oldest_file.strftime('%d-%m-%Y')}.sql",
            stderr=subprocess.DEVNULL,
            shell=True
        )
        _logger.info(f"Oldest save: \"{oldest_file.strftime('%d-%m-%Y')}.sql\" deleted")
        sleep(0.5)