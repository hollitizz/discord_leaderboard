from mysql.connector import MySQLConnection
from mysql.connector.connection import CursorBase
import os


class SQLRequests(MySQLConnection):
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

    def getTables(self) -> 'list[str]':
        self.__clearCache()
        self.__cursor.execute("SHOW TABLES")
        return self.__cursor.fetchall()