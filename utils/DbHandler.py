import json
from types import SimpleNamespace as Namespace
from json import JSONEncoder

class DbEncoder(JSONEncoder):
        def default(self, o): return o.__dict__

class DbHandler():
    def __init__(self):
        with open("db.json", encoding='utf-8') as tmp0:
            self.db = json.load(tmp0, object_hook=lambda d: Namespace(**d))

    async def save(self):
        with open("db.json", "w", encoding='utf-8') as db_file:
            json.dump(self.db, db_file, indent=4, cls=DbEncoder)
