from mysql import connector
from mysql.connector.connection import CursorBase
import dotenv
from DbHandler import DbHandler
import os

dotenv.load_dotenv("../pyke/.env")

db = DbHandler("./olddb.json")

class SQLRequests(connector.MySQLConnection):
    def __init__(self):
        super().__init__(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME')
        )
        self.__cursor: CursorBase = self.cursor()
    
    def __clearCache(self):
        try:
            self.__cursor.fetchall()
        except:
            pass
    
    def createUser(self, user_id: int):
        request = f"""
            INSERT INTO users (user_id)
            VALUES ("{user_id}")
        """
        self.__clearCache()
        self.__cursor.execute(request)
        self.commit()
        return 'ok'

    def addAccountToUser(self, user_id: int, summoner_name: str, tier: int, rank: int, lp: int, league_id: str):
        request = f"""
            INSERT INTO accounts (user_id, summoner_name, lp, tier, `rank`, league_id)
            VALUES ("{user_id}", "{summoner_name}", {lp}, {tier}, {rank}, "{league_id}")
        """
        self.__clearCache()
        self.__cursor.execute(request)
        self.commit()
        return 'ok'

converter = SQLRequests()

for user in db.db.users:
    user_id = user.tag.replace("<", "").replace(">", "").replace("@", "").replace("!", "")
    converter.createUser(user_id)
    converter.addAccountToUser(user_id, user.name, user.tier, user.rank, user.lp, user.id)
