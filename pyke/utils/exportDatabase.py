from datetime import date, datetime
import logging
import os
import subprocess


_logger = logging.getLogger(__name__)

def cleanSaveFolder():
    while len(os.listdir("./db_saves")) > 7:
        oldest_file = min([datetime.strptime(f, "%d-%m-%Y.sql") for f in os.listdir("./db_saves") if f != "init.sql"])
        process = subprocess.Popen(
            f"rm -rf ./db_saves/{oldest_file.strftime('%d-%m-%Y')}.sql",
            stderr=subprocess.DEVNULL,
            shell=True
        )
        process.wait()
        _logger.info(f"Oldest save: ./db_saves/\"{oldest_file.strftime('%d-%m-%Y')}.sql\" deleted")

def exportDataBase():
    today = date.today().strftime("%d-%m-%Y")
    process = subprocess.Popen(
        f"mysqldump -p'{os.getenv('DB_ROOT_PASS')}' -h {os.getenv('DB_HOST')} {os.getenv('DB_NAME')} > ./db_saves/{today}.sql;"
        f"rm -rf ./db/db_saves/init.sql; cp ./db/db_saves/{today}.sql ./db_saves/init.sql",
        shell=True
    )
    process.wait()
    _logger.info(f"save done at ./db_saves/{today}.sql")
    cleanSaveFolder()