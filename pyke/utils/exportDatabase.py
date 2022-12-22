from datetime import date
from logging import getLogger
import os
import subprocess


_logger = getLogger(__name__)


def exportDataBase():
    today = date.today().strftime("%d-%m-%Y")
    subprocess.Popen(
        f"mysqldump -u {os.getenv('DB_USER')} -p{os.getenv('DB_PASS')} {os.getenv('DB_NAME')} > {os.getenv('DB_SAVE_PATH')}/{today}.sql",
        stderr=subprocess.DEVNULL,
        shell=True
    )
    _logger.info(f"save done at {os.getenv('DB_SAVE_PATH')}/{today}.sql")