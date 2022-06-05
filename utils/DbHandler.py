import json
from types import SimpleNamespace as Namespace
from json import JSONEncoder

class DbEncoder(JSONEncoder):
    def default(self, o): return o.__dict__

class DbHandler():
    def __init__(self, db_path):
        self.db_path = db_path
        with open(f"{self.db_path}", encoding='utf-8') as tmp0:
            self.db = json.load(tmp0, object_hook=lambda d: Namespace(**d))

    def save(self):
        with open(f"{self.db_path}", "w", encoding='utf-8') as db_file:
            json.dump(self.db, db_file, indent=4, cls=DbEncoder)
